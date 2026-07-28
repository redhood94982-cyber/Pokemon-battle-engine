"""
Pokemon Battle Engine
battle.py

Core battle controller.
"""

from .battle_state import BattleState


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