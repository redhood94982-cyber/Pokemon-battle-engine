"""
Pokemon Battle Engine
damage.py

Damage calculation utilities.

This file implements the core Generation 6+ damage formula
foundation. Additional modifiers (abilities, items, weather,
screens, etc.) will be added in future commits.
"""

import math

FIXED_DAMAGE_ROLL = 0.925


def apply_stab(base_damage: int, stab: bool) -> int:
    """Apply Same Type Attack Bonus."""

    if not stab:
        return base_damage

    return math.floor(base_damage * 1.5)


def apply_type_effectiveness(base_damage: int, multiplier: float) -> int:
    """Apply type effectiveness."""

    return math.floor(base_damage * multiplier)


def apply_burn(base_damage: int,
               burned: bool,
               physical: bool) -> int:
    """Apply burn attack reduction."""

    if burned and physical:
        return math.floor(base_damage * 0.5)

    return base_damage


def apply_spread(base_damage: int,
                 spread_move: bool) -> int:
    """Apply doubles spread modifier."""

    if spread_move:
        return math.floor(base_damage * 0.75)

    return base_damage


def calculate_damage(
    level: int,
    power: int,
    attack: int,
    defense: int,
    stab: bool = False,
    effectiveness: float = 1.0,
    burned: bool = False,
    physical: bool = True,
    spread_move: bool = False,
) -> int:
    """
    Core cartridge damage calculation.

    This is the foundation and will be expanded with:
    - Weather
    - Critical Hits
    - Abilities
    - Items
    - Screens
    - Terrain
    - Multi-target modifiers
    """

    damage = math.floor((2 * level) / 5)
    damage += 2

    damage = math.floor(damage * power * attack / defense)

    damage = math.floor(damage / 50)

    damage += 2

    damage = math.floor(damage * FIXED_DAMAGE_ROLL)

    damage = apply_stab(damage, stab