"""Generic item resolver for the Pokémon Battle Engine.

The item database is the canonical source of item facts and numeric modifiers.
This module resolves those facts into battle-ready queries; it does not own
battle state or implement item effects itself.
"""

from dataclasses import dataclass
from typing import Any, Optional

from .Database.items import ITEM_DATABASE


def _name(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    return str(value).strip()


@dataclass(frozen=True)
class ItemResolver:
    """Read-only gateway from a held item to its database definition."""

    database: dict[str, dict[str, Any]]

    def get(self, item: Optional[str]) -> Optional[dict[str, Any]]:
        name = _name(item)
        if not name:
            return None
        record = self.database.get(name)
        if record is None:
            raise KeyError(f"Item not found in database: {name}")
        return record

    def has(self, item: Optional[str]) -> bool:
        return self.get(item) is not None

    def value(self, item: Optional[str], field: str, default: Any = None) -> Any:
        record = self.get(item)
        return default if record is None else record.get(field, default)

    def damage_multiplier(
        self,
        item: Optional[str],
        move_type: Optional[str] = None,
    ) -> float:
        multiplier = float(self.value(item, "damage_multiplier", 1.0))
        boosted_type = self.value(item, "boosted_type")
        if boosted_type and move_type and str(boosted_type).lower() != str(move_type).lower():
            return 1.0
        return multiplier

    def stat_multiplier(self, item: Optional[str], stat: str) -> float:
        stat = stat.lower()
        if stat == "spd":
            return float(self.value(item, "special_defense_multiplier", 1.0))
        if stat == "spa":
            return float(self.value(item, "special_attack_multiplier", 1.0))
        return 1.0

    def blocks_status_moves(self, item: Optional[str]) -> bool:
        return bool(self.value(item, "blocks_status_moves", False))

    def blocks_secondary_effects(self, item: Optional[str]) -> bool:
        return bool(self.value(item, "blocks_secondary_effects", False))

    def blocks_stat_drops(self, item: Optional[str]) -> bool:
        return bool(self.value(item, "blocks_opponent_stat_drops", False))

    def contact_damage_fraction(self, item: Optional[str]) -> float:
        return float(self.value(item, "contact_recoil_fraction", 0.0))

    def recoil_fraction(self, item: Optional[str]) -> float:
        return float(self.value(item, "recoil_fraction", 0.0))

    def healing_fraction(self, item: Optional[str]) -> float:
        return float(self.value(item, "heal_fraction", 0.0))

    def poison_healing_fraction(self, item: Optional[str]) -> float:
        return float(self.value(item, "poison_heal_fraction", 0.0))

    def non_poison_damage_fraction(self, item: Optional[str]) -> float:
        return float(self.value(item, "non_poison_damage_fraction", 0.0))

    def trigger(self, item: Optional[str]) -> Optional[str]:
        return self.value(item, "trigger")

    def is_consumable(self, item: Optional[str]) -> bool:
        return bool(self.value(item, "consumable", False))

    def requires_full_hp(self, item: Optional[str]) -> bool:
        return bool(self.value(item, "requires_full_hp", False))

    def survival_hp(self, item: Optional[str]) -> Optional[int]:
        value = self.value(item, "survive_at_hp")
        return int(value) if value is not None else None

    def weather_duration(self, item: Optional[str], weather: Optional[str]) -> Optional[int]:
        item_weather = self.value(item, "weather")
        if item_weather and weather and item_weather.lower() == weather.lower():
            value = self.value(item, "weather_duration")
            return int(value) if value is not None else None
        return None

    def screen_duration(self, item: Optional[str]) -> Optional[int]:
        value = self.value(item, "screen_duration")
        return int(value) if value is not None else None

    def boosted_type(self, item: Optional[str]) -> Optional[str]:
        return self.value(item, "boosted_type")


ITEM_RESOLVER = ItemResolver(ITEM_DATABASE)


__all__ = ["ItemResolver", "ITEM_RESOLVER"]
