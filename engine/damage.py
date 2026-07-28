"""
Pokemon Battle Engine
damage.py

Damage calculation utilities.

This file implements the foundation of the
Generation 6+ damage formula.
"""

import math
from .type_chart import TYPE_CHART

FIXED_DAMAGE_ROLL = 0.925


def apply_stab(base_damage: int, stab: bool) -> int:
    """Apply Same Type Attack Bonus."""

    if not stab:
        return base_damage

    return math.floor(base_damage * 1.5)


def apply_type_effectiveness(
    base_damage: int,
    multiplier: float,
) -> int:
    """Apply type effectiveness."""

    return math.floor(base_damage * multiplier)


def apply_burn(
    base_damage: int,
    burned: bool,
    physical: bool,
) -> int:
    """Apply burn modifier."""

    if burned and physical:
        return math.floor(base_damage * 0.5)

    return base_damage

def get_type_multiplier(move_type: str, defender_types: list[str]) -> float:
    """
    Calculate total type effectiveness against one or two defender types.
    """
    multiplier = 1.0

    for defender_type in defender_types:
        multiplier *= TYPE_CHART.get(
            move_type,
            {}
        ).get(
            defender_type,
            1.0
        )

    return multiplier


def apply_spread(
    base_damage: int,
    spread_move: bool,
) -> int:
    """Apply spread move modifier."""

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
    Core damage calculation.

    Future updates will add:
    - Critical hits
    - Weather
    - Abilities
    - Items
    - Screens
    - Terrain
    """

    damage = math.floor((2 * level) / 5)
    damage += 2

    damage = math.floor(
        damage * power * attack / defense
    )

    damage = math.floor(damage / 50)

    damage += 2

    damage = math.floor(
        damage * FIXED_DAMAGE_ROLL
    )

    damage = apply_stab(
        damage,
        stab,
    )

    damage = apply_type_effectiveness(
    damage,
    get_type_multiplier(
        move_type,
        defender_types,
    ),
)

    damage = apply_burn(
        damage,
        burned,
        physical,
    )

    damage = apply_spread(
        damage,
        spread_move,
    )

    if damage < 1:
        damage = 1

    return damage