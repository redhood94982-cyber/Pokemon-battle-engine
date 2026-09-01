"""Canonical held-item database for the Pokémon Battle Engine.
The database defines item mechanics; the engine executes them.
"""

ITEM_DATABASE = {
    'Assault Vest': {'name': 'Assault Vest', 'description': "An item to be held by a Pokémon. This offensive vest boosts the holder's Sp. Def stat but prevents the use of status moves.", 'special_defense_multiplier': 1.5, 'blocks_status_moves': True},
    'Black Sludge': {'name': 'Black Sludge', 'description': 'An item to be held by a Pokémon. If the holder is a Poison type, this sludge will gradually restore its HP. It damages any other type.', 'damage_fraction': 0.125, 'poison_heal_fraction': 0.0625, 'non_poison_damage_fraction': 0.125, 'end_of_turn': True},
    'Booster Energy': {'name': 'Booster Energy', 'description': 'An item to be held by Pokémon with certain Abilities. The energy that fills this capsule boosts the strength of the Pokémon.', 'consumable': True, 'activates_protosynthesis_or_quark_drive': True},
    'Charcoal': {'name': 'Charcoal', 'description': "An item to be held by a Pokémon. It's a combustible fuel that boosts the power of the holder's Fire-type moves.", 'damage_multiplier': 1.2, 'boosted_type': 'Fire'},
    'Choice Specs': {'name': 'Choice Specs', 'description': "An item to be held by a Pokémon. These curious glasses boost the holder's Sp. Atk stat but only allow the use of a single move.", 'special_attack_multiplier': 1.5, 'move_lock': True},
    'Clear Amulet': {'name': 'Clear Amulet', 'description': "An item to be held by a Pokémon. This clear, sparkling amulet protects the holder from having its stats lowered by moves used against it or by other Pokémon's Abilities.", 'blocks_opponent_stat_drops': True},
    'Covert Cloak': {'name': 'Covert Cloak', 'description': 'An item to be held by a Pokémon. This hooded cloak conceals the holder, tricking the eyes of its enemies and protecting it from the additional effects of moves.', 'blocks_secondary_effects': True},
    'Damp Rock': {'name': 'Damp Rock', 'description': 'An item to be held by a Pokémon. When the holder changes the weather to rain, the rain will persist for longer than usual.', 'weather_duration': 8, 'weather': 'Rain'},
    'Focus Sash': {'name': 'Focus Sash', 'description': 'An item to be held by a Pokémon. If the holder has full HP and it is hit with a move that should knock it out, it will endure with 1 HP—but only once.', 'survive_at_hp': 1, 'requires_full_hp': True, 'consumable': True, 'single_use': True},
    'Flame Orb': {'name': 'Flame Orb', 'description': "An item to be held by a Pokémon. It's a bizarre orb that gives off heat when touched and will afflict the holder with a burn during battle.", 'status': 'burn', 'trigger': 'end_of_turn'},
    'Heat Rock': {'name': 'Heat Rock', 'description': 'An item to be held by a Pokémon. When the holder changes the weather to harsh sunlight, the sunlight will persist for longer than usual.', 'weather_duration': 8, 'weather': 'Sun'},
    'Houndoomite': {'name': 'Houndoomite', 'description': 'One of a variety of mysterious Mega Stones. Have Houndoom hold it, and this stone will enable it to Mega Evolve during battle.', 'mega_evolution_species': 'Houndoom'},
    'Leftovers': {'name': 'Leftovers', 'description': "An item to be held by a Pokémon. It slowly but steadily restores the holder's HP.", 'heal_fraction': 0.0625, 'trigger': 'end_of_turn'},
    'Light Clay': {'name': 'Light Clay', 'description': 'An item to be held by a Pokémon. When the holder uses protective moves like Light Screen or Reflect, their effects will last longer than usual.', 'screen_duration': 8},
    'Lucarionite': {'name': 'Lucarionite', 'description': 'One of a variety of mysterious Mega Stones. Have Lucario hold it, and this stone will enable it to Mega Evolve during battle.', 'mega_evolution_species': 'Lucario'},
    'Mental Herb': {'name': 'Mental Herb', 'description': 'An item to be held by a Pokémon. The holder will be able to shake off move-binding effects to move freely—but only once.', 'consumable': True, 'cures_mental_effects': True},
    'Mystic Water': {'name': 'Mystic Water', 'description': "An item to be held by a Pokémon. This teardrop-shaped gem boosts the power of the holder's Water-type moves.", 'damage_multiplier': 1.2, 'boosted_type': 'Water'},
    'Power Herb': {'name': 'Power Herb', 'description': 'An item to be held by a Pokémon. It allows the holder to immediately use a move that normally requires a turn to charge—but only once.', 'consumable': True, 'removes_charge_turn': True, 'single_use': True},
    'Psychic Seed': {'name': 'Psychic Seed', 'description': 'An item to be held by a Pokémon. If the terrain becomes Psychic Terrain, the holder will use this seed to boost its own Sp. Def stat.', 'trigger_terrain': 'Psychic', 'stat': 'special_defense', 'stat_stage_change': 1, 'consumable': True},
    'Red Orb': {'name': 'Red Orb', 'description': 'A shiny red orb that is said to have a deep connection to a legend of the Hoenn region.', 'primal_evolution_species': 'Groudon', 'transformation': 'Primal Groudon'},
    'Rocky Helmet': {'name': 'Rocky Helmet', 'description': 'An item to be held by a Pokémon. This helmet damages any attacker that makes direct contact with the holder.', 'damage_fraction': 0.16666666666666666, 'contact_recoil_fraction': 0.16666666666666666},
    'Safety Goggles': {'name': 'Safety Goggles', 'description': 'An item to be held by a Pokémon. These goggles protect the holder from both sandstorm damage and the effects of powders and spores.', 'blocks_powder': True, 'blocks_weather_chip': True},
    'Sitrus Berry': {'name': 'Sitrus Berry', 'description': 'If a Pokémon holds one of these Berries, it will be able to restore a small amount of HP to itself.', 'heal_fraction': 0.25, 'trigger_hp_fraction': 0.5, 'consumable': True},
    'Swampertite': {'name': 'Swampertite', 'description': 'One of a variety of mysterious Mega Stones. Have Swampert hold it, and this stone will enable it to Mega Evolve during battle.', 'mega_evolution_species': 'Swampert'},
    'Tyranitarite': {'name': 'Tyranitarite', 'description': 'One of the mysterious Mega Stones. Have Tyranitar hold it, and this stone will enable it to Mega Evolve in battle.', 'mega_evolution_species': 'Tyranitar'},
    'Weakness Policy': {'name': 'Weakness Policy', 'description': "An item to be held by a Pokémon. This policy boosts the holder's Attack and Sp. Atk. stats for a while if the holder is hit with a move it's weak to.", 'trigger': 'super_effective_hit', 'attack_stage_change': 2, 'special_attack_stage_change': 2, 'consumable': True},
    'White Herb': {'name': 'White Herb', 'description': 'An item to be held by a Pokémon. It will restore any lowered stat in battle—but only once.', 'trigger': 'stat_drop', 'restores_lowered_stats': True, 'consumable': True, 'single_use': True},
    'Life Orb': {'name': 'Life Orb', 'description': "An item to be held by a Pokémon. It boosts the power of the holder's moves, but the holder also loses a small amount of HP upon landing an attack.", 'damage_multiplier': 1.3, 'recoil_fraction': 0.1, 'trigger': 'successful_damaging_move'},
    'Lum Berry': {'name': 'Lum Berry', 'description': 'If a Pokémon holds one of these Berries, it will be able to cure itself of any status condition it may have.', 'cures_major_status': True, 'cures_confusion': True, 'consumable': True},
}

ITEMS = ITEM_DATABASE

__all__ = ['ITEM_DATABASE', 'ITEMS']
