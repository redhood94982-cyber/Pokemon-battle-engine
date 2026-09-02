"""Battle damage calculation.

Implements the project's supplied damage formula and keeps the individual
modifiers explicit so battle mechanics can be added without changing the
core formula.
"""
import math
import random

from . import item_resolver
from .Database.type_chart import TYPE_CHART


def apply_random_roll(base_damage: int, rng=None) -> int:
    rng = rng or random
    return math.floor(base_damage * rng.randint(85, 100) / 100)


def apply_stab(base_damage: int, stab: bool, multiplier: float = 1.5) -> int:
    return math.floor(base_damage * multiplier) if stab else base_damage


def apply_type_effectiveness(base_damage: int, multiplier: float) -> int:
    return math.floor(base_damage * multiplier)


def apply_burn(base_damage: int, burned: bool, physical: bool) -> int:
    return math.floor(base_damage * 0.5) if burned and physical else base_damage


def apply_critical(base_damage: int, critical: bool) -> int:
    return math.floor(base_damage * 1.5) if critical else base_damage


def apply_spread(base_damage: int, spread_move: bool) -> int:
    return math.floor(base_damage * 0.75) if spread_move else base_damage


def get_type_multiplier(move_type: str, defender_types: list[str]) -> float:
    multiplier = 1.0
    row = TYPE_CHART.get(move_type, {})
    for defender_type in defender_types:
        multiplier *= row.get(defender_type, 1.0)
    return multiplier


def _stage_multiplier(stage: int) -> float:
    if stage >= 0:
        return (2 + stage) / 2
    return 2 / (2 - stage)


def _modified_stat(pokemon, stat: str, critical: bool = False,
                   ignore_positive: bool = False,
                   ignore_negative: bool = False) -> int:
    raw = pokemon.stats.get(stat, 0)
    stage = getattr(pokemon, "stat_stages", {}).get(stat, 0)

    # Critical hits ignore the attacker's negative stages and the defender's
    # positive stages. The caller handles which stat is which.
    if critical and ((ignore_negative and stage < 0) or
                     (ignore_positive and stage > 0)):
        stage = 0

    return max(1, math.floor(raw * _stage_multiplier(stage)))


def _side_of(battle_state, pokemon):
    if battle_state is None:
        return None
    return getattr(battle_state, "side_of", lambda p: None)(pokemon)


def _has_ally_with_ability(battle_state, defender, ability):
    if battle_state is None:
        return False
    side = _side_of(battle_state, defender)
    if side == 1:
        allies = getattr(battle_state, "active_p1", [])
    elif side == 2:
        allies = getattr(battle_state, "active_p2", [])
    else:
        # BattleState normally delegates side information to the controller.
        return False
    return any(
        p is not None and p is not defender and not getattr(p, "fainted", False)
        and getattr(p, "ability", "") == ability
        for p in allies
    )


def _other_modifier(attacker, defender, move, battle_state, multiplier):
    """Resolve the modifier group from the supplied formula."""
    modifier = 1.0
    weather = getattr(battle_state, "weather", None)

    # Screens. In doubles, Reflect/Light Screen/Aurora Veil reduce damage to
    # 2/3. Critical hits bypass these screens.
    if battle_state is not None and not multiplier == 0:
        side = _side_of(battle_state, defender)
        if side == 1:
            screen = (getattr(battle_state, "reflect_p1", 0)
                      if move.is_physical()
                      else getattr(battle_state, "light_screen_p1", 0))
            veil = getattr(battle_state, "aurora_veil_p1", 0)
        elif side == 2:
            screen = (getattr(battle_state, "reflect_p2", 0)
                      if move.is_physical()
                      else getattr(battle_state, "light_screen_p2", 0))
            veil = getattr(battle_state, "aurora_veil_p2", 0)
        else:
            screen = veil = 0
        if (screen or veil) and not getattr(battle_state, "_damage_is_critical", False):
            modifier *= 2 / 3

    # Defensive abilities.
    defender_ability = getattr(defender, "ability", "")
    if defender_ability in {"Multiscale", "Shadow Shield"}:
        if defender.current_hp == defender.max_hp:
            modifier *= 0.5
    if defender_ability in {"Filter", "Solid Rock", "Prism Armor"} and multiplier > 1:
        modifier *= 0.75
    if defender_ability == "Ice Scales" and move.is_special():
        modifier *= 0.5
    if defender_ability == "Fluffy":
        if move.makes_contact:
            modifier *= 0.5
        if move.move_type == "Fire":
            modifier *= 2.0
    if defender_ability == "Punk Rock" and getattr(move, "notes", ""):
        if "sound" in move.notes.lower():
            modifier *= 0.5

    # Friend Guard is supplied by an ally of the defender.
    if _has_ally_with_ability(battle_state, defender, "Friend Guard"):
        modifier *= 0.75

    # Tinted Lens doubles resisted damage.
    if getattr(attacker, "ability", "") == "Tinted Lens" and 0 < multiplier < 1:
        modifier *= 2.0

    # Held-item damage multipliers come from the item database. Do not invent
    # effects for items that are absent from the database.
    try:
        modifier *= float(item_resolver.damage_multiplier(attacker, move))
    except (KeyError, TypeError, ValueError):
        pass

    # Helping Hand is a battle-state effect set by the move resolver.
    if getattr(attacker, "_helping_hand", False):
        modifier *= 1.5

    return modifier


