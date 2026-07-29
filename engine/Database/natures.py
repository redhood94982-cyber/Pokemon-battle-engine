"""
Pokemon Battle Engine
database/natures.py

The database knows.
The engine does.

Official Pokémon natures with direct stat modifiers.
"""

NATURES = {
    "Hardy": {"HP":1.0,"Attack":1.0,"Defense":1.0,"Special Attack":1.0,"Special Defense":1.0,"Speed":1.0},
    "Lonely": {"HP":1.0,"Attack":1.1,"Defense":0.9,"Special Attack":1.0,"Special Defense":1.0,"Speed":1.0},
    "Brave": {"HP":1.0,"Attack":1.1,"Defense":1.0,"Special Attack":1.0,"Special Defense":1.0,"Speed":0.9},
    "Adamant": {"HP":1.0,"Attack":1.1,"Defense":1.0,"Special Attack":0.9,"Special Defense":1.0,"Speed":1.0},
    "Naughty": {"HP":1.0,"Attack":1.1,"Defense":1.0,"Special Attack":1.0,"Special Defense":0.9,"Speed":1.0},

    "Bold": {"HP":1.0,"Attack":0.9,"Defense":1.1,"Special Attack":1.0,"Special Defense":1.0,"Speed":1.0},
    "Docile": {"HP":1.0,"Attack":1.0,"Defense":1.0,"Special Attack":1.0,"Special Defense":1.0,"Speed":1.0},
    "Relaxed": {"HP":1.0,"Attack":1.0,"Defense":1.1,"Special Attack":1.0,"Special Defense":1.0,"Speed":0.9},
    "Impish": {"HP":1.0,"Attack":1.0,"Defense":1.1,"Special Attack":0.9,"Special Defense":1.0,"Speed":1.0},
    "Lax": {"HP":1.0,"Attack":1.0,"Defense":1.1,"Special Attack":1.0,"Special Defense":0.9,"Speed":1.0},

    "Timid": {"HP":1.0,"Attack":0.9,"Defense":1.0,"Special Attack":1.0,"Special Defense":1.0,"Speed":1.1},
    "Hasty": {"HP":1.0,"Attack":1.0,"Defense":0.9,"Special Attack":1.0,"Special Defense":1.0,"Speed":1.1},
    "Serious": {"HP":1.0,"Attack":1.0,"Defense":1.0,"Special Attack":1.0,"Special Defense":1.0,"Speed":1.0},
    "Jolly": {"HP":1.0,"Attack":1.0,"Defense":1.0,"Special Attack":0.9,"Special Defense":1.0,"Speed":1.1},
    "Naive": {"HP":1.0,"Attack":1.0,"Defense":1.0,"Special Attack":1.0,"Special Defense":0.9,"Speed":1.1},

    "Modest": {"HP":1.0,"Attack":0.9,"Defense":1.0,"Special Attack":1.1,"Special Defense":1.0,"Speed":1.0},
    "Mild": {"HP":1.0,"Attack":1.0,"Defense":0.9,"Special Attack":1.1,"Special Defense":1.0,"Speed":1.0},
    "Quiet": {"HP":1.0,"Attack":1.0,"Defense":1.0,"Special Attack":1.1,"Special Defense":1.0,"Speed":0.9},
    "Bashful": {"HP":1.0,"Attack":1.0,"Defense":1.0,"Special Attack":1.0,"Special Defense":1.0,"Speed":1.0},
    "Rash": {"HP":1.0,"Attack":1.0,"Defense":1.0,"Special Attack":1.1,"Special Defense":0.9,"Speed":1.0},

    "Calm": {"HP":1.0,"Attack":0.9,"Defense":1.0,"Special Attack":1.0,"Special Defense":1.1,"Speed":1.0},
    "Gentle": {"HP":1.0,"Attack":1.0,"Defense":0.9,"Special Attack":1.0,"Special Defense":1.1,"Speed":1.0},
    "Sassy": {"HP":1.0,"Attack":1.0,"Defense":1.0,"Special Attack":1.0,"Special Defense":1.1,"Speed":0.9},
    "Careful": {"HP":1.0,"Attack":1.0,"Defense":1.0,"Special Attack":0.9,"Special Defense":1.1,"Speed":1.0},
    "Quirky": {"HP":1.0,"Attack":1.0,"Defense":1.0,"Special Attack":1.0,"Special Defense":1.0,"Speed":1.0},
}
