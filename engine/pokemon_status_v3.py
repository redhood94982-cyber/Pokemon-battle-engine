"""Core Pokémon object. The database supplies canonical move/nature/species data."""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from .Database.natures import NATURES
from .Database.species import SPECIES
from .Database.abilities import ABILITIES
from .Database.types import TYPES
from .move import Move

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
    moves: List[object]
    current_hp: int = 0
    max_hp: int = 0
    status: Optional[str] = None
    toxic_counter: int = 0
    sleep_counter: int = 0
    stat_stages: Dict[str, int] = field(default_factory=lambda: {
        "atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0,
        "accuracy": 0, "evasion": 0,
    })
    mega_evolved: bool = False
    # Persistent Mega Evolution state. Mega Evolution is permanent for the battle,
    # including after switching out.
    original_species: Optional[str] = None
    mega_species: Optional[str] = None
    _active_turns: int = 0
    _moved_this_battle: bool = False
    _last_move: Optional[str] = None

    def __post_init__(self):
        if self.species not in SPECIES:
            raise KeyError(f"Species not found in database: {self.species}")
        if self.nature not in NATURES:
            raise KeyError(f"Nature not found in database: {self.nature}")
        if self.ability not in ABILITIES:
            raise KeyError(f"Ability not found in database: {self.ability}")
        if any(t not in TYPES for t in self.types):
            raise KeyError(f"Unknown Pokémon type in {self.species}: {self.types}")
        if self.original_species is None:
            self.original_species = self.species
        self.moves = [m if isinstance(m, Move) else Move.from_database(m) for m in self.moves]
        if len(self.moves) > 4:
            raise ValueError("A Pokémon may have at most 4 moves.")
        self.calculate_stats()

    @classmethod
    def from_database(cls, species: str, level: int, types: List[str],
                      ability: str, item: Optional[str], nature: str,
                      base_stats: Dict[str, int], ivs: Dict[str, int],
                      evs: Dict[str, int], moves: List[str]):
        """Explicit constructor for the current database schema."""
        return cls(species, level, types, ability, item, nature,
                   base_stats, ivs, evs, moves)

    def is_fainted(self) -> bool:
        return self.current_hp <= 0

    def heal(self, amount: int):
        self.current_hp = min(self.max_hp, self.current_hp + max(0, amount))

    def damage(self, amount: int):
        self.current_hp = max(0, self.current_hp - max(0, amount))

    def _calc_hp(self, base, iv, ev):
        return ((2 * base + iv + (ev // 4)) * self.level) // 100 + self.level + 10

    def _calc_other(self, base, iv, ev, nature):
        value = ((2 * base + iv + (ev // 4)) * self.level) // 100 + 5
        return int(value * nature)

    def _get(self, d, *keys):
        for k in keys:
            if k in d:
                return d[k]
        raise KeyError(keys[0])

    def calculate_stats(self):
        nature = NATURES[self.nature]
        self.max_hp = self._calc_hp(self._get(self.base_stats, "HP", "hp"),
                                    self._get(self.ivs, "HP", "hp"),
                                    self._get(self.evs, "HP", "hp"))
        self.attack = self._calc_other(self._get(self.base_stats, "Attack", "attack", "atk"),
                                       self._get(self.ivs, "Attack", "attack", "atk"),
                                       self._get(self.evs, "Attack", "attack", "atk"), nature["Attack"])
        self.defense = self._calc_other(self._get(self.base_stats, "Defense", "defense", "def"),
                                        self._get(self.ivs, "Defense", "defense", "def"),
                                        self._get(self.evs, "Defense", "defense", "def"), nature["Defense"])
        self.special_attack = self._calc_other(self._get(self.base_stats, "Special Attack", "special_attack", "sp_attack", "spa"),
                                               self._get(self.ivs, "Special Attack", "special_attack", "sp_attack", "spa"),
                                               self._get(self.evs, "Special Attack", "special_attack", "sp_attack", "spa"), nature["Special Attack"])
        self.special_defense = self._calc_other(self._get(self.base_stats, "Special Defense", "special_defense", "sp_defense", "spd"),
                                                self._get(self.ivs, "Special Defense", "special_defense", "sp_defense", "spd"),
                                                self._get(self.evs, "Special Defense", "special_defense", "sp_defense", "spd"), nature["Special Defense"])
        self.speed = self._calc_other(self._get(self.base_stats, "Speed", "speed", "spe"),
                                      self._get(self.ivs, "Speed", "speed", "spe"),
                                      self._get(self.evs, "Speed", "speed", "spe"), nature["Speed"])
        self.current_hp = self.max_hp

    def recalculate_stats_preserve_hp(self):
        """Recalculate stats after a form change without healing or resetting HP."""
        old_hp = self.current_hp
        self.calculate_stats()
        self.current_hp = min(old_hp, self.max_hp)

    def change_stage(self, stat, amount):
        self.stat_stages[stat] = max(-6, min(6, self.stat_stages.get(stat, 0) + amount))

    @staticmethod
    def stage_multiplier(stage):
        return (2 + stage) / 2 if stage >= 0 else 2 / (2 - stage)

    def get_modified_stat(self, stat):
        attr = {"atk": "attack", "def": "defense", "spa": "special_attack",
                "spd": "special_defense", "spe": "speed"}[stat]
        return int(getattr(self, attr) * self.stage_multiplier(self.stat_stages.get(stat, 0)))


# ---------------------------------------------------------------------------
# Gen 3+ stat calculation
# These functions intentionally preserve the required floor order.
# ---------------------------------------------------------------------------

def calculate_hp(base, iv, ev, level):
    """Calculate HP using the Gen 3+ formula."""
    return (((2 * base + iv + (ev // 4)) * level) // 100) + level + 10


def calculate_stat(base, iv, ev, level, nature_multiplier=1.0):
    """Calculate a non-HP stat using the Gen 3+ formula."""
    intermediate = ((2 * base + iv + (ev // 4)) * level) // 100
    return int((intermediate + 5) * nature_multiplier)


def calculate_level_stats(base_stats, ivs, evs, level, nature_multipliers=None):
    """Calculate all six stats from base stats, IVs, EVs, level, and nature."""
    nature_multipliers = nature_multipliers or {}
    hp = calculate_hp(
        base_stats["hp"],
        ivs["hp"],
        evs["hp"],
        level,
    )
    stats = {"hp": hp}
    for stat in ("attack", "defense", "special_attack", "special_defense", "speed"):
        stats[stat] = calculate_stat(
            base_stats[stat],
            ivs[stat],
            evs[stat],
            level,
            nature_multipliers.get(stat, 1.0),
        )
    return stats
