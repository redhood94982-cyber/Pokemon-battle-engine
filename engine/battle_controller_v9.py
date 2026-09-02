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
    def can_mega_evolve(self, pokemon):
        """Return whether this Pokémon can legally Mega Evolve right now."""
        if pokemon is None or pokemon.is_fainted() or pokemon.mega_evolved:
            return False
        if not getattr(pokemon, "item", None):
            return False

        item = item_resolver.item_record(pokemon) or {}
        required_species = item.get("mega_evolution_species")
        if not required_species:
            return False

        # The held stone must match the Pokémon's pre-Mega species.
        base_species = getattr(pokemon, "original_species", None) or pokemon.species
        return base_species == required_species and f"Mega {required_species}" in SPECIES

    def mega_evolve(self, pokemon):
        """Apply a player's selected Mega Evolution before move-order resolution."""
        if not self.can_mega_evolve(pokemon):
            raise ValueError(f"{pokemon.species} cannot Mega Evolve with its current state/item.")

        side = 1 if pokemon in self.active_p1 else 2 if pokemon in self.active_p2 else None
        if side is None:
            raise ValueError("Only an active Pokémon can Mega Evolve.")

        used_attr = "mega_used_p1" if side == 1 else "mega_used_p2"
        if getattr(self.state, used_attr, False):
            raise ValueError(f"Player {side} has already used Mega Evolution.")

        base_species = pokemon.original_species or pokemon.species
        mega_species = f"Mega {base_species}"
        mega_data = SPECIES[mega_species]

        # Mega Evolution does not consume the Mega Stone.
        pokemon.mega_species = mega_species
        pokemon.mega_evolved = True
        pokemon.species = mega_species
        pokemon.base_stats = dict(mega_data["base_stats"])
        pokemon.types = list(mega_data["types"])
        pokemon.ability = mega_data["ability"]

        # HP is preserved; Mega forms do not alter the HP stat in our supported set.
        pokemon.recalculate_stats_preserve_hp()
        setattr(self.state, used_attr, True)
        self.state.log(f"{base_species} Mega Evolved into {mega_species}!")
        self.state.log(f"{mega_species}'s Ability became {pokemon.ability}!")
        return True

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

    def start_battle(self, player1_leads, player2_leads):
        """Start the battle with the two leads explicitly chosen by each player.

        Leads are deliberately not inferred from team-sheet order.  This keeps
        team selection separate from lead selection and prevents the engine
        from silently deploying the first two Pokémon on a team.
        """
        if len(self.player1_team) != 6 or len(self.player2_team) != 6:
            raise ValueError("Both players must have exactly 6 Pokémon.")
        self.active_p1 = self._validate_leads(player1_leads, self.player1_team, 1)
        self.active_p2 = self._validate_leads(player2_leads, self.player2_team, 2)
        self._process_switch_ins(self.active_p1 + self.active_p2)
        self.state.log(
            f"Player 1 sent out {self.active_p1[0].species} and {self.active_p1[1].species}."
        )
        self.state.log(
            f"Player 2 sent out {self.active_p2[0].species} and {self.active_p2[1].species}."
        )

    @staticmethod
    def _validate_leads(leads, team, player_number):
        if not isinstance(leads, (list, tuple)) or len(leads) != 2:
            raise ValueError(f"Player {player_number} must choose exactly 2 leads.")
        if leads[0] is leads[1]:
            raise ValueError(f"Player {player_number} cannot choose the same Pokémon twice.")
        if any(p not in team for p in leads):
            raise ValueError(f"Player {player_number}'s leads must come from that player's registered team.")
        if any(p.is_fainted() for p in leads):
            raise ValueError(f"Player {player_number} cannot lead with a fainted Pokémon.")
        return list(leads)

    def _process_switch_ins(self, pokemon_list):
        """Resolve simultaneous switch-in abilities in game Speed order.

        Switch-in abilities activate from faster to slower. For weather
        setters, the later (slower) activation overwrites the earlier
        weather. Speed ties are randomized.
        """
        battlers = list(pokemon_list)
        random.shuffle(battlers)
        battlers.sort(key=lambda p: p.get_modified_stat("spe"), reverse=True)
        for pokemon in battlers:
            self._on_switch_in(pokemon)

    def get_active_team(self, pokemon):
        return self.active_p1 if pokemon in self.active_p1 else self.active_p2

    def get_turn_order(self, actions=None):
        """Return action order using priority, then effective Speed, then a random tie-break.

        ``actions`` must contain the selected action priority for every living
        active Pokémon when resolving a turn.  Speed modifiers that affect
        ordering are calculated here, not by the player.
        """
        battlers = [p for p in self.active_p1 + self.active_p2 if not p.is_fainted()]
        actions = actions or {}
        random.shuffle(battlers)  # establishes an unbiased tie-break order

        def effective_speed(p):
            speed = p.get_modified_stat("spe")
            if getattr(p, "status", None) == "paralysis":
                speed //= 2
            side = 1 if p in self.active_p1 else 2
            if (side == 1 and self.state.tailwind_p1) or (side == 2 and self.state.tailwind_p2):
                speed *= 2
            if p.ability == "Chlorophyll" and self.state.weather == "sun":
                speed *= 2
            elif p.ability == "Swift Swim" and self.state.weather == "rain":
                speed *= 2
            elif p.ability == "Sand Rush" and self.state.weather == "sand":
                speed *= 2
            return speed

        def key(p):
            priority = actions.get(id(p), 0)
            return priority, effective_speed(p)

        # Python's stable sort preserves the shuffled order for exact ties.
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
        """Resolve one turn from explicit player-selected actions.

        A living active Pokémon MUST have a selection. The engine never chooses
        a move, target, or switch on the player's behalf.
        Supported move selection forms:
          Move / move-name
          (Move / move-name, target Pokémon)
        Switch selection forms:
          ("switch", replacement Pokémon)
        """
        if selections is None:
            raise ValueError("Turn selections are required; the engine will not choose actions automatically.")

        living = [p for p in self.active_p1 + self.active_p2 if not p.is_fainted()]

        def selected(pokemon):
            return selections.get(id(pokemon), selections.get(pokemon.species))

        def parse_choice(pokemon):
            choice = selected(pokemon)
            if choice is None:
                raise ValueError(f"No action selected for {pokemon.species}.")

            # Explicit Mega selection forms:
            #   {"mega": True, "move": "Protect", "target": target}
            #   ("mega", move_or_name, target)
            # Mega is a declaration attached to the player's chosen action;
            # the engine performs it before calculating this turn's move order.
            mega = False
            if isinstance(choice, dict):
                mega = bool(choice.get("mega", False))
                if str(choice.get("action", "")).lower() == "switch":
                    replacement = choice.get("replacement")
                    if replacement is None:
                        raise ValueError(f"Switch action for {pokemon.species} requires a replacement.")
                    return ("switch", replacement, None, mega)
                raw_move = choice.get("move")
                target = choice.get("target")
            elif isinstance(choice, tuple) and choice and str(choice[0]).lower() == "mega":
                mega = True
                if len(choice) < 2:
                    raise ValueError(f"Mega action for {pokemon.species} requires a move.")
                raw_move = choice[1]
                target = choice[2] if len(choice) > 2 else None
            else:
                if isinstance(choice, tuple) and choice and str(choice[0]).lower() == "switch":
                    if len(choice) != 2:
                        raise ValueError(f"Switch action for {pokemon.species} must be ('switch', replacement).")
                    return ("switch", choice[1], None, False)
                target = choice[1] if isinstance(choice, tuple) and len(choice) > 1 else None
                raw_move = choice[0] if isinstance(choice, tuple) else choice

            if isinstance(raw_move, str):
                raw_move = Move.from_database(raw_move)
            if not isinstance(raw_move, Move):
                raise ValueError(f"Invalid move selection for {pokemon.species}.")
            return ("move", raw_move, target, mega)

        parsed = {id(p): parse_choice(p) for p in living}
        actions = {}
        for p in living:
            kind, action, _, _mega = parsed[id(p)]
            actions[id(p)] = 6 if kind == "switch" else action.priority

        # Switches occur before attacks/status moves, ordered by switch
        # priority. Multiple switches are still simultaneous player choices.
        switchers = [p for p in living if parsed[id(p)][0] == "switch"]
        for p in switchers:
            replacement = parsed[id(p)][1]
            slot = (self.active_p1 if p in self.active_p1 else self.active_p2).index(p)
            if parsed[id(p)][3]:
                raise ValueError("Mega Evolution cannot be selected on a switching action.")
            if not self.switch_pokemon(1 if p in self.active_p1 else 2, slot, replacement):
                raise ValueError(f"Illegal switch selected for {p.species}.")
        if switchers:
            # Switching ends the action for that slot this turn.
            living = [p for p in self.active_p1 + self.active_p2 if not p.is_fainted()]
            for p in switchers:
                parsed.pop(id(p), None)
                actions.pop(id(p), None)

        # Mega Evolution happens before move-order calculation. This means the
        # Mega form's Speed and ability are active when the turn order is built.
        for pokemon in list(parsed_pokemon for parsed_pokemon in self.active_p1 + self.active_p2):
            if id(pokemon) not in parsed or pokemon.is_fainted():
                continue
            if parsed[id(pokemon)][3]:
                self.mega_evolve(pokemon)

        for pokemon in self.get_turn_order(actions):
            if pokemon.is_fainted() or id(pokemon) not in parsed:
                continue
            kind, move, target_choice, _mega = parsed[id(pokemon)]
            if getattr(pokemon, "_flinched", False):
                self.state.log(f"{pokemon.species} flinched and couldn't move!")
                pokemon._flinched = False
                continue
            if getattr(pokemon, "_active_turns", 0) == 0 and move.name == "Fake Out" and pokemon._moved_this_battle:
                self.state.log(f"{pokemon.species} can't use Fake Out after entering battle!")
                continue
            if not move.has_pp():
                raise ValueError(f"{move.name} has no PP left for {pokemon.species}.")
            if self.paralysis_check(pokemon) or self.sleep_check(pokemon):
                continue
            if not self.use_move(pokemon, move):
                continue
            if move.name != "Protect":
                pokemon._protect_streak = 0
            if move.name == "Protect":
                streak = getattr(pokemon, "_protect_streak", 0)
                chance = 1.0 / (3 ** streak)
                if random.random() >= chance:
                    pokemon._protected = False
                    pokemon._protect_streak = 0
                    self.state.log(f"{pokemon.species}'s Protect failed!")
                    continue
                pokemon._protected = True
                pokemon._protect_streak = streak + 1
                self.state.log(f"{pokemon.species} protected itself!")
                continue

            targets = [t for t in self._targets(pokemon, move, target_choice) if t is not None]
            if not targets:
                continue
            # Accuracy is checked per target for spread/redirected resolution.
            for target in targets:
                if target.is_fainted():
                    continue
                if not self.accuracy_check(pokemon, move, target):
                    self.state.log(f"{pokemon.species}'s {move.name} missed {target.species}!")
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
                if move.drain and damage:
                    pokemon.heal(max(1, int(damage * move.drain)))
                if move.recoil and damage:
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
            pokemon._moved_this_battle = True
            pokemon._last_move = move.name
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
        elif effect == "helping_hand": setattr(user, "_helping_hand", True)
        elif effect == "heal_half":
            user.heal(int(user.max_hp * 0.5))
            if target is not None and target is not user:
                target.heal(int(target.max_hp * 0.5))
        elif effect == "strength_sap":
            target.change_stage("atk", -1)
            user.heal(max(0, target.get_modified_stat("atk")))
        elif effect == "def_down": target.change_stage("def", -1)
        elif effect == "break_screens":
            side = 1 if target in self.active_p1 else 2
            for name in ("reflect", "light_screen", "aurora_veil"):
                setattr(self.state, f"{name}_p{side}", 0)
        elif effect == "poison": self._inflict_status(target, "poison")
        elif effect == "confusion": setattr(target, "_confused", True)

        # Canonical named moves whose database notes contain a rule.
        if move.name == "Sunny Day": self.state.weather, self.state.weather_turns = "sun", 5
        if move.name == "Tailwind": self._set_side_timer(user, "tailwind", 4)
        if move.name == "Haze":
            for p in self.active_p1+self.active_p2: p.stat_stages = {k:0 for k in p.stat_stages}
        if move.name == "Swords Dance": user.change_stage("atk", 2)
        if move.name == "Nasty Plot": user.change_stage("spa", 2)
        if move.name == "Toxic": self._inflict_status(target, "badly_poisoned")
        if move.name == "Will-O-Wisp": self._inflict_status(target, "burn")
        if move.name == "Thunder Wave": self._inflict_status(target, "paralysis")
        if move.name == "Lunar Blessing":
            if target is not None:
                target.heal(int(target.max_hp * 0.5))
                target.status = None
        if move.name == "Life Dew":
            for p in self.active_p1 + self.active_p2:
                if p in self.active_p1 if user in self.active_p1 else p in self.active_p2:
                    p.heal(int(p.max_hp * 0.25))
        if move.name == "Sleep Powder": self._inflict_status(target, "sleep")
        if move.name == "Yawn" and target.status is None: setattr(target, "_yawn", True)

    def _inflict_status(self, target, status):
        if target.status is not None: return False
        if status == "sleep": target.sleep_counter = random.randint(1,3)
        if status == "badly_poisoned": target.toxic_counter = 0
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
        elif ability == "Sand Stream": self.state.weather, self.state.weather_turns = "sand", 5
        elif ability == "Snow Warning": self.state.weather, self.state.weather_turns = "snow", 5
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
            elif pokemon.status == "badly_poisoned":
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
        active[active_slot]._protect_streak = 0
        active[active_slot]._protected = False
        active[active_slot] = new_pokemon
        new_pokemon._protect_streak = 0
        new_pokemon._protected = False
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
