"""Canonical held-item registry for the Pokémon Battle Engine."""

ITEM_DATABASE = {
    'Assault Vest': {'name': 'Assault Vest', 'description': "An item to be held by a Pokémon. This offensive vest boosts the holder's Sp. Def stat but prevents the use of status moves."},
    'Black Sludge': {'name': 'Black Sludge', 'description': 'An item to be held by a Pokémon. If the holder is a Poison type, this sludge will gradually restore its HP. It damages any other type.'},
    'Booster Energy': {'name': 'Booster Energy', 'description': 'An item to be held by Pokémon with certain Abilities. The energy that fills this capsule boosts the strength of the Pokémon.'},
    'Charcoal': {'name': 'Charcoal', 'description': "An item to be held by a Pokémon. It's a combustible fuel that boosts the power of the holder's Fire-type moves."},
    'Choice Specs': {'name': 'Choice Specs', 'description': "An item to be held by a Pokémon. These curious glasses boost the holder's Sp. Atk stat but only allow the use of a single move."},
    'Clear Amulet': {'name': 'Clear Amulet', 'description': "An item to be held by a Pokémon. This clear, sparkling amulet protects the holder from having its stats lowered by moves used against it or by other Pokémon's Abilities."},
    'Covert Cloak': {'name': 'Covert Cloak', 'description': 'An item to be held by a Pokémon. This hooded cloak conceals the holder, tricking the eyes of its enemies and protecting it from the additional effects of moves.'},
    'Damp Rock': {'name': 'Damp Rock', 'description': 'An item to be held by a Pokémon. When the holder changes the weather to rain, the rain will persist for longer than usual.'},
    'Focus Sash': {'name': 'Focus Sash', 'description': 'An item to be held by a Pokémon. If the holder has full HP and it is hit with a move that should knock it out, it will endure with 1 HP—but only once.'},
    'Flame Orb': {'name': 'Flame Orb', 'description': "An item to be held by a Pokémon. It's a bizarre orb that gives off heat when touched and will afflict the holder with a burn during battle."},
    'Heat Rock': {'name': 'Heat Rock', 'description': 'An item to be held by a Pokémon. When the holder changes the weather to harsh sunlight, the sunlight will persist for longer than usual.'},
    'Houndoomite': {'name': 'Houndoomite', 'description': 'One of a variety of mysterious Mega Stones. Have Houndoom hold it, and this stone will enable it to Mega Evolve during battle.'},
    'Leftovers': {'name': 'Leftovers', 'description': "An item to be held by a Pokémon. It slowly but steadily restores the holder's HP."},
    'Light Clay': {'name': 'Light Clay', 'description': 'An item to be held by a Pokémon. When the holder uses protective moves like Light Screen or Reflect, their effects will last longer than usual.'},
    'Lucarionite': {'name': 'Lucarionite', 'description': 'One of a variety of mysterious Mega Stones. Have Lucario hold it, and this stone will enable it to Mega Evolve during battle.'},
    'Mental Herb': {'name': 'Mental Herb', 'description': 'An item to be held by a Pokémon. The holder will be able to shake off move-binding effects to move freely—but only once.'},
    'Mystic Water': {'name': 'Mystic Water', 'description': "An item to be held by a Pokémon. This teardrop-shaped gem boosts the power of the holder's Water-type moves."},
    'Power Herb': {'name': 'Power Herb', 'description': 'An item to be held by a Pokémon. It allows the holder to immediately use a move that normally requires a turn to charge—but only once.'},
    'Psychic Seed': {'name': 'Psychic Seed', 'description': 'An item to be held by a Pokémon. If the terrain becomes Psychic Terrain, the holder will use this seed to boost its own Sp. Def stat.'},
    'Red Orb': {'name': 'Red Orb', 'description': 'A shiny red orb that is said to have a deep connection to a legend of the Hoenn region.'},
    'Rocky Helmet': {'name': 'Rocky Helmet', 'description': 'An item to be held by a Pokémon. This helmet damages any attacker that makes direct contact with the holder.'},
    'Safety Goggles': {'name': 'Safety Goggles', 'description': 'An item to be held by a Pokémon. These goggles protect the holder from both sandstorm damage and the effects of powders and spores.'},
    'Sitrus Berry': {'name': 'Sitrus Berry', 'description': 'If a Pokémon holds one of these Berries, it will be able to restore a small amount of HP to itself.'},
    'Swampertite': {'name': 'Swampertite', 'description': 'One of a variety of mysterious Mega Stones. Have Swampert hold it, and this stone will enable it to Mega Evolve during battle.'},
    'Tyranitarite': {'name': 'Tyranitarite', 'description': 'One of the mysterious Mega Stones. Have Tyranitar hold it, and this stone will enable it to Mega Evolve in battle.'},
    'Weakness Policy': {'name': 'Weakness Policy', 'description': "An item to be held by a Pokémon. This policy boosts the holder's Attack and Sp. Atk. stats for a while if the holder is hit with a move it's weak to."},
    'White Herb': {'name': 'White Herb', 'description': 'An item to be held by a Pokémon. It will restore any lowered stat in battle—but only once.'},
    'Life Orb': {'name': 'Life Orb', 'description': "An item to be held by a Pokémon. It boosts the power of the holder's moves, but the holder also loses a small amount of HP upon landing an attack."},
    'Lum Berry': {'name': 'Lum Berry', 'description': 'If a Pokémon holds one of these Berries, it will be able to cure itself of any status condition it may have.'},
}

ITEMS = ITEM_DATABASE

__all__ = ["ITEM_DATABASE", "ITEMS"]
