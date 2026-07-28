"""
Pokemon Battle Engine
battle_state.py

Core battle state.
Phase 1
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class BattleState:
    # -------------------------
    # Battle Info
    # -------------------------

    turn: int = 1

    weather: Optional[str] = None
    terrain: Optional[str] = None

    trick_room: bool = False
    trick_room_turns: int = 0

    # -------------------------
    # Player 1 Field
    # -------------------------

    tailwind_p1: bool = False
    tailwind_turns_p1: int = 0

    reflect_p1: bool = False
    reflect_turns_p1: int = 0

    light_screen_p1: bool = False
    light_screen_turns_p1: int = 0

    aurora_veil_p1: bool = False
    aurora_veil_turns_p1: int = 0

    # -------------------------
    # Player 2 Field
    # -------------------------

    tailwind_p2: bool = False
    tailwind_turns_p2: int = 0

    reflect_p2: bool = False
    reflect_turns_p2: int = 0

    light_screen_p2: bool = False
    light_screen_turns_p2: int = 0

    aurora_veil_p2: bool = False
    aurora_veil_turns_p2: int = 0

    # -------------------------
    # Active Pokémon
    # -------------------------

    player1_active: List[str] = field(default_factory=list)
    player2_active: List[str] = field(default_factory=list)

    # -------------------------
    # Teams
    # -------------------------

    player1_team: List[str] = field(default_factory=list)
    player2_team: List[str] = field(default_factory=list)

    # -------------------------
    # HP Tracking
    # -------------------------

    hp: Dict[str, int] = field(default_factory=dict)
    max_hp: Dict[str, int] = field(default_factory=dict)

    # -------------------------
    # Status
    # -------------------------

    status: Dict[str, Optional[str]] = field(default_factory=dict)

    toxic_counter: Dict[str, int] = field(default_factory=dict)

    sleep_turns: Dict[str, int] = field(default_factory=dict)

    # -------------------------
    # Stat Stages
    # -------------------------

    stat_stages: Dict[str, Dict[str, int]] = field(default_factory=dict)

    # -------------------------
    # Battle