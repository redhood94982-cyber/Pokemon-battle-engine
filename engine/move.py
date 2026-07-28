"""
Pokemon Battle Engine
move.py

Represents a Pokémon move.
"""

from dataclasses import dataclass


@dataclass
class Move:
    # Basic Info
    name: str
    move_type: str
    category: str

    # Battle Data
    power: int = 0
    accuracy: int = 100
    pp: int = 0
    max_pp: int = 0
    priority: int = 0

    # Move Properties
    target: str = "selected"
    makes_contact: bool = False
    sound_move: bool = False
    punch_move: bool = False
    bite_move: bool = False
    pulse_move: bool = False
    recoil: bool = False
    spread_move: bool = False
    protectable: bool = True

    # Status Moves
    causes_status: str | None = None

    def use_pp(self) -> bool:
        """Consumes 1 PP if possible."""

        if self.pp <= 0:
            return False

        self.pp -= 1
        return True

    def restore_pp(self):
        """Restores PP to maximum."""

        self.pp = self.max_pp

    def has_pp(self) -> bool:
        """Returns True if the move can still be used."""

        return self.pp > 0

    def is_status(self) -> bool:
        return self.category.lower() == "status"

    def is_physical(self) -> bool:
        return self.category.lower() == "physical"

    def is_special(self) -> bool:
        return self.category.lower() == "special"