"""
Pokemon Battle Engine
pokemon.py

Represents a single Pokémon in battle.
This file will grow over time as new mechanics are added.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Pokemon:
    # -------------------------
    # Identity
    # -------------------------

    species: str
    level: int = 50
    nickname: Optional[str] = None

    # -------------------------
    # Battle Data
    # -------------------------

    ability: str = ""
    item: str = ""

    # -------------------------
    # Stats
    # -------------------------

    max_hp: int = 0
    current_hp: int = 0

    attack: int = 0
    defense: int = 0
    special_attack: int = 0
    special_defense: int = 0
    speed: int = 0

    # -------------------------
    # Status
    # -------------------------

    status: Optional[str] = None

    # -------------------------
    # Moves
    # -------------------------

    moves: List[str] = field(default_factory=list)

    # -------------------------
    # Stat Stages
    # -------------------------

    stat_stages: Dict[str, int] = field(default_factory=lambda: {
        "atk": 0,
        "def": 0,
        "spa": 0,
        "spd": 0,
        "spe": 0,
        "acc": 0,
        "eva": 0,
    })

    # -------------------------
    # Battle Flags
    # -------------------------

    fainted: bool = False
    protected: bool = False
    flinched: bool = False

    # -------------------------
    # Methods
    # -------------------------

    def take_damage(self, amount: int):
        self.current_hp = max(0, self.current_hp - amount)

        if self.current_hp == 0:
            self.fainted = True

    def heal(self, amount: int):
        self.current_hp = min(
            self.max_hp,
            self.current_hp + amount
        )

    def is_fainted(self) -> bool:
        return self.fainted

    def set_status(self, status: str):
        self.status = status

    def clear_status(self):
        self.status = None

    def hp_percent(self) -> float:
        if self.max_hp == 0:
            return 0.0

        return (self.current_hp / self.max_hp) * 100