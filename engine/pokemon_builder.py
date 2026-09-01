"""Factory for constructing battle-ready Pokémon from team-sheet inputs."""

import re

from .Database.species import SPECIES
from .Database.natures import NATURES
from .Database.move_database import MOVE_DATABASE
from .Database.items import ITEM_DATABASE

try:
    from .Database.abilities import ABILITIES
except ImportError:
    ABILITIES = None

from .pokemon_status_v3 import Pokemon


def _normalize_name(value):
    """Normalize human-readable names to the database naming convention."""
    if value is None:
        return None
    normalized = str(value).strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    return normalized.strip("_")


def _find_key(database, value):
    if value is None:
        return None

    wanted = _normalize_name(value)
    for key in database:
        if _normalize_name(key) == wanted:
            return key

    return None


def _validate_ivs(ivs):
    names = ("hp", "attack", "defense", "special_attack", "special_defense", "speed")
    if set(ivs) != set(names):
        raise ValueError("IVs must contain all six stat names.")
    for name, value in ivs.items():
        if not isinstance(value, int) or not 0 <= value <= 31:
            raise ValueError(f"IV for {name} must be an integer from 0 to 31.")


def _validate_evs(evs):
    names = ("hp", "attack", "defense", "special_attack", "special_defense", "speed")
    if set(evs) != set(names):
        raise ValueError("EVs must contain all six stat names.")
    total = 0
    for name, value in evs.items():
        if not isinstance(value, int) or not 0 <= value <= 252:
            raise ValueError(f"EV for {name} must be an integer from 0 to 252.")
        total += value
    if total > 510:
        raise ValueError(f"Total EVs cannot exceed 510 (got {total}).")


def build_pokemon(*, species, level, nature, ivs, evs, ability, item=None, moves=None):
    """Build an existing Pokemon object from canonical database inputs."""
    species_key = _find_key(SPECIES, species)
    if species_key is None:
        raise ValueError(f"Unknown species/form: {species}")

    if not isinstance(level, int) or level != 50:
        raise ValueError("Level must be exactly 50.")

    nature_key = _find_key(NATURES, nature)
    if nature_key is None:
        raise ValueError(f"Unknown nature: {nature}")

    _validate_ivs(ivs)
    _validate_evs(evs)

    item_key = _find_key(ITEM_DATABASE, item) if item else None
    if item and item_key is None:
        raise ValueError(f"Unknown item: {item}")

    if ABILITIES is not None:
        ability_key = _find_key(ABILITIES, ability)
        if ability and ability_key is None:
            raise ValueError(f"Unknown ability: {ability}")
    else:
        ability_key = ability

    if not isinstance(moves, (list, tuple)) or not 1 <= len(moves) <= 4:
        raise ValueError("A Pokémon must have between 1 and 4 moves.")

    move_keys = []
    for move in moves:
        move_key = _find_key(MOVE_DATABASE, move)
        if move_key is None:
            raise ValueError(f"Unknown move: {move}")
        move_keys.append(move_key)

    record = SPECIES[species_key]
    base_stats = record.get("base_stats")
    if not base_stats:
        raise ValueError(f"No base stats available for {species_key}.")

    types = record.get("types", [])
    return Pokemon(
        species=species_key,
        level=level,
        types=types,
        ability=ability_key,
        item=item_key,
        nature=nature_key,
        base_stats=base_stats,
        ivs=dict(ivs),
        evs=dict(evs),
        moves=move_keys,
    )


__all__ = ["build_pokemon"]