def calculate_damage(attacker, defender, move, battle_state=None,
                     critical: bool = False, rng=None) -> int:
    """Calculate one target's damage using the supplied project formula."""
    if move.power <= 0 or move.is_status():
        return 0

    physical = move.is_physical()

    # Critical hits use the appropriate unmodified stat when required.
    if physical:
        attack = _modified_stat(
            attacker, "atk", critical=critical, ignore_negative=True
        )
        defense = _modified_stat(
            defender, "def", critical=critical, ignore_positive=True
        )
    else:
        attack = _modified_stat(
            attacker, "spa", critical=critical, ignore_negative=True
        )
        defense = _modified_stat(
            defender, "spd", critical=critical, ignore_positive=True
        )

    # Item stat multipliers are part of the actual attacking/defending stat.
    try:
        if physical:
            attack = math.floor(attack * item_resolver.stat_multiplier(attacker, "atk"))
        else:
            attack = math.floor(attack * item_resolver.stat_multiplier(attacker, "spa"))
            defense = math.floor(defense * item_resolver.stat_multiplier(defender, "spd"))
    except (KeyError, TypeError, ValueError):
        pass

    defense = max(1, defense)

    # Supplied base formula:
    # (((2*Level/5 + 2) * Power * Attack/Defense) / 50) + 2
    damage = math.floor((2 * attacker.level) / 5) + 2
    damage = math.floor(damage * move.power * attack / defense)
    damage = math.floor(damage / 50) + 2

    # Move-specific power behavior.
    if move.name == "Hex" and getattr(defender, "status", None) is not None:
        damage = math.floor(damage * 2)

    # Technician boosts moves with power <= 60.
    if getattr(attacker, "ability", "") == "Technician" and move.power <= 60:
        damage = math.floor(damage * 1.5)

    # Low-HP type-boosting abilities.
    attacker_ability = getattr(attacker, "ability", "")
    if attacker_ability in {"Blaze", "Overgrow", "Torrent", "Swarm"}:
        if attacker.current_hp * 3 <= attacker.max_hp:
            boosted_type = {
                "Blaze": "Fire", "Overgrow": "Grass",
                "Torrent": "Water", "Swarm": "Bug"
            }[attacker_ability]
            if move.move_type == boosted_type:
                damage = math.floor(damage * 1.5)

    # Solar Power: Special Attack is effectively 1.5x in sun.
    if attacker_ability == "Solar Power" and weather == "sun" and move.is_special():
        damage = math.floor(damage * 1.5)

    # Weather modifier.
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

    # STAB, including Adaptability's 2x STAB.
    stab = move.move_type in getattr(attacker, "types", [])
    stab_multiplier = 2.0 if attacker_ability == "Adaptability" else 1.5
    damage = apply_stab(damage, stab, stab_multiplier)

    # Type immunity is absolute.
    type_multiplier = get_type_multiplier(move.move_type, defender.types)
    if type_multiplier == 0:
        return 0

    damage = apply_type_effectiveness(damage, type_multiplier)

    # Critical and spread are explicit parts of the supplied modifier chain.
    damage = apply_critical(damage, critical)
    damage = apply_spread(damage, getattr(move, "spread_move", False))

    # Burn only cuts physical damage from a burned attacker.
    damage = apply_burn(
        damage, getattr(attacker, "status", None) == "burn", physical
    )

    # Remaining modifier group.
    old_critical_flag = getattr(battle_state, "_damage_is_critical", False) if battle_state else False
    if battle_state is not None:
        battle_state._damage_is_critical = critical
    damage = math.floor(damage * _other_modifier(
        attacker, defender, move, battle_state, type_multiplier
    ))
    if battle_state is not None:
        battle_state._damage_is_critical = old_critical_flag

    # Pokémon damage cannot be below 1 after a non-immune damaging hit.
    return max(1, damage)


def apply_item_damage_modifier(attacker, move, damage):
    """Compatibility helper for callers that apply item damage separately."""
    return int(damage * item_resolver.damage_multiplier(attacker, move))
