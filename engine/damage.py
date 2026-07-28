"""
Pokemon Battle Engine
damage.py

Core damage calculation functions.

This is the foundation of the cartridge damage engine.
Additional modifiers (abilities, items, weather, etc.)
will be added in future commits.
"""

import math


def stab_modifier(move_type: str, attacker_types: list[str]) -> float:
    """Returns the STAB multiplier."""

    if move_type in attacker_types:
        return 1.5

    return 1.0


def type_modifier(modifiers: list[float]) -> float:
    """Multiplies together all type effectiveness values."""

    result = 1.0

    for value in modifiers:
        result *= value

    return result


def burn_modifier(is_burned: bool, physical_move: bool) -> float:
    """Physical attacks are halved while burned."""

    if is_burned and physical_move:
        return 0.5

    return 1.0


def spread_modifier(is_spread_move: bool) -> float:
    """Damage modifier for spread moves."""

    if is_spread_move:
        return 0.75

    return 1.0


def calculate_damage(
    level: int,
    power: int,
    attack: int,
    defense: int,
    stab: float,
    effectiveness: float,
    burn: float,
    spread: float,
    other: float = 1.0,
    damage_roll: float = 0.925,
) -> int:
    """
    Core Pokémon damage formula.

    This version is intentionally simple.
    Future commits will add exact cartridge rounding,
    critical hits, weather, abilities, items,
    screens, Parental Bond, and every remaining modifier.
    """

    base = math.floor((2 * level) / 5)
    base += 2

    base = math.floor(base * power * attack / defense)

    base = math.floor(base / 50)

    base += 2

    modifier = (
        stab
        * effectiveness
        * burn
        * spread
        * other
        * damage_roll
    )

    damage = math.floor(base * modifier)

    if damage < 1:
        damage = 1

    return damage