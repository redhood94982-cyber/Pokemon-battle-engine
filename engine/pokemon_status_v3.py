"""
pokemon.py

Core Pokémon object used by the battle engine.

Temporary implementation:
- Stores all battle information.
- Stat calculations will be added next.
"""

from dataclasses import dataclass, field
from .Database.natures import NATURES
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

    def __post_init__(self):
        self.calculate_stats()

    def is_fainted(self) -> bool:
        return self.current_hp <= 0

    def heal(self, amount: int):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def damage(self, amount: int):
        self.current_hp = max(0, self.current_hp - amount)

    def _calc_hp(self, base, iv, ev):
        return ((2*base + iv + (ev//4))*self.level)//100 + self.level + 10

    def _calc_other(self, base, iv, ev, nature):
        value=((2*base+iv+(ev//4))*self.level)//100+5
        return int(value*nature)

    def _get(self, d, *keys):
        for k in keys:
            if k in d:
                return d[k]
        raise KeyError(keys[0])

    def calculate_stats(self):
        nature=NATURES[self.nature]
        self.max_hp=self._calc_hp(self._get(self.base_stats,"HP","hp"),self._get(self.ivs,"HP","hp"),self._get(self.evs,"HP","hp"))
        self.attack=self._calc_other(self._get(self.base_stats,"Attack","attack"),self._get(self.ivs,"Attack","attack"),self._get(self.evs,"Attack","attack"),nature["Attack"])
        self.defense=self._calc_other(self._get(self.base_stats,"Defense","defense"),self._get(self.ivs,"Defense","defense"),self._get(self.evs,"Defense","defense"),nature["Defense"])
        self.special_attack=self._calc_other(self._get(self.base_stats,"Special Attack","special_attack","sp_attack"),self._get(self.ivs,"Special Attack","special_attack","sp_attack"),self._get(self.evs,"Special Attack","special_attack","sp_attack"),nature["Special Attack"])
        self.special_defense=self._calc_other(self._get(self.base_stats,"Special Defense","special_defense","sp_defense"),self._get(self.ivs,"Special Defense","special_defense","sp_defense"),self._get(self.evs,"Special Defense","special_defense","sp_defense"),nature["Special Defense"])
        self.speed=self._calc_other(self._get(self.base_stats,"Speed","speed"),self._get(self.ivs,"Speed","speed"),self._get(self.evs,"Speed","speed"),nature["Speed"])
        self.current_hp=self.max_hp

    def change_stage(self, stat, amount):
        self.stat_stages[stat]=max(-6,min(6,self.stat_stages.get(stat,0)+amount))

    def get_stage_multiplier(self, stage):
        return (2+stage)/2 if stage>=0 else 2/(2-stage)

    def get_modified_stat(self, stat):
        attr={"atk":"attack","def":"defense","spa":"special_attack","spd":"special_defense","spe":"speed"}[stat]
        return int(getattr(self,attr)*self.get_stage_multiplier(self.stat_stages[stat]))
