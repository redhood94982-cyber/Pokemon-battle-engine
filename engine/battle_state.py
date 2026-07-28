"""
Pokemon Battle Engine
battle_state.py

Tracks the current state of a Pokémon battle.
Version: 0.1.0
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BattleState:
    """Stores all information about the current battle."""

    turn: int = 1

    weather: Optional[str] = None
    terrain: Optional[str] = None

    trick_room: bool = False
    tailwind_player1: bool = False
    tailwind_player2: bool = False

    reflect_player1: bool = False
    reflect_player2: bool = False

    light_screen_player1: bool = False
    light_screen_player2: bool = False

    aurora_veil_player1: bool = False
    aurora_veil_player2: bool = False

    player1_active: List[str] = field(default_factory=list)
    player2_active: List[str] = field(default_factory=list)

    battle_log: List[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        """Adds a message to the battle log."""
        self.battle_log.append(message)

    def next_turn(self) -> None:
        """Advance to the next turn."""
        self.turn += 1