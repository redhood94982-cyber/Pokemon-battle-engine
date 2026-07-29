"""
Pokemon Battle Engine
battle.py

Core battle controller.
"""
import random

from .battle_state import BattleState
from .damage import calculate_damage

CRITICAL_HIT_CHANCE = 24


class Battle:
    """Main battle controller."""

    def __init__(self):
        self.state = BattleState()
        self.player1_team = []
        self.player2_team = []
        self.active_p1 = []
        self.active_p2 = []
        self.winner = None
        self.state.log("Battle initialized.")

    def accuracy_check(self, move) -> bool:
        if move.accuracy >= 100:
            return True
        return random.randint(1, 100) <= move.accuracy

    def critical_hit(self) -> bool:
        return random.randint(1, CRITICAL_HIT_CHANCE) == 1

    def paralysis_check(self, pokemon) -> bool:
        """Return True if paralysis prevents movement."""
        if getattr(pokemon, "status", None) != "paralysis":
            return False
        if random.randint(1, 4) == 1:
            self.state.log(f"{pokemon.species} is fully paralyzed! It can't move!")
            return True
        return False


    def sleep_check(self, pokemon) -> bool:
        """Return True if sleep prevents movement."""
        if getattr(pokemon, "status", None) != "sleep":
            return False
        if pokemon.sleep_counter <= 0:
            pokemon.status = None
            self.state.log(f"{pokemon.species} woke up!")
            return False
        self.state.log(f"{pokemon.species} is fast asleep.")
        pokemon.sleep_counter -= 1
        return True


    def apply_sleep(self, pokemon) -> bool:
        """Inflict sleep with a random 1-3 turn duration."""
        if getattr(pokemon, "status", None) is not None:
            return False
        pokemon.status = "sleep"
        pokemon.sleep_counter = random.randint(1, 3)
        self.state.log(f"{pokemon.species} fell asleep!")
        return True

    def register_teams(self, player1_team, player2_team):
        if len(player1_team) != 6:
            raise ValueError("Player 1 must have exactly 6 Pokémon.")
        if len(player2_team) != 6:
            raise ValueError("Player 2 must have exactly 6 Pokémon.")
        self.player1_team = player1_team
        self.player2_team = player2_team
        self.state.log("Teams registered.")

    def start_battle(self):
        self.active_p1=[self.player1_team[0],self.player1_team[1]]
        self.active_p2=[self.player2_team[0],self.player2_team[1]]
        self.state.log("Battle started.")
        self.state.log(f"Player 1 sent out {self.active_p1[0].species} and {self.active_p1[1].species}.")
        self.state.log(f"Player 2 sent out {self.active_p2[0].species} and {self.active_p2[1].species}.")

    def get_turn_order(self):
        battlers=[p for p in (self.active_p1+self.active_p2) if p.current_hp>0]
        random.shuffle(battlers)
        battlers.sort(key=lambda p:p.speed, reverse=True)
        return battlers

    def begin_turn(self):
        self.state.turn+=1
        self.state.last_damage=0
        self.state.last_target=None
        self.state.last_move=None
        self.state.log(f"--- Turn {self.state.turn} ---")
        order=self.get_turn_order()
        self.state.log("Turn order: " + ", ".join(p.species for p in order))
        return order

    def get_active_team(self, pokemon):
        """Return the active team containing the given Pokémon."""
        return self.active_p1 if pokemon in self.active_p1 else self.active_p2

    def get_target(self, attacker):
        opponents=self.active_p2 if attacker in self.active_p1 else self.active_p1
        for target in opponents:
            if target.current_hp>0:
                return target
        return None

    def perform_turn(self):
        for pokemon in self.get_turn_order():
            if pokemon.current_hp<=0:
                continue
            if not pokemon.moves:
                self.state.log(f"{pokemon.species} has no moves available.")
                continue
            move=next((m for m in pokemon.moves if getattr(m,'pp',1)!=0), None)
            if move is None:
                self.state.log(f"{pokemon.species} has no PP remaining.")
                continue
            if self.paralysis_check(pokemon):
                continue
            if self.sleep_check(pokemon):
                continue
            target=self.get_target(pokemon)
            if target is None:
                self.state.log(f"{pokemon.species} has no valid target.")
                continue
            self.use_move(pokemon,move)
            if not self.accuracy_check(move):
                self.state.log(f"{pokemon.species}'s {move.name} missed {target.species}!")
                continue
            crit=self.critical_hit()
            damage=calculate_damage(
                pokemon,target,move,
                stab=move.move_type in pokemon.types,
                defender_types=target.types,
                burned=pokemon.status=="burn",
                physical=move.category=="Physical",
                critical=crit,
            )
            target.current_hp=max(0,target.current_hp-damage)
            if crit:
                self.state.log("A critical hit!")
            self.state.log(f"{target.species} took {damage} damage! ({target.current_hp}/{target.max_hp} HP remaining)")
            self.state.last_damage=damage
            self.state.last_target=target
            if target.current_hp==0:
                self.state.log(f"{target.species} fainted!")
                winner=self.check_win_condition()
                if winner:
                    self.state.log(f"Battle over! Winner: {winner}")
                    return winner
        return None

    def use_move(self,pokemon,move):
        if pokemon.current_hp<=0 or move is None:
            return
        self.state.log(f"{pokemon.species} used {move.name}!")
        self.state.last_move=move.name
        if hasattr(move,'pp'):
            if move.pp<=0:
                self.state.log(f'{move.name} has no PP left!')
                return
            move.pp-=1

    def check_win_condition(self):
        p1_alive=any(p.current_hp>0 for p in self.player1_team)
        p2_alive=any(p.current_hp>0 for p in self.player2_team)
        if not p1_alive and not p2_alive:
            return "draw"
        if not p1_alive:
            return "player2"
        if not p2_alive:
            return "player1"
        return None

    def end_turn(self):
        for pokemon in self.player1_team+self.player2_team:
            if pokemon.current_hp<=0:
                continue
            if pokemon.status=="burn":
                damage=max(1,pokemon.max_hp//16)
                pokemon.current_hp=max(0,pokemon.current_hp-damage)
                self.state.log(f"{pokemon.species} is hurt by its burn! (-{damage} HP)")
                if pokemon.current_hp==0:
                    self.state.log(f"{pokemon.species} fainted from its burn!")

            elif pokemon.status=="poison":
                damage=max(1,pokemon.max_hp//8)
                pokemon.current_hp=max(0,pokemon.current_hp-damage)
                self.state.log(f"{pokemon.species} is hurt by poison! (-{damage} HP)")
                if pokemon.current_hp==0:
                    self.state.log(f"{pokemon.species} fainted from poison!")

            elif pokemon.status=="toxic":
                pokemon.toxic_counter=max(1,pokemon.toxic_counter+1)
                damage=max(1,(pokemon.max_hp*pokemon.toxic_counter)//16)
                pokemon.current_hp=max(0,pokemon.current_hp-damage)
                self.state.log(f"{pokemon.species} is badly poisoned! (-{damage} HP)")
                if pokemon.current_hp==0:
                    self.state.log(f"{pokemon.species} fainted from poison!")
        winner=self.check_win_condition()
        if winner:
            self.state.log(f"Battle over! Winner: {winner}")
        return winner

    def switch_pokemon(self,team,active_slot,new_pokemon):
        active=self.active_p1 if team==1 else self.active_p2
        reserve=self.player1_team if team==1 else self.player2_team
        if new_pokemon not in reserve or new_pokemon.current_hp<=0:
            self.state.log("Switch failed.")
            return False
        if active_slot<0 or active_slot>=len(active):
            self.state.log("Invalid active slot.")
            return False
        if active[active_slot] is new_pokemon:
            self.state.log(f"{new_pokemon.species} is already active.")
            return False
        self.state.log(f"{active[active_slot].species}, come back!")
        active[active_slot]=new_pokemon
        self.state.log(f"Go, {new_pokemon.species}!")
        return True
