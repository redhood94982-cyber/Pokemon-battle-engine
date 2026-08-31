"""Move model and database-backed construction for the Pokémon Battle Engine."""
from dataclasses import dataclass
from .Database.move_database import MOVE_DATABASE

def _key(value: str) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")

@dataclass
class Move:
    name: str
    move_type: str
    category: str
    power: int = 0
    accuracy: int = 100
    pp: int = 0
    max_pp: int = 0
    priority: int = 0
    target: str = "selected"
    makes_contact: bool = False
    protectable: bool = True
    spread_move: bool = False
    stat_changes: dict | None = None
    status_effect: str | None = None
    effect_chance: int = 100
    drain: float = 0.0
    recoil: float = 0.0
    healing: float = 0.0
    secondary_effect: str | None = None
    notes: str = ""

    @classmethod
    def from_database(cls, name: str) -> "Move":
        record = MOVE_DATABASE.get(_key(name))
        if record is None:
            raise KeyError(f"Move not found in database: {name}")
        notes = record.get("notes", "")
        recoil = 1/3 if "1/3 recoil" in notes.lower() else 0.0
        return cls(
            name=record["name"],
            move_type=record.get("type", "Normal"),
            category=record.get("category", "Status"),
            power=record.get("power", 0),
            accuracy=record.get("accuracy", 100),
            pp=record.get("pp", 0),
            max_pp=record.get("max_pp", record.get("pp", 0)),
            priority=record.get("priority", 0),
            target=record.get("target", "selected"),
            makes_contact=record.get("makes_contact", False),
            protectable=record.get("protectable", True),
            spread_move=record.get("spread_move", False),
            stat_changes=record.get("stat_changes") or {},
            status_effect=record.get("status_inflicted"),
            effect_chance=record.get("effect_chance", 100),
            recoil=record.get("recoil", recoil),
            secondary_effect=record.get("secondary_effect"),
            notes=record.get("notes", ""),
        )

    def has_pp(self) -> bool:
        return self.pp > 0

    def use_pp(self) -> bool:
        if self.pp <= 0:
            return False
        self.pp -= 1
        return True

    def restore_pp(self):
        self.pp = self.max_pp

    def is_status(self) -> bool:
        return self.category.lower() == "status"

    def is_physical(self) -> bool:
        return self.category.lower() == "physical"

    def is_special(self) -> bool:
        return self.category.lower() == "special"
