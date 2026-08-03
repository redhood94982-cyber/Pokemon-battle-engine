from .debug import debug_damage, debug_accuracy, debug_secondary
"""
Pokemon Battle Engine
damage.py

Damage calculation utilities.

This file implements the foundation of the
Generation 6+ damage formula.
"""

import math
import random
from .Database.type_chart import TYPE_CHART

def apply_random_roll(base_damage: int) -> int:
    """Apply the standard 85–100% damage roll."""
    roll = random.randint(85, 100)
    return math.floor(base_damage * roll / 100)


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
        multiplier *= TYPE_CHART.get(move_type, {}).get(defender_type, 1.0)

    return multiplier

def apply_critical(
    base_damage: int,
    critical: bool,
) -> int:
    """Apply critical hit modifier."""

    if critical:
        return math.floor(base_damage * 1.5)

    return base_damage

def apply_spread(
    base_damage: int,
    spread_move: bool,
) -> int:
    """Apply spread move modifier."""

    if spread_move:
        return math.floor(base_damage * 0.75)

    return base_damage


def calculate_damage(
    attacker,
    defender,
    move,
    battle_state=None,
    critical: bool=False,
) -> int:
    """
    Core damage calculation.
    """

    level=attacker.level
    power=move.power
    move_type=move.move_type
    defender_types=defender.types
    physical = move.category.lower() == "physical"

    if physical:
        attack = attacker.attack
        defense = defender.defense
    else:
        attack = attacker.special_attack
        defense = defender.special_defense

    stab = move_type in attacker.types
    burned = attacker.status == "burn"
    spread_move = getattr(move, "spread_move", False)

    damage=math.floor((2*level)/5)+2
    if defense<=0:
        raise ValueError("Defense must be greater than zero.")
    damage=math.floor(damage*power*attack/defense)
    damage=math.floor(damage/50)+2
    damage=apply_random_roll(damage)
    damage=apply_stab(damage,stab)
    damage=apply_type_effectiveness(damage,get_type_multiplier(move_type,defender_types))
    damage=apply_critical(damage,critical)
    damage=apply_burn(damage,burned,physical)
    damage=apply_spread(damage,spread_move)
    if damage<1:
        damage=1
    return damage