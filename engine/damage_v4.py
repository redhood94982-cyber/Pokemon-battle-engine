from . import item_resolver
"""Database-backed Generation 6+ style damage calculation."""
import math
import random
from .Database.type_chart import TYPE_CHART

def apply_random_roll(base_damage: int) -> int:
    return math.floor(base_damage * random.randint(85, 100) / 100)

def apply_stab(base_damage: int, stab: bool) -> int:
    return math.floor(base_damage * 1.5) if stab else base_damage

def apply_type_effectiveness(base_damage: int, multiplier: float) -> int:
    return math.floor(base_damage * multiplier)

def apply_burn(base_damage: int, burned: bool, physical: bool) -> int:
    return math.floor(base_damage * 0.5) if burned and physical else base_damage

def get_type_multiplier(move_type: str, defender_types: list[str]) -> float:
    multiplier = 1.0
    row = TYPE_CHART.get(move_type, {})
    for defender_type in defender_types:
        multiplier *= row.get(defender_type, 1.0)
    return multiplier

def apply_critical(base_damage: int, critical: bool) -> int:
    return math.floor(base_damage * 1.5) if critical else base_damage

def apply_spread(base_damage: int, spread_move: bool) -> int:
    return math.floor(base_damage * 0.75) if spread_move else base_damage

def calculate_damage(attacker, defender, move, battle_state=None, critical: bool = False) -> int:
    if move.power <= 0 or move.is_status():
        return 0
    level = attacker.level
    physical = move.is_physical()
    attack = attacker.get_modified_stat("atk") if physical else attacker.get_modified_stat("spa")
    defense = defender.get_modified_stat("def") if physical else defender.get_modified_stat("spd")
    if defense <= 0:
        defense = 1

    damage = math.floor((2 * level) / 5) + 2
    damage = math.floor(damage * move.power * attack / defense)
    damage = math.floor(damage / 50) + 2

    # Weather and a few canonical ability effects are resolved from battle state.
    weather = getattr(battle_state, "weather", None)
    if weather == "rain":
        if move.move_type == "Water":
            damage = math.floor(damage * 1.5)
        elif move.move_type == "Fire":
            damage = math.floor(damage * 0.5)
    elif weather == "sun":
        if move.move_type == "Fire":
            damage = math.floor(damage * 1.5)
        elif move.move_type == "Water":
            damage = math.floor(damage * 0.5)

    ability = getattr(attacker, "ability", "")
    if ability == "Adaptability" and move.move_type in attacker.types:
        damage = math.floor(damage * 2 / 1.5)

    if ability in {"Blaze", "Overgrow", "Torrent", "Swarm"}:
        threshold = attacker.current_hp * 3 <= attacker.max_hp
        boosted_type = {"Blaze": "Fire", "Overgrow": "Grass",
                        "Torrent": "Water", "Swarm": "Bug"}[ability]
        if threshold and move.move_type == boosted_type:
            damage = math.floor(damage * 1.5)

    damage = apply_random_roll(damage)
    damage = apply_stab(damage, move.move_type in attacker.types)
    multiplier = get_type_multiplier(move.move_type, defender.types)

    defender_ability = getattr(defender, "ability", "")
    if defender_ability == "Filter" and multiplier > 1:
        damage = math.floor(damage * 0.75)
    if defender_ability == "Fluffy" and move.makes_contact:
        damage = math.floor(damage * 0.5)
    if defender_ability == "Fluffy" and move.move_type == "Fire":
        damage = math.floor(damage * 2)

    damage = apply_type_effectiveness(damage, multiplier)
    damage = apply_critical(damage, critical)
    damage = apply_burn(damage, getattr(attacker, "status", None) == "burn", physical)

    # Screens are side effects, not database facts, so BattleState owns them.
    if battle_state is not None and not critical:
        side = "p1" if getattr(battle_state, "side_of", lambda p: None)(defender) == 1 else "p2"
        screen = getattr(battle_state, f"reflect_{side}", 0) if physical else getattr(battle_state, f"light_screen_{side}", 0)
        veil = getattr(battle_state, f"aurora_veil_{side}", 0)
        if screen or veil:
            damage = math.floor(damage * 0.5)

    damage = apply_spread(damage, move.spread_move)
    return max(1, damage)


def apply_item_damage_modifier(attacker, move, damage):
    """Apply the held item's database-defined damage multiplier."""
    return int(damage * item_resolver.damage_multiplier(attacker, move))
