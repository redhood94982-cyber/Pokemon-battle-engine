"""
Pokemon Battle Engine
battle.py

Core battle controller.
"""
import random

CRITICAL_HIT_CHANCE = 24

from .battle_state import BattleState
from .damage import calculate_damage
from .move import Move

class Battle:
    """
    Main battle controller.

    This class will eventually control:
    - Battle setup
    - Turn order
    - Move execution
    - Switching
    - Weather
    - Terrain
    - End-of-turn effects
    - Win/Loss conditions
    """

    def __init__(self):
        self.state = BattleState()

        self.player1_team = []
        self.player2_team = []

        self.active_p1 = []
        self.active_p2 = []

        self.winner = None

        self.state.log("Battle initialized.")

    def accuracy_check(self, move) -> bool:
      """
      Return True if the move hits.
      """

      if move.accuracy >= 100:
         return True

      roll = random.randint(1, 100)

      return roll <= move.accuracy

    def critical_hit(self) -> bool:
        """
        Return True if the attack is a critical hit.
        """
        return random.randint(1, CRITICAL_HIT_CHANCE) == 1
 
    def register_teams(self, player1_team, player2_team):
      """
      Give each player their team.
      """

      if len(player1_team) != 6:
            raise ValueError("Player 1 must have exactly 6 Pokémon.")

        if len(player2_team) != 6:
           raise ValueError("Player 2 must have exactly 6 Pokémon.")

        self.player1_team = player1_team
        self.player2_team = player2_team

        self.state.log("Teams registered.")

    def start_battle(self):
        """
        Send the first two Pokémon onto the field.
        """

        self.active_p1 = [
            self.player1_team[0],
            self.player1_team[1],
        ]

        self.active_p2 = [
            self.player2_team[0],
            self.player2_team[1],
        ]

        self.state.log("Battle started.")

        self.state.log(
            f"P1 sent out "
            f"{self.active_p1[0].species} and "
            f"{self.active_p1[1].species}."
        )

        self.state.log(
            f"P2 sent out "
            f"{self.active_p2[0].species} and "
            f"{self.active_p2[1].species}."
        )
    def get_turn_order(self):
        """
        Returns all active Pokémon sorted by Speed.
        Fastest Pokémon goes first.
        """

        battlers = (
            self.active_p1 +
            self.active_p2
        )

        battlers.sort(
            key=lambda pokemon: pokemon.speed,
            reverse=True,
        )

        return battlers

    def begin_turn(self):
        """
        Start a new turn.
        """

        self.state.log(
            f"Turn {self.state.turn}"
        )

        turn_order = self.get_turn_order()

        self.state.log(
            "Turn order:"
        )

        for pokemon in turn_order:
        self.state.log(
            f" - {pokemon.species}"
        )
    
    def perform_turn(self):
    """
    Make each Pokémon act in Speed order.
    """

    turn_order = self.get_turn_order()

    for pokemon in turn_order:

        if pokemon.current_hp <= 0:
            continue

        move = pokemon.moves[0]

        if move is None:
            continue

        self.use_move(
            pokemon,
            move,
        )

        target = self.active_p2[0]

        if target.current_hp <= 0:
            continue

        self.state.log(
            f"{target.species} was targeted."
        )
        if not self.accuracy_check(move):
           self.state.log(
              f"{pokemon.species}'s attack missed!"
    )
    continue

        damage = calculate_damage(
            pokemon,
            target,
            move,
        )

        target.current_hp -= damage

        if target.current_hp < 0:
            target.current_hp = 0
        elif target.current_hp > target.hp:
            target.current_hp = target.hp

        self.state.log(
            f"{target.species} took {damage} damage."
        )

        if target.current_hp == 0:
            self.state.log(
                f"{target.species} fainted!"
            )
            continue
    def use_move(self, pokemon, move):
        """
        Have a Pokémon use a move.
        """

        self.state.log(
            f"{pokemon.species} used {move.name}!"
        )

        return move