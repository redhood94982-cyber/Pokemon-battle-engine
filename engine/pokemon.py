"""
Pokemon Battle Engine
pokemon.py

Represents a single Pokémon in battle.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Pokemon:
    # Identity
    species: str
    level: int = 50
    nickname: Optional[str] = None

    # Typing
    type1: str = ""
    type2: Optional[str] = None

    # Battle Information
    ability: str = ""
    item: str = ""

    # HP
    max_hp: int = 0
    current_hp: int = 0

    # Stats
    attack: int = 0
    defense: int = 0
    special_attack: int = 0
    special_defense: int = 0
    speed: int = 0

    # Status
    status: Optional[str] = None
    sleep_turns: int = 0
    toxic_counter: int = 0

    # Moves
    moves: List[str] = field(default_factory=list)

    # PP
    pp: Dict[str, int] = field(default_factory=dict)

    # Stat stages
    stat_stages: Dict[str, int] = field(default_factory=lambda: {
        "atk": 0,
        "def": 0,
        "spa": 0,
        "spd": 0,
        "spe": 0,
        "acc": 0,
        "eva": 0,
    })

    # Volatile conditions
    protected: bool = False
    flinched: bool = False
    taunted: bool = False
    confused: bool = False
    substitute_hp: int = 0

    # Battle flags
    fainted: bool = False

    def take_damage(self, damage: int):
        self.current_hp = max(0, self.current_hp - damage)

        if self.current_hp == 0:
            self.fainted = True

   