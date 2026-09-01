"""Canonical held-item registry for the Pokémon Battle Engine.

Names are intentionally the only populated field in this first pass.
Mechanical behavior will be added later; the database remains the
canonical source of truth for item definitions.
"""

ITEM_DATABASE = {'Assault Vest': {'name': 'Assault Vest'}, 'Black Sludge': {'name': 'Black Sludge'}, 'Booster Energy': {'name': 'Booster Energy'}, 'Charcoal': {'name': 'Charcoal', 'description': "An item to be held by a Pokémon. It's a combustible fuel that boosts the power of the holder's Fire-type moves."}, 'Choice Specs': {'name': 'Choice Specs'}, 'Clear Amulet': {'name': 'Clear Amulet'}, 'Covert Cloak': {'name': 'Covert Cloak'}, 'Damp Rock': {'name': 'Damp Rock'}, 'Focus Sash': {'name': 'Focus Sash'}, 'Flame Orb': {'name': 'Flame Orb'}, 'Heat Rock': {'name': 'Heat Rock'}, 'Houndoomite': {'name': 'Houndoomite'}, 'Leftovers': {'name': 'Leftovers'}, 'Light Clay': {'name': 'Light Clay'}, 'Lucarionite': {'name': 'Lucarionite'}, 'Mental Herb': {'name': 'Mental Herb'}, 'Mystic Water': {'name': 'Mystic Water'}, 'Power Herb': {'name': 'Power Herb'}, 'Psychic Seed': {'name': 'Psychic Seed'}, 'Red Orb': {'name': 'Red Orb'}, 'Rocky Helmet': {'name': 'Rocky Helmet'}, 'Safety Goggles': {'name': 'Safety Goggles'}, 'Sitrus Berry': {'name': 'Sitrus Berry'}, 'Swampertite': {'name': 'Swampertite'}, 'Tyranitarite': {'name': 'Tyranitarite'}, 'Weakness Policy': {'name': 'Weakness Policy'}, 'White Herb': {'name': 'White Herb'}, 'Life Orb': {'name': 'Life Orb', 'description': "An item to be held by a Pokémon. It boosts the power of the holder's moves, but the holder also loses a small amount of HP upon landing an attack."}}

# Compatibility alias for code that prefers a plural database name.
ITEMS = ITEM_DATABASE

__all__ = ["ITEM_DATABASE", "ITEMS"]
