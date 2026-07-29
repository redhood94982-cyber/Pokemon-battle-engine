"""
pokemon.py

Core Pokémon object used by the battle engine.

Temporary implementation:
- Stores all battle information.
- Stat calculations will be added next.
"""

from dataclasses import dataclass
from .Database.natures import NATURES, field
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

def _calc_hp(base, iv, ev, level):
    return ((2*base + iv + (ev//4))*level)//100 + level + 10

def _calc_other(base, iv, ev, level, nature):
    value=((2*base+iv+(ev//4))*level)//100+5
    return int(value*nature)

def calculate_stats(self):
    nature=NATURES[self.nature]
    self.hp=_calc_hp(self.base_stats["HP"],self.ivs["HP"],self.evs["HP"],self.level)
    self.attack=_calc_other(self.base_stats["Attack"],self.ivs["Attack"],self.evs["Attack"],self.level,nature["Attack"])
    self.defense=_calc_other(self.base_stats["Defense"],self.ivs["Defense"],self.evs["Defense"],self.level,nature["Defense"])
    self.special_attack=_calc_other(self.base_stats["Special Attack"],self.ivs["Special Attack"],self.evs["Special Attack"],self.level,nature["Special Attack"])
    self.special_defense=_calc_other(self.base_stats["Special Defense"],self.ivs["Special Defense"],self.evs["Special Defense"],self.level,nature["Special Defense"])
    self.speed=_calc_other(self.base_stats["Speed"],self.ivs["Speed"],self.evs["Speed"],self.level,nature["Speed"])
    self.current_hp=self.hp
