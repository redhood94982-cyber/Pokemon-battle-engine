"""
pokemon.py

Core Pokémon object used by the battle engine.

Temporary implementation:
- Stores all battle information.
- Stat calculations will be added next.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Pokemon:
    species: str
    level: int
    types: List[str]

    ability: str
    item: Optional[str]
    nature: str

    base_stats: Dict[str, int]
    ivs: Dict[str, int]
    evs: Dict[str, int]

    moves: List[str]

    current_hp: int = 0
    max_hp: int = 0

    status: Optional[str] = None
    toxic_counter: int = 0
    sleep_counter: int = 0

    stat_stages: Dict[str, int] = field(default_factory=lambda: {
        "atk": 0,
        "def": 0,
        "spa": 0,
        "spd": 0,
        "spe": 0,
        "accuracy": 0,
        "evasion": 0,
    })

    mega_evolved: bool = False

    def is_fainted(self) -> bool:
        return self.current_hp <= 0

    def heal(self, amount: int):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def damage(self, amount: int):
        self.current_hp = max(0, self.current_hp - amount)