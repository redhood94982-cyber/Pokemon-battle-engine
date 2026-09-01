"""Battle controller: executes rules; canonical move/nature/ability data lives in Database."""
import random
from .battle_state import BattleState
from .damage_v4 import calculate_damage
from . import item_resolver
from .move import Move
from .Database.abilities import ABILITIES
from .Database.natures import NATURES
from .Database.species import SPECIES
from .Database.types import TYPES
from .Database.type_chart import TYPE_CHART

CRITICAL_HIT_CHANCE = 24
STATUS_MOVES_WITHOUT_DAMAGE = {"haze", "ingrain", "leech_seed", "mean_look",
                                "nasty_plot", "parting_shot", "perish_song",
                                "sleep_powder", "sunny_day", "swords_dance",
                                "tailwind", "toxic", "yawn", "aurora_veil"}

class Battle:
    def __init__(self):
        self.state = BattleState()
        self.player1_team, self.player2_team = [], []
        self.active_p1, self.active_p2 = [], []
        self.winner = None
        self.state.log("Battle initialized.")

    # ---- Database gateway -------------------------------------------------
    @staticmethod
    def get_move(name): return Move.from_database(name)
    @staticmethod
    def get_ability(name): return ABILITIES.get(name)
    @staticmethod
    def get_nature(name): return NATURES.get(name)
    @staticmethod
    def get_species(name): return SPECIES.get(name)
    @staticmethod
    def get_type(name):
        if name not in TYPES: raise KeyError(f"Unknown type: {name}")
        return name
    @staticmethod
    def get_type_multiplier(move_type, defender_types):
        row = TYPE_CHART.get(move_type, {})
        result = 1.0
        for t in defender_types: result *= row.get(t, 1.0)
        return result

    def accuracy_check(self, pokemon, move, target=None):
        # Database uses 0 for "never misses".
        if move.accuracy in (0, 100): return True
        return random.randint(1, 100) <= move.accuracy

    def critical_hit(self, pokemon=None, move=None):
        if pokemon is not None and getattr(pokemon, "ability", "") in {"Battle Armor", "Shell Armor"}:
            return False
        return random.randint(1, CRITICAL_HIT_CHANCE) == 1

    def paralysis_check(self, pokemon):
        if pokemon.status != "paralysis": return False
        if random.randint(1, 4) == 1:
            self.state.log(f"{pokemon.species} is fully paralyzed! It can't move!")
            return True
        return False

    def sleep_check(self, pokemon):
        if pokemon.status != "sleep": return False
        if pokemon.sleep_counter <= 0:
            pokemon.status = None
            self.state.log(f"{pokemon.species} woke up!")
            return False
        self.state.log(f"{pokemon.species} is fast asleep.")
        pokemon.sleep_counter -= 1
        return True

    def register_teams(self, player1_team, player2_team):
        if len(player1_team) != 6 or len(player2_team) != 6:
            raise ValueError("Both players must have exactly 6 Pokémon.")
        self.player1_team, self.player2_team = list(player1_team), list(player2_team)
        for p in self.player1_team: p._battle_side = 1
        for p in self.player2_team: p._battle_side = 2
        self.state.log("Teams registered.")

    def start_battle(self):
        if len(self.player1_team) != 6 or len(self.player2_team) != 6:
            raise ValueError("Register both six-Pokémon teams before starting.")
        self.active_p1 = [self.player1_team[0], self.player1_team[1]]
        self.active_p2 = [self.player2_team[0], self.player2_team[1]]
        for p in self.active_p1 + self.active_p2: self._on_switch_in(p)
        self.state.log(f"Player 1 sent out {self.active_p1[0].species} and {self.active_p1[1].species}.")
        self.state.log(f"Player 2 sent out {self.active_p2[0].species} and {self.active_p2[1].species}.")

    def get_active_team(self, pokemon):
        return self.active_p1 if pokemon in self.active_p1 else self.active_p2

    def get_turn_order(self, actions=None):
        battlers = [p for p in self.active_p1 + self.active_p2 if not p.is_fainted()]
        random.shuffle(battlers)
        def key(p):
            move_priority = actions.get(id(p), 0) if actions else 0
            speed = p.get_modified_stat("spe")
            side = 1 if p in self.active_p1 else 2
            if self.state.tailwind_p1 and side == 1: speed *= 2
            if self.state.tailwind_p2 and side == 2: speed *= 2
            return move_priority, speed
        battlers.sort(key=key, reverse=not self.state.trick_room)
        return battlers

    def begin_turn(self):
        self.state.turn += 1
        self.state.last_damage = 0
        self.state.last_target = None
        self.state.last_move = None
        order = self.get_turn_order()
        self.state.log(f"--- Turn {self.state.turn} ---")
        self.state.log("Turn order: " + ", ".join(p.species for p in order))
        return order

    def _targets(self, attacker, move, chosen_target=None):
        foes = self.active_p2 if attacker in self.active_p1 else self.active_p1
        allies = self.active_p1 if attacker in self.active_p1 else self.active_p2
        living_foes = [p for p in foes if not p.is_fainted()]
        living_allies = [p for p in allies if not p.is_fainted()]
        target = chosen_target if chosen_target in living_foes + living_allies else None
        t = move.target
        if t in {"all_adjacent_foes", "all_opponents", "spread"}: return living_foes
        if t in {"all", "all_adjacent"}: return [p for p in self.active_p1+self.active_p2 if not p.is_fainted()]
        if t in {"ally", "ally_side"}: return [attacker] if t == "ally" else living_allies
        if t == "self": return [attacker]
        return [target or (living_foes[0] if living_foes else None)]

    def perform_turn(self, selections=None):
        """Execute a turn. Selections are keyed by id(Pokemon) or species name."""
        selections = selections or {}
        def selected(pokemon):
            return selections.get(id(pokemon), selections.get(pokemon.species))

        actions = {}
        for p in self.active_p1 + self.active_p2:
            choice = selected(p)
            if choice is None:
                move = next((m for m in p.moves if m.has_pp()), None)
            else:
                move = choice[0] if isinstance(choice, tuple) else choice
                if isinstance(move, str):
                    move = Move.from_database(move)
            if move is not None:
                actions[id(p)] = move.priority

        for pokemon in self.get_turn_order(actions):
            if pokemon.is_fainted():
                continue
            if getattr(pokemon, "_flinched", False):
                self.state.log(f"{pokemon.species} flinched and couldn't move!")
                pokemon._flinched = False
                continue
            choice = selected(pokemon)
            target_choice = choice[1] if isinstance(choice, tuple) and len(choice) > 1 else None
            if choice is None:
                move = next((m for m in pokemon.moves if m.has_pp()), None)
            else:
                move = choice[0] if isinstance(choice, tuple) else choice
                if isinstance(move, str):
                    move = Move.from_database(move)
            if move is None:
                self.state.log(f"{pokemon.species} has no move available.")
                continue
            if not move.has_pp():
                self.state.log(f"{move.name} has no PP left!")
                continue
            if move.name == "Fake Out" and pokemon._active_turns > 0:
                self.state.log(f"{pokemon.species} can't use Fake Out after entering battle!")
                continue
            if self.paralysis_check(pokemon) or self.sleep_check(pokemon):
                continue
            if not self.use_move(pokemon, move):
                continue
            if move.name == "Protect":
                pokemon._protected = True
                self.state.log(f"{pokemon.species} protected itself!")
                continue
            targets = [t for t in self._targets(pokemon, move, target_choice) if t is not None]
            if not targets:
                continue
            if not self.accuracy_check(pokemon, move, targets[0]):
                self.state.log(f"{pokemon.species}'s {move.name} missed!")
                continue
            for target in targets:
                if target.is_fainted():
                    continue
                if getattr(target, "_protected", False) and move.protectable:
                    self.state.log(f"{target.species} protected itself from {move.name}!")
                    continue
                crit = self.critical_hit(pokemon, move)
                damage = calculate_damage(pokemon, target, move, self.state, crit)
                if damage:
                    target.damage(damage)
                    self.state.last_damage, self.state.last_target = damage, target
                    self.state.log(f"{target.species} took {damage} damage! ({target.current_hp}/{target.max_hp} HP remaining)")
                    self._on_damage_taken(pokemon, target, move, damage, crit)
                    if move.drain:
                        pokemon.heal(max(1, int(damage * move.drain)))
                    if move.recoil:
                        recoil = max(1, int(damage * move.recoil))
                        pokemon.damage(recoil)
                        self.state.log(f"{pokemon.species} took {recoil} recoil damage!")
                if move.healing:
                    pokemon.heal(max(1, int(pokemon.max_hp * move.healing)))
                self._apply_move_effect(pokemon, target, move)
                if target.is_fainted():
                    self.state.log(f"{target.species} fainted!")
                    self._on_faint(target, pokemon, move)
                    winner = self.check_win_condition()
                    if winner:
                        return winner
            if pokemon.is_fainted():
                continue
        return self.check_win_condition()

    def use_move(self, pokemon, move):
        if pokemon.is_fainted() or move is None or not move.has_pp(): return False
        self.state.log(f"{pokemon.species} used {move.name}!")
        self.state.last_move = move.name
        return move.use_pp()

    def _apply_move_effect(self, user, target, move):
        effect = move.secondary_effect
        if move.stat_changes:
            for recipient, changes in move.stat_changes.items():
                obj = user if recipient in {"self", "user"} else target
                for stat, amount in changes.items(): obj.change_stage(stat, amount)
        if move.status_effect and random.randint(1,100) <= move.effect_chance:
            self._inflict_status(target, move.status_effect)
        if effect == "burn" and random.randint(1,100) <= move.effect_chance: self._inflict_status(target, "burn")
        elif effect == "freeze" and random.randint(1,100) <= move.effect_chance: self._inflict_status(target, "freeze")
        elif effect == "flinch" and random.randint(1,100) <= move.effect_chance: setattr(target, "_flinched", True)
        elif effect == "random_status" and random.randint(1,100) <= move.effect_chance:
            self._inflict_status(target, random.choice(["poison","paralysis","sleep"]))
        elif effect in {"speed_down","spdef_down","spatk_down"}:
            stat = {"speed_down":"spe","spdef_down":"spd","spatk_down":"spa"}[effect]
            target.change_stage(stat, -1)
        elif effect == "raise_spatk": user.change_stage("spa", 2)
        elif effect == "self_spatk_down": user.change_stage("spa", -2)
        elif effect == "clear_stat_changes":
            for p in self.active_p1+self.active_p2: p.stat_stages.update({k:0 for k in p.stat_stages})
        elif effect == "remove_item": target.item = None
        elif effect == "ingrain": setattr(user, "_ingrain", True)
        elif effect == "leech_seed": setattr(target, "_leech_seeded", True)
        elif effect == "trap": setattr(target, "_trapped", True)
        elif effect == "perish_song": setattr(user, "_perish", 3); setattr(target, "_perish", 3)
        elif effect == "aurora_veil": self._set_side_timer(user, "aurora_veil", 5)
        elif effect == "pivot": setattr(user, "_pivot", True)
        elif effect == "speed_down": target.change_stage("spe", -1)
        elif effect == "heal": user.heal(int(user.max_hp * 0.5))

        # Canonical named moves whose database notes contain a rule.
        if move.name == "Sunny Day": self.state.weather, self.state.weather_turns = "sun", 5
        if move.name == "Tailwind": self._set_side_timer(user, "tailwind", 4)
        if move.name == "Haze":
            for p in self.active_p1+self.active_p2: p.stat_stages = {k:0 for k in p.stat_stages}
        if move.name == "Swords Dance": user.change_stage("atk", 2)
        if move.name == "Nasty Plot": user.change_stage("spa", 2)
        if move.name == "Toxic": self._inflict_status(target, "toxic")
        if move.name == "Sleep Powder": self._inflict_status(target, "sleep")
        if move.name == "Yawn" and target.status is None: setattr(target, "_yawn", True)

    def _inflict_status(self, target, status):
        if target.status is not None: return False
        if status == "sleep": target.sleep_counter = random.randint(1,3)
        if status == "toxic": target.toxic_counter = 0
        target.status = status
        self.state.status_effect = status
        self.state.log(f"{target.species} became {status}!")
        return True

    def _set_side_timer(self, pokemon, name, turns):
        side = 1 if pokemon in self.active_p1 else 2
        setattr(self.state, f"{name}_p{side}", turns)

    def _on_switch_in(self, pokemon):
        pokemon._active_turns = 0
        ability = pokemon.ability
        if ability == "Drizzle": self.state.weather, self.state.weather_turns = "rain", 5
        elif ability == "Drought": self.state.weather, self.state.weather_turns = "sun", 5
        elif ability == "Electric Surge": self.state.terrain, self.state.terrain_turns = "electric", 5
        elif ability == "Grassy Surge": self.state.terrain, self.state.terrain_turns = "grassy", 5
        elif ability == "Dauntless Shield": pokemon.change_stage("def", 1)

    def _on_damage_taken(self, attacker, target, move, damage, crit):
        if target.ability == "Disguise" and damage > 0:
            # Data-driven ability identity; exact disguise state can be added later.
            self.state.log(f"{target.species}'s Disguise was triggered!")
        if target.ability == "Anger Point" and crit:
            target.stat_stages["atk"] = 6
        if target.ability == "Cursed Body" and move and random.randint(1,100) <= 30:
            setattr(target, "_disabled_move", move.name)
        if target.ability == "Flame Body" and move.makes_contact and random.randint(1,100) <= 30:
            self._inflict_status(attacker, "burn")
        if target.ability == "Effect Spore" and move.makes_contact and random.randint(1,100) <= 30:
            self._inflict_status(attacker, random.choice(["sleep","paralysis","poison"]))
        if target.ability == "Static" and move.makes_contact and random.randint(1,100) <= 30:
            self._inflict_status(attacker, "paralysis")
        if target.ability == "Gooey" and move.makes_contact:
            attacker.change_stage("spe", -1)
        if target.ability == "Cotton Down":
            attacker.change_stage("spe", -1)

    def _on_faint(self, target, attacker, move):
        if attacker.ability in {"Beast Boost", "Chilling Neigh", "Grim Neigh"}:
            stat = "atk" if attacker.ability == "Chilling Neigh" else "spa" if attacker.ability == "Grim Neigh" else max(("atk","def","spa","spd","spe"), key=lambda s: attacker.get_modified_stat(s))
            attacker.change_stage(stat, 1)
        if target.ability == "Aftermath" and move and move.makes_contact and attacker.ability != "Damp":
            attacker.damage(max(1, attacker.max_hp // 4))

    def resolve_item_damage(self, attacker, defender, move, damage, super_effective=False):
        """Resolve held-item reactions to a completed damaging hit."""
        attacker_record = item_resolver.item_record(attacker) or {}
        defender_record = item_resolver.item_record(defender) or {}

        recoil_fraction = attacker_record.get("recoil_fraction", 0)
        if recoil_fraction and damage > 0:
            loss = max(1, int(attacker.max_hp * recoil_fraction))
            attacker.current_hp = max(0, attacker.current_hp - loss)
            self.state.log(f"{attacker.species} lost {loss} HP from {attacker.item}!")

        if getattr(move, "makes_contact", False) and damage > 0:
            contact_fraction = defender_record.get("contact_recoil_fraction", 0)
            if contact_fraction:
                loss = max(1, int(attacker.max_hp * contact_fraction))
                attacker.current_hp = max(0, attacker.current_hp - loss)
                self.state.log(f"{attacker.species} was hurt by {defender.item}!")

        if super_effective and defender_record.get("trigger") == "super_effective_hit":
            stages = getattr(defender, "stat_stages", None)
            if stages is not None:
                stages["attack"] = stages.get("attack", 0) + defender_record.get("attack_stage_change", 0)
                stages["special_attack"] = stages.get("special_attack", 0) + defender_record.get("special_attack_stage_change", 0)
            self.state.log(f"{defender.species} activated {defender.item}!")

    def apply_item_end_turn(self, pokemon):
        """Resolve simple database-defined end-of-turn item effects."""
        record = item_resolver.item_record(pokemon) or {}
        if pokemon.current_hp <= 0:
            return

        if pokemon.status == "poison" and record.get("poison_heal_fraction"):
            amount = max(1, int(pokemon.max_hp * record["poison_heal_fraction"]))
            pokemon.current_hp = min(pokemon.max_hp, pokemon.current_hp + amount)
            self.state.log(f"{pokemon.species} restored HP with {pokemon.item}!")
            return

        if record.get("heal_fraction"):
            amount = max(1, int(pokemon.max_hp * record["heal_fraction"]))
            pokemon.current_hp = min(pokemon.max_hp, pokemon.current_hp + amount)
            self.state.log(f"{pokemon.species} restored HP with {pokemon.item}!")

        if record.get("non_poison_damage_fraction") and pokemon.status != "poison":
            amount = max(1, int(pokemon.max_hp * record["non_poison_damage_fraction"]))
            pokemon.current_hp = max(0, pokemon.current_hp - amount)
            self.state.log(f"{pokemon.species} was hurt by {pokemon.item}!")

    def end_turn(self):
        for pokemon in self.active_p1 + self.active_p2:
            if not pokemon.is_fainted(): pokemon._active_turns += 1
        for pokemon in self.player1_team + self.player2_team:
            if pokemon.is_fainted(): continue
            if getattr(pokemon, "_yawn", False):
                self._inflict_status(pokemon, "sleep"); pokemon._yawn = False
            if pokemon.status == "burn": pokemon.damage(max(1, pokemon.max_hp // 16))
            elif pokemon.status == "poison": pokemon.damage(max(1, pokemon.max_hp // 8))
            elif pokemon.status == "toxic":
                pokemon.toxic_counter = max(1, pokemon.toxic_counter + 1)
                pokemon.damage(max(1, pokemon.max_hp * pokemon.toxic_counter // 16))
            if getattr(pokemon, "_ingrain", False): pokemon.heal(max(1, pokemon.max_hp // 16))
            if getattr(pokemon, "_leech_seeded", False): 
                drain = max(1, pokemon.max_hp // 8); pokemon.damage(drain)
                foe_team = self.active_p2 if pokemon in self.active_p1 else self.active_p1
                for ally in foe_team:
                    if not ally.is_fainted(): ally.heal(drain); break
            if getattr(pokemon, "_perish", 0) > 0:
                pokemon._perish -= 1
                if pokemon._perish == 0: pokemon.current_hp = 0; self.state.log(f"{pokemon.species} fainted from Perish Song!")
        for p in self.active_p1 + self.active_p2:
            p._protected = False
        for pokemon in self.player1_team + self.player2_team:
            self.apply_item_end_turn(pokemon)
        self.state.decrement_timers()
        if self.state.weather_turns == 0: self.state.weather = None
        if self.state.terrain_turns == 0: self.state.terrain = None
        if self.state.trick_room_turns == 0: self.state.trick_room = False
        return self.check_win_condition()

    def switch_pokemon(self, team, active_slot, new_pokemon):
        active = self.active_p1 if team == 1 else self.active_p2
        reserve = self.player1_team if team == 1 else self.player2_team
        if new_pokemon not in reserve or new_pokemon.is_fainted() or not 0 <= active_slot < len(active): return False
        if new_pokemon in active or getattr(active[active_slot], "_trapped", False): return False
        self.state.log(f"{active[active_slot].species}, come back!")
        active[active_slot] = new_pokemon
        self._on_switch_in(new_pokemon)
        self.state.log(f"Go, {new_pokemon.species}!")
        return True

    def replace_fainted(self, team):
        active = self.active_p1 if team == 1 else self.active_p2
        reserve = self.player1_team if team == 1 else self.player2_team
        for i, p in enumerate(active):
            if p.is_fainted():
                candidates = [c for c in reserve if not c.is_fainted() and c not in active]
                if candidates:
                    active[i] = candidates[0]; self._on_switch_in(candidates[0])
                    self.state.log(f"Go, {candidates[0].species}!")

    def check_win_condition(self):
        p1_alive = any(not p.is_fainted() for p in self.player1_team)
        p2_alive = any(not p.is_fainted() for p in self.player2_team)
        if not p1_alive and not p2_alive: return "draw"
        if not p1_alive: return "player2"
        if not p2_alive: return "player1"
        return None
