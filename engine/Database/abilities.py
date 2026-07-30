"""
abilities.py

Ability database for the Pokémon Battle Engine.

Development Rule:
- Store the ability name.
- Store a concise description.
- Store every trigger used by the engine.
"""

ABILITIES = {
    "Adaptability": {
        "description": "Increases the power of moves that match the user's type (STAB).",
        "triggers": ["Always Active"]
    },
    "Aerilate": {
        "description": "Normal-type moves become Flying-type moves and receive a power boost.",
        "triggers": ["Before Move"]
    },
    "Aftermath": {
        "description": "Damages an adjacent attacker if this Pokémon is knocked out by a contact move.",
        "triggers": ["On Faint", "On Contact"]
    },
    "Air Lock": {
        "description": "Negates the effects of weather while this Pokémon is active.",
        "triggers": ["Always Active"]
    },
    "Analytic": {
        "description": "Boosts move power when moving after the target.",
        "triggers": ["Before Move"]
    },
    "Anger Point": {
        "description": "Maximizes Attack after receiving a critical hit.",
        "triggers": ["On Critical Hit Taken"]
    },
    "Anger Shell": {
        "description": "When HP drops to half or below, lowers Defense and Special Defense while raising Attack, Special Attack, and Speed.",
        "triggers": ["On HP Threshold"]
    },
    "Anticipation": {
        "description": "Shudders if an opposing Pokémon knows a super-effective or one-hit KO move.",
        "triggers": ["On Switch-In"]
    },
    "Arena Trap": {
        "description": "Prevents adjacent grounded opposing Pokémon from switching out.",
        "triggers": ["Always Active"]
    },
    "Armor Tail": {
        "description": "Protects allies from opposing priority moves.",
        "triggers": ["On Priority Move"]
    },
    "Aroma Veil": {
        "description": "Protects the Pokémon and its allies from move-limiting effects.",
        "triggers": ["Always Active"]
    },
    "As One (Glastrier)": {
        "description": "Combines Chilling Neigh and Unnerve.",
        "triggers": ["On Faint", "Always Active"]
    },
    "As One (Spectrier)": {
        "description": "Combines Grim Neigh and Unnerve.",
        "triggers": ["On Faint", "Always Active"]
    },
    "Aura Break": {
        "description": "Reverses the effects of Fairy Aura and Dark Aura.",
        "triggers": ["Always Active"]
    }

    ,
    "Bad Dreams": {
        "description": "Damages sleeping opposing Pokémon at the end of each turn.",
        "triggers": ["End of Turn"]
    },
    "Ball Fetch": {
        "description": "Retrieves the first failed Poké Ball if the Pokémon is not holding an item.",
        "triggers": ["After Item Use"]
    },
    "Battery": {
        "description": "Boosts the power of allies' special moves.",
        "triggers": ["Always Active"]
    },
    "Battle Armor": {
        "description": "Prevents this Pokémon from receiving critical hits.",
        "triggers": ["Always Active"]
    },
    "Battle Bond": {
        "description": "Activates after knocking out a Pokémon, granting its special effect.",
        "triggers": ["On Faint"]
    },
    "Beads of Ruin": {
        "description": "Lowers the Special Defense of all other active Pokémon.",
        "triggers": ["Always Active"]
    },
    "Beast Boost": {
        "description": "Raises the user's highest stat after it knocks out a Pokémon.",
        "triggers": ["On Faint"]
    },
    "Berserk": {
        "description": "Raises Special Attack when HP drops below half.",
        "triggers": ["On HP Threshold"]
    },
    "Big Pecks": {
        "description": "Prevents Defense from being lowered by other Pokémon.",
        "triggers": ["Always Active"]
    },
    "Blaze": {
        "description": "Boosts Fire-type moves when HP is low.",
        "triggers": ["On HP Threshold"]
    },
    "Bulletproof": {
        "description": "Grants immunity to ball and bomb-based moves.",
        "triggers": ["Always Active"]
    }


    ,
    "Cheek Pouch": {
        "description": "Restores HP after consuming a Berry.",
        "triggers": ["On Berry Consumed"]
    },
    "Chilling Neigh": {
        "description": "Raises Attack after knocking out a Pokémon.",
        "triggers": ["On Faint"]
    },
    "Chlorophyll": {
        "description": "Doubles Speed during harsh sunlight.",
        "triggers": ["On Weather"]
    },
    "Clear Body": {
        "description": "Prevents other Pokémon from lowering this Pokémon's stats.",
        "triggers": ["Always Active"]
    },
    "Cloud Nine": {
        "description": "Negates the effects of weather while this Pokémon is active.",
        "triggers": ["Always Active"]
    },
    "Color Change": {
        "description": "Changes the user's type to match the type of the move that hit it.",
        "triggers": ["On Damage Taken"]
    },
    "Comatose": {
        "description": "The Pokémon is treated as though it is always asleep.",
        "triggers": ["Always Active"]
    },
    "Commander": {
        "description": "Allows Tatsugiri to enter Dondozo's mouth and empower it in battle.",
        "triggers": ["On Switch-In"]
    },
    "Competitive": {
        "description": "Sharply raises Special Attack when a stat is lowered by an opponent.",
        "triggers": ["On Stat Lowered"]
    },
    "Compound Eyes": {
        "description": "Raises the accuracy of this Pokémon's moves.",
        "triggers": ["Always Active"]
    },
    "Contrary": {
        "description": "Reverses all stat stage increases and decreases.",
        "triggers": ["Always Active"]
    },
    "Corrosion": {
        "description": "Allows Poison- and Steel-type Pokémon to be poisoned.",
        "triggers": ["Before Move"]
    },
    "Costar": {
        "description": "Copies an ally's stat changes upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Cotton Down": {
        "description": "Lowers the Speed of other Pokémon when hit by an attack.",
        "triggers": ["On Damage Taken"]
    },
    "Cud Chew": {
        "description": "Causes a consumed Berry to be eaten again at the end of the next turn.",
        "triggers": ["End of Turn"]
    },
    "Curious Medicine": {
        "description": "Resets allies' stat changes when entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Cursed Body": {
        "description": "May disable a move that damages this Pokémon.",
        "triggers": ["On Damage Taken"]
    }


    ,
    "Damp": {
        "description": "Prevents Self-Destruct, Explosion, Mind Blown, and Aftermath from activating.",
        "triggers": ["Always Active"]
    },
    "Dancer": {
        "description": "Copies dance moves used by other Pokémon immediately after they are executed.",
        "triggers": ["After Move"]
    },
    "Dark Aura": {
        "description": "Boosts the power of Dark-type moves used by all active Pokémon.",
        "triggers": ["Always Active"]
    },
    "Dauntless Shield": {
        "description": "Raises Defense upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Dazzling": {
        "description": "Prevents opposing Pokémon from using priority moves against this Pokémon or its allies.",
        "triggers": ["On Priority Move"]
    },
    "Defeatist": {
        "description": "Halves Attack and Special Attack when HP falls below half.",
        "triggers": ["On HP Threshold"]
    },
    "Defiant": {
        "description": "Sharply raises Attack when a stat is lowered by an opponent.",
        "triggers": ["On Stat Lowered"]
    },
    "Delta Stream": {
        "description": "Creates strong winds that protect Flying-type Pokémon from weaknesses.",
        "triggers": ["On Switch-In", "On Weather"]
    },
    "Desolate Land": {
        "description": "Creates extremely harsh sunlight that nullifies Water-type moves.",
        "triggers": ["On Switch-In", "On Weather"]
    },
    "Disguise": {
        "description": "Negates damage from the first damaging hit while in its disguised form.",
        "triggers": ["On Damage Taken"]
    },
    "Download": {
        "description": "Raises Attack or Special Attack based on the target's weaker defensive stat.",
        "triggers": ["On Switch-In"]
    },
    "Dragon's Maw": {
        "description": "Boosts the power of Dragon-type moves.",
        "triggers": ["Always Active"]
    },
    "Drizzle": {
        "description": "Summons rain when entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Drought": {
        "description": "Summons harsh sunlight when entering battle.",
        "triggers": ["On Switch-In"]
    }


    ,
    "Early Bird": {
        "description": "Wakes from sleep in half the normal number of turns.",
        "triggers": ["Always Active"]
    },
    "Earth Eater": {
        "description": "Grants immunity to Ground-type moves and restores HP when hit by one.",
        "triggers": ["On Damage Taken"]
    },
    "Effect Spore": {
        "description": "May inflict sleep, paralysis, or poison on a Pokémon making contact.",
        "triggers": ["On Contact"]
    },
    "Electric Surge": {
        "description": "Creates Electric Terrain upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Electromorphosis": {
        "description": "Charges up after taking damage, boosting the next Electric-type move.",
        "triggers": ["On Damage Taken", "Before Move"]
    },
    "Embody Aspect (Cornerstone)": {
        "description": "Raises Defense when Terastallizing into the Cornerstone form.",
        "triggers": ["On Terastallize"]
    },
    "Embody Aspect (Hearthflame)": {
        "description": "Raises Attack when Terastallizing into the Hearthflame form.",
        "triggers": ["On Terastallize"]
    },
    "Embody Aspect (Teal)": {
        "description": "Raises Speed when Terastallizing into the Teal form.",
        "triggers": ["On Terastallize"]
    },
    "Embody Aspect (Wellspring)": {
        "description": "Raises Special Defense when Terastallizing into the Wellspring form.",
        "triggers": ["On Terastallize"]
    },
    "Emergency Exit": {
        "description": "Forces the Pokémon to switch out when its HP drops below half.",
        "triggers": ["On HP Threshold"]
    },
    "Fairy Aura": {
        "description": "Boosts the power of Fairy-type moves used by all active Pokémon.",
        "triggers": ["Always Active"]
    },
    "Filter": {
        "description": "Reduces damage taken from super-effective moves.",
        "triggers": ["On Damage Taken"]
    },
    "Flame Body": {
        "description": "May burn a Pokémon that makes contact.",
        "triggers": ["On Contact"]
    },
    "Flare Boost": {
        "description": "Boosts Special Attack while the Pokémon is burned.",
        "triggers": ["Always Active"]
    },
    "Flash Fire": {
        "description": "Grants immunity to Fire-type moves and boosts Fire-type moves after being hit.",
        "triggers": ["On Damage Taken", "Always Active"]
    },
    "Flower Gift": {
        "description": "Transforms Cherrim in sunshine and boosts the Attack and Special Defense of allies.",
        "triggers": ["On Weather"]
    },
    "Flower Veil": {
        "description": "Protects allied Grass-type Pokémon from status conditions and stat reductions.",
        "triggers": ["Always Active"]
    },
    "Fluffy": {
        "description": "Halves damage from contact moves but increases damage from Fire-type moves.",
        "triggers": ["On Damage Taken"]
    },
    "Forecast": {
        "description": "Changes Castform's form based on the current weather.",
        "triggers": ["On Weather"]
    },
    "Forewarn": {
        "description": "Reveals an opponent's move with the highest base power.",
        "triggers": ["On Switch-In"]
    },
    "Friend Guard": {
        "description": "Reduces damage taken by allies.",
        "triggers": ["Always Active"]
    },
    "Frisk": {
        "description": "Reveals the held item of an opposing Pokémon.",
        "triggers": ["On Switch-In"]
    },
    "Full Metal Body": {
        "description": "Prevents other Pokémon from lowering this Pokémon's stats.",
        "triggers": ["Always Active"]
    },
    "Fur Coat": {
        "description": "Doubles the Pokémon's Defense against physical moves.",
        "triggers": ["Always Active"]
    }


    ,
    "Galvanize": {
        "description": "Normal-type moves become Electric-type moves and receive a power boost.",
        "triggers": ["Before Move"]
    },
    "Gluttony": {
        "description": "Causes the Pokémon to eat its Berry earlier than usual.",
        "triggers": ["On HP Threshold"]
    },
    "Good as Gold": {
        "description": "Grants immunity to status moves used by other Pokémon.",
        "triggers": ["Always Active"]
    },
    "Gooey": {
        "description": "Lowers the Speed of a Pokémon that makes contact.",
        "triggers": ["On Contact"]
    },
    "Gorilla Tactics": {
        "description": "Boosts Attack but restricts the Pokémon to its first selected move.",
        "triggers": ["Always Active"]
    },
    "Grass Pelt": {
        "description": "Raises Defense while Grassy Terrain is active.",
        "triggers": ["On Terrain"]
    },
    "Grassy Surge": {
        "description": "Creates Grassy Terrain upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Grim Neigh": {
        "description": "Raises Special Attack after knocking out a Pokémon.",
        "triggers": ["On Faint"]
    },
    "Guard Dog": {
        "description": "Prevents forced switching and raises Attack when intimidated.",
        "triggers": ["Always Active", "On Stat Lowered"]
    },
    "Gulp Missile": {
        "description": "Changes form after Surf or Dive and retaliates when hit.",
        "triggers": ["After Move", "On Damage Taken"]
    },
    "Guts": {
        "description": "Boosts Attack while affected by a major status condition.",
        "triggers": ["Always Active"]
    }


    ,
    "Hadron Engine": {
        "description": "Creates Electric Terrain on entry and boosts the user's Special Attack while Electric Terrain is active.",
        "triggers": ["On Switch-In", "On Terrain"]
    },
    "Harvest": {
        "description": "May restore a consumed Berry at the end of the turn, with a higher chance in sunshine.",
        "triggers": ["End of Turn", "On Weather"]
    },
    "Healer": {
        "description": "May cure an adjacent ally's major status condition at the end of the turn.",
        "triggers": ["End of Turn"]
    },
    "Heatproof": {
        "description": "Reduces damage from Fire-type moves and burn damage.",
        "triggers": ["Always Active"]
    },
    "Heavy Metal": {
        "description": "Doubles the Pokémon's weight.",
        "triggers": ["Always Active"]
    },
    "Honey Gather": {
        "description": "May gather Honey outside of battle.",
        "triggers": []
    },
    "Hospitality": {
        "description": "Restores an ally's HP when entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Huge Power": {
        "description": "Doubles the Pokémon's Attack stat.",
        "triggers": ["Always Active"]
    },
    "Hunger Switch": {
        "description": "Switches Morpeko between Full Belly Mode and Hangry Mode at the end of each turn.",
        "triggers": ["End of Turn"]
    },
    "Hustle": {
        "description": "Raises Attack but lowers the accuracy of physical moves.",
        "triggers": ["Always Active"]
    },
    "Hydration": {
        "description": "Cures status conditions at the end of the turn while it is raining.",
        "triggers": ["End of Turn", "On Weather"]
    },
    "Hyper Cutter": {
        "description": "Prevents other Pokémon from lowering this Pokémon's Attack stat.",
        "triggers": ["Always Active"]
    }


    ,
    "Ice Body": {
        "description": "Restores HP at the end of each turn during snow.",
        "triggers": ["End of Turn", "On Weather"]
    },
    "Ice Face": {
        "description": "Prevents damage from the first physical hit and is restored during snow.",
        "triggers": ["On Damage Taken", "On Weather"]
    },
    "Ice Scales": {
        "description": "Halves damage taken from special moves.",
        "triggers": ["Always Active"]
    },
    "Illuminate": {
        "description": "Has no effect during battle.",
        "triggers": []
    },
    "Illusion": {
        "description": "Disguises the Pokémon as the last healthy party member until the disguise is broken.",
        "triggers": ["On Switch-In", "On Damage Taken"]
    },
    "Immunity": {
        "description": "Prevents the Pokémon from being poisoned.",
        "triggers": ["Always Active"]
    },
    "Imposter": {
        "description": "Transforms into the opposing Pokémon upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Infiltrator": {
        "description": "Allows moves to ignore the target's substitutes and protective barriers.",
        "triggers": ["Always Active"]
    },
    "Innards Out": {
        "description": "Damages the attacker equal to this Pokémon's remaining HP when it faints.",
        "triggers": ["On Faint"]
    },
    "Inner Focus": {
        "description": "Prevents flinching and ignores Intimidate.",
        "triggers": ["Always Active"]
    },
    "Insomnia": {
        "description": "Prevents the Pokémon from falling asleep.",
        "triggers": ["Always Active"]
    },
    "Intimidate": {
        "description": "Lowers the Attack of adjacent opposing Pokémon upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Intrepid Sword": {
        "description": "Raises Attack upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Iron Barbs": {
        "description": "Damages a Pokémon that makes contact.",
        "triggers": ["On Contact"]
    },
    "Iron Fist": {
        "description": "Boosts the power of punching moves.",
        "triggers": ["Always Active"]
    }


    ,
    "Justified": {
        "description": "Raises Attack when hit by a Dark-type move.",
        "triggers": ["On Damage Taken"]
    }


    ,
    "Keen Eye": {
        "description": "Prevents other Pokémon from lowering this Pokémon's Accuracy and ignores the target's evasiveness.",
        "triggers": ["Always Active"]
    },
    "Klutz": {
        "description": "Prevents the Pokémon from using the effects of its held item.",
        "triggers": ["Always Active"]
    }


    ,
    "Leaf Guard": {
        "description": "Prevents status conditions while harsh sunlight is active.",
        "triggers": ["On Weather"]
    },
    "Levitate": {
        "description": "Grants immunity to Ground-type moves and the effects of grounded hazards and terrain.",
        "triggers": ["Always Active"]
    },
    "Libero": {
        "description": "Changes the user's type to match the type of the move it is about to use once upon entering battle.",
        "triggers": ["Before Move"]
    },
    "Light Metal": {
        "description": "Halves the Pokémon's weight.",
        "triggers": ["Always Active"]
    },
    "Lightning Rod": {
        "description": "Draws Electric-type moves to the user, grants immunity to them, and raises Special Attack when hit.",
        "triggers": ["On Move Targeted", "On Damage Taken"]
    },
    "Limber": {
        "description": "Prevents the Pokémon from becoming paralyzed.",
        "triggers": ["Always Active"]
    },
    "Lingering Aroma": {
        "description": "Replaces the attacker's Ability with Lingering Aroma after a contact move.",
        "triggers": ["On Contact"]
    },
    "Liquid Ooze": {
        "description": "Damages Pokémon that attempt to drain HP from this Pokémon.",
        "triggers": ["On HP Drained"]
    },
    "Liquid Voice": {
        "description": "Sound-based moves become Water-type moves.",
        "triggers": ["Before Move"]
    },
    "Long Reach": {
        "description": "Allows contact moves to be used without making physical contact.",
        "triggers": ["Before Move"]
    }


    ,
    "Magic Bounce": {
        "description": "Reflects most status moves back at the user instead of allowing them to take effect.",
        "triggers": ["On Status Move Targeted"]
    },
    "Magic Guard": {
        "description": "Prevents all indirect damage except damage from direct attacks.",
        "triggers": ["Always Active"]
    },
    "Magician": {
        "description": "Steals the target's held item after damaging it if the user is not holding an item.",
        "triggers": ["After Move"]
    },
    "Magma Armor": {
        "description": "Prevents the Pokémon from becoming frozen.",
        "triggers": ["Always Active"]
    },
    "Magnet Pull": {
        "description": "Prevents adjacent Steel-type Pokémon from switching out.",
        "triggers": ["Always Active"]
    },
    "Marvel Scale": {
        "description": "Raises Defense while the Pokémon is affected by a major status condition.",
        "triggers": ["Always Active"]
    },
    "Mega Launcher": {
        "description": "Boosts the power of aura and pulse moves.",
        "triggers": ["Always Active"]
    },
    "Merciless": {
        "description": "Always lands critical hits against poisoned targets.",
        "triggers": ["Before Move"]
    },
    "Mimicry": {
        "description": "Changes the Pokémon's type to match the current terrain.",
        "triggers": ["On Terrain"]
    },
    "Minus": {
        "description": "Raises Special Attack when an ally has Plus or Minus.",
        "triggers": ["Always Active"]
    },
    "Mirror Armor": {
        "description": "Reflects stat reductions back to the Pokémon that caused them.",
        "triggers": ["On Stat Lowered"]
    },
    "Misty Surge": {
        "description": "Creates Misty Terrain upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Mold Breaker": {
        "description": "Moves ignore the target's Ability when applicable.",
        "triggers": ["Before Move"]
    },
    "Moody": {
        "description": "Raises one stat by two stages and lowers another by one stage at the end of each turn.",
        "triggers": ["End of Turn"]
    },
    "Motor Drive": {
        "description": "Grants immunity to Electric-type moves and raises Speed when hit by one.",
        "triggers": ["On Damage Taken"]
    },
    "Moxie": {
        "description": "Raises Attack after knocking out a Pokémon.",
        "triggers": ["On Faint"]
    },
    "Multiscale": {
        "description": "Reduces damage taken when the Pokémon is at full HP.",
        "triggers": ["On Damage Taken"]
    },
    "Multitype": {
        "description": "Changes Arceus's type to match the Plate or Z-Crystal it is holding.",
        "triggers": ["Always Active"]
    },
    "Mummy": {
        "description": "Replaces the attacker's Ability with Mummy after a contact move.",
        "triggers": ["On Contact"]
    },
    "Mycelium Might": {
        "description": "Status moves always move last but ignore the target's Ability.",
        "triggers": ["Before Move"]
    }


    ,
    "Natural Cure": {
        "description": "Cures the Pokémon's major status condition when it switches out.",
        "triggers": ["On Switch-Out"]
    },
    "Neuroforce": {
        "description": "Boosts the power of super-effective moves.",
        "triggers": ["Before Move"]
    },
    "Neutralizing Gas": {
        "description": "Suppresses the effects of all other Abilities while this Pokémon is active.",
        "triggers": ["On Switch-In", "On Switch-Out"]
    },
    "No Guard": {
        "description": "Ensures that all moves used by and against this Pokémon bypass accuracy checks.",
        "triggers": ["Always Active"]
    },
    "Normalize": {
        "description": "Makes all moves Normal-type and boosts their power.",
        "triggers": ["Before Move"]
    }


    ,
    "Oblivious": {
        "description": "Prevents infatuation, Taunt, Intimidate, and similar mental effects.",
        "triggers": ["Always Active"]
    },
    "Opportunist": {
        "description": "Copies an opposing Pokémon's stat increases when they occur.",
        "triggers": ["On Stat Raised"]
    },
    "Orichalcum Pulse": {
        "description": "Creates harsh sunlight upon entering battle and boosts the user's Attack while sunlight is active.",
        "triggers": ["On Switch-In", "On Weather"]
    },
    "Overcoat": {
        "description": "Protects the Pokémon from powder moves and damage from weather.",
        "triggers": ["Always Active"]
    },
    "Overgrow": {
        "description": "Boosts the power of Grass-type moves when HP is low.",
        "triggers": ["On HP Threshold"]
    },
    "Own Tempo": {
        "description": "Prevents confusion and ignores Intimidate.",
        "triggers": ["Always Active"]
    }


    ,
    "Parental Bond": {
        "description": "Allows damaging moves to hit twice, with the second hit dealing reduced damage.",
        "triggers": ["Before Move"]
    },
    "Pastel Veil": {
        "description": "Prevents poisoning for the Pokémon and its allies and cures allies of poison on entry.",
        "triggers": ["Always Active", "On Switch-In"]
    },
    "Perish Body": {
        "description": "Causes both Pokémon to gain Perish Song's effect after contact.",
        "triggers": ["On Contact"]
    },
    "Pickpocket": {
        "description": "Steals the attacker's held item after being hit by a contact move.",
        "triggers": ["On Contact"]
    },
    "Pickup": {
        "description": "May obtain or recover a used item.",
        "triggers": ["End of Turn"]
    },
    "Pixilate": {
        "description": "Normal-type moves become Fairy-type moves and receive a power boost.",
        "triggers": ["Before Move"]
    },
    "Plus": {
        "description": "Raises Special Attack when an ally has Plus or Minus.",
        "triggers": ["Always Active"]
    },
    "Poison Heal": {
        "description": "Restores HP instead of taking poison damage while poisoned.",
        "triggers": ["End of Turn"]
    },
    "Poison Point": {
        "description": "May poison a Pokémon that makes contact.",
        "triggers": ["On Contact"]
    },
    "Poison Puppeteer": {
        "description": "Confuses a target that becomes poisoned by this Pokémon.",
        "triggers": ["On Status Inflicted"]
    },
    "Poison Touch": {
        "description": "May poison a target hit by a contact move.",
        "triggers": ["After Move"]
    },
    "Power Construct": {
        "description": "Changes Zygarde into its Complete Forme when its HP falls below half.",
        "triggers": ["On HP Threshold"]
    },
    "Power of Alchemy": {
        "description": "Copies the Ability of a fainted ally.",
        "triggers": ["On Ally Faint"]
    },
    "Pressure": {
        "description": "Causes opposing Pokémon to use extra PP.",
        "triggers": ["Always Active"]
    },
    "Primordial Sea": {
        "description": "Creates heavy rain that nullifies Fire-type moves.",
        "triggers": ["On Switch-In", "On Weather"]
    },
    "Prism Armor": {
        "description": "Reduces damage taken from super-effective moves.",
        "triggers": ["On Damage Taken"]
    },
    "Propeller Tail": {
        "description": "Ignores effects that redirect moves.",
        "triggers": ["Always Active"]
    },
    "Protean": {
        "description": "Changes the user's type to match the move it uses once upon entering battle.",
        "triggers": ["Before Move"]
    },
    "Protosynthesis": {
        "description": "Boosts the user's highest stat in harsh sunlight or with Booster Energy.",
        "triggers": ["On Weather", "On Item"]
    },
    "Psychic Surge": {
        "description": "Creates Psychic Terrain upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Punk Rock": {
        "description": "Boosts sound-based moves and reduces damage from them.",
        "triggers": ["Always Active"]
    },
    "Pure Power": {
        "description": "Doubles the Pokémon's Attack stat.",
        "triggers": ["Always Active"]
    },
    "Purifying Salt": {
        "description": "Prevents status conditions and halves damage from Ghost-type moves.",
        "triggers": ["Always Active"]
    }


    ,
    "Queenly Majesty": {
        "description": "Prevents opposing Pokémon from using priority moves against this Pokémon or its allies.",
        "triggers": ["On Priority Move"]
    },
    "Quick Draw": {
        "description": "May allow the Pokémon to move first regardless of priority.",
        "triggers": ["Before Move"]
    },
    "Quick Feet": {
        "description": "Raises Speed while affected by a major status condition.",
        "triggers": ["Always Active"]
    }


    ,
    "Rain Dish": {
        "description": "Restores HP at the end of each turn while it is raining.",
        "triggers": ["End of Turn", "On Weather"]
    },
    "Rattled": {
        "description": "Raises Speed when hit by a Bug-, Dark-, or Ghost-type move or when intimidated.",
        "triggers": ["On Damage Taken", "On Stat Lowered"]
    },
    "Receiver": {
        "description": "Copies the Ability of a fainted ally.",
        "triggers": ["On Ally Faint"]
    },
    "Reckless": {
        "description": "Boosts the power of moves that cause recoil damage.",
        "triggers": ["Before Move"]
    },
    "Refrigerate": {
        "description": "Normal-type moves become Ice-type moves and receive a power boost.",
        "triggers": ["Before Move"]
    },
    "Regenerator": {
        "description": "Restores HP when the Pokémon switches out.",
        "triggers": ["On Switch-Out"]
    },
    "Ripen": {
        "description": "Doubles the effects of Berries consumed by the Pokémon.",
        "triggers": ["On Berry Consumed"]
    },
    "Rivalry": {
        "description": "Deals more damage to Pokémon of the same gender and less to the opposite gender.",
        "triggers": ["Before Move"]
    },
    "RKS System": {
        "description": "Changes Silvally's type to match the Memory it is holding.",
        "triggers": ["Always Active"]
    },
    "Rock Head": {
        "description": "Prevents recoil damage from recoil-causing moves.",
        "triggers": ["Always Active"]
    },
    "Rocky Payload": {
        "description": "Boosts the power of Rock-type moves.",
        "triggers": ["Always Active"]
    },
    "Rough Skin": {
        "description": "Damages a Pokémon that makes contact.",
        "triggers": ["On Contact"]
    },
    "Run Away": {
        "description": "Allows the Pokémon to always flee from wild battles.",
        "triggers": []
    }


    ,
    "Sand Force": {
        "description": "Boosts Rock-, Ground-, and Steel-type moves during a sandstorm.",
        "triggers": ["On Weather"]
    },
    "Sand Rush": {
        "description": "Doubles Speed during a sandstorm.",
        "triggers": ["On Weather"]
    },
    "Sand Spit": {
        "description": "Summons a sandstorm when hit by an attack.",
        "triggers": ["On Damage Taken"]
    },
    "Sand Stream": {
        "description": "Summons a sandstorm upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Sand Veil": {
        "description": "Raises evasiveness during a sandstorm.",
        "triggers": ["On Weather"]
    },
    "Sap Sipper": {
        "description": "Grants immunity to Grass-type moves and raises Attack when hit by one.",
        "triggers": ["On Damage Taken"]
    },
    "Schooling": {
        "description": "Changes Wishiwashi into School Form while its HP is above the threshold.",
        "triggers": ["On HP Threshold"]
    },
    "Scrappy": {
        "description": "Allows Normal- and Fighting-type moves to hit Ghost-type Pokémon.",
        "triggers": ["Always Active"]
    },
    "Screen Cleaner": {
        "description": "Removes barriers and screens when entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Seed Sower": {
        "description": "Creates Grassy Terrain after the Pokémon is hit by an attack.",
        "triggers": ["On Damage Taken"]
    },
    "Serene Grace": {
        "description": "Doubles the chance of additional effects occurring.",
        "triggers": ["Always Active"]
    },
    "Shadow Shield": {
        "description": "Reduces damage taken when the Pokémon is at full HP.",
        "triggers": ["On Damage Taken"]
    },
    "Shadow Tag": {
        "description": "Prevents opposing Pokémon from switching out.",
        "triggers": ["Always Active"]
    },
    "Sharpness": {
        "description": "Boosts the power of slicing moves.",
        "triggers": ["Always Active"]
    },
    "Shed Skin": {
        "description": "May cure a major status condition at the end of each turn.",
        "triggers": ["End of Turn"]
    },
    "Sheer Force": {
        "description": "Boosts moves with secondary effects while removing those effects.",
        "triggers": ["Before Move"]
    },
    "Shell Armor": {
        "description": "Prevents the Pokémon from receiving critical hits.",
        "triggers": ["Always Active"]
    },
    "Shield Dust": {
        "description": "Blocks the additional effects of damaging moves.",
        "triggers": ["Always Active"]
    },
    "Shields Down": {
        "description": "Changes Minior's form based on its HP.",
        "triggers": ["On HP Threshold"]
    },
    "Simple": {
        "description": "Doubles the effect of stat stage changes.",
        "triggers": ["On Stat Changed"]
    },
    "Skill Link": {
        "description": "Multi-hit moves always strike the maximum number of times.",
        "triggers": ["Before Move"]
    },
    "Slow Start": {
        "description": "Halves Attack and Speed for the first five turns after entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Slush Rush": {
        "description": "Doubles Speed during snow.",
        "triggers": ["On Weather"]
    },
    "Sniper": {
        "description": "Boosts the damage dealt by critical hits.",
        "triggers": ["On Critical Hit"]
    },
    "Snow Cloak": {
        "description": "Raises evasiveness during snow.",
        "triggers": ["On Weather"]
    },
    "Snow Warning": {
        "description": "Summons snow upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Solar Power": {
        "description": "Raises Special Attack in harsh sunlight but loses HP each turn.",
        "triggers": ["On Weather", "End of Turn"]
    },
    "Solid Rock": {
        "description": "Reduces damage taken from super-effective moves.",
        "triggers": ["On Damage Taken"]
    },
    "Soul-Heart": {
        "description": "Raises Special Attack whenever another Pokémon faints.",
        "triggers": ["On Faint"]
    },
    "Soundproof": {
        "description": "Grants immunity to sound-based moves.",
        "triggers": ["Always Active"]
    },
    "Speed Boost": {
        "description": "Raises Speed at the end of each turn.",
        "triggers": ["End of Turn"]
    },
    "Stakeout": {
        "description": "Deals double damage to a target that switched in that turn.",
        "triggers": ["Before Move"]
    },
    "Stall": {
        "description": "Makes the Pokémon move last within its priority bracket.",
        "triggers": ["Before Move"]
    },
    "Stalwart": {
        "description": "Ignores effects that redirect moves.",
        "triggers": ["Always Active"]
    },
    "Stamina": {
        "description": "Raises Defense when hit by an attack.",
        "triggers": ["On Damage Taken"]
    },
    "Stance Change": {
        "description": "Changes Aegislash's form based on the move it uses.",
        "triggers": ["Before Move"]
    },
    "Static": {
        "description": "May paralyze a Pokémon that makes contact.",
        "triggers": ["On Contact"]
    },
    "Steadfast": {
        "description": "Raises Speed after flinching.",
        "triggers": ["On Flinch"]
    },
    "Steam Engine": {
        "description": "Greatly raises Speed when hit by a Fire- or Water-type move.",
        "triggers": ["On Damage Taken"]
    },
    "Steelworker": {
        "description": "Boosts the power of Steel-type moves.",
        "triggers": ["Always Active"]
    },
    "Steely Spirit": {
        "description": "Boosts the power of allies' Steel-type moves.",
        "triggers": ["Always Active"]
    },
    "Stench": {
        "description": "May cause the target to flinch.",
        "triggers": ["After Move"]
    },
    "Sticky Hold": {
        "description": "Prevents the Pokémon's held item from being removed or swapped.",
        "triggers": ["Always Active"]
    },
    "Storm Drain": {
        "description": "Draws Water-type moves to the user, grants immunity, and raises Special Attack.",
        "triggers": ["On Move Targeted", "On Damage Taken"]
    },
    "Strong Jaw": {
        "description": "Boosts the power of biting moves.",
        "triggers": ["Always Active"]
    },
    "Sturdy": {
        "description": "Prevents a one-hit knockout from full HP.",
        "triggers": ["On Damage Taken"]
    },
    "Suction Cups": {
        "description": "Prevents forced switching.",
        "triggers": ["Always Active"]
    },
    "Super Luck": {
        "description": "Raises the critical-hit ratio of moves.",
        "triggers": ["Always Active"]
    },
    "Supersweet Syrup": {
        "description": "Lowers the evasiveness of opposing Pokémon upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Supreme Overlord": {
        "description": "Boosts the user's moves based on the number of fainted allies.",
        "triggers": ["Always Active"]
    },
    "Surge Surfer": {
        "description": "Doubles Speed while Electric Terrain is active.",
        "triggers": ["On Terrain"]
    },
    "Swarm": {
        "description": "Boosts the power of Bug-type moves when HP is low.",
        "triggers": ["On HP Threshold"]
    },
    "Sweet Veil": {
        "description": "Prevents allies from falling asleep.",
        "triggers": ["Always Active"]
    },
    "Swift Swim": {
        "description": "Doubles Speed while it is raining.",
        "triggers": ["On Weather"]
    },
    "Symbiosis": {
        "description": "Passes its held item to an ally that consumed theirs.",
        "triggers": ["After Item Use"]
    },
    "Synchronize": {
        "description": "Passes burn, poison, or paralysis back to the Pokémon that inflicted it.",
        "triggers": ["On Status Inflicted"]
    }


    ,
    "Tablets of Ruin": {
        "description": "Lowers the Attack of all other active Pokémon.",
        "triggers": ["Always Active"]
    },
    "Tangling Hair": {
        "description": "Lowers the Speed of a Pokémon that makes contact.",
        "triggers": ["On Contact"]
    },
    "Technician": {
        "description": "Boosts the power of moves with 60 base power or less.",
        "triggers": ["Before Move"]
    },
    "Telepathy": {
        "description": "Avoids damage from allies' attacks.",
        "triggers": ["Always Active"]
    },
    "Tera Shift": {
        "description": "Transforms Terapagos into its Terastal Form upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Tera Shell": {
        "description": "Reduces damage from super-effective moves while at full HP.",
        "triggers": ["On Damage Taken"]
    },
    "Teraform Zero": {
        "description": "Removes all weather and terrain effects upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Teravolt": {
        "description": "Moves ignore the target's Ability when applicable.",
        "triggers": ["Before Move"]
    },
    "Thermal Exchange": {
        "description": "Raises Attack when hit by a Fire-type move and prevents burns.",
        "triggers": ["On Damage Taken", "Always Active"]
    },
    "Thick Fat": {
        "description": "Halves damage from Fire- and Ice-type moves.",
        "triggers": ["On Damage Taken"]
    },
    "Tinted Lens": {
        "description": "Doubles the power of not very effective moves.",
        "triggers": ["Before Move"]
    },
    "Torrent": {
        "description": "Boosts the power of Water-type moves when HP is low.",
        "triggers": ["On HP Threshold"]
    },
    "Tough Claws": {
        "description": "Boosts the power of contact moves.",
        "triggers": ["Before Move"]
    },
    "Toxic Boost": {
        "description": "Boosts physical attacks while poisoned.",
        "triggers": ["Always Active"]
    },
    "Toxic Chain": {
        "description": "May badly poison a target after damaging it.",
        "triggers": ["After Move"]
    },
    "Toxic Debris": {
        "description": "Scatters Toxic Spikes when hit by a physical move.",
        "triggers": ["On Damage Taken"]
    },
    "Trace": {
        "description": "Copies an opposing Pokémon's Ability upon entering battle.",
        "triggers": ["On Switch-In"]
    },
    "Transistor": {
        "description": "Boosts the power of Electric-type moves.",
        "triggers": ["Always Active"]
    },
    "Triage": {
        "description": "Gives increased priority to healing moves.",
        "triggers": ["Before Move"]
    },
    "Truant": {
        "description": "Only allows the Pokémon to act every other turn.",
        "triggers": ["Before Move"]
    },
    "Turboblaze": {
        "description": "Moves ignore the target's Ability when applicable.",
        "triggers": ["Before Move"]
    }


    ,
    "Unaware": {
        "description": "Ignores the target's stat changes when attacking and ignores the attacker's stat changes when defending.",
        "triggers": ["Before Move", "On Damage Taken"]
    },
    "Unburden": {
        "description": "Doubles Speed after the Pokémon consumes or loses its held item.",
        "triggers": ["After Item Use"]
    },
    "Unnerve": {
        "description": "Prevents opposing Pokémon from eating Berries.",
        "triggers": ["Always Active"]
    }


    ,
    "Wandering Spirit": {
        "description": "Swaps Abilities with a Pokémon that makes contact.",
        "triggers": ["On Contact"]
    },
    "Water Absorb": {
        "description": "Grants immunity to Water-type moves and restores HP when hit by one.",
        "triggers": ["On Damage Taken"]
    },
    "Water Bubble": {
        "description": "Boosts Water-type moves, prevents burns, and halves Fire-type damage.",
        "triggers": ["Always Active", "On Damage Taken"]
    },
    "Water Compaction": {
        "description": "Sharply raises Defense when hit by a Water-type move.",
        "triggers": ["On Damage Taken"]
    },
    "Water Veil": {
        "description": "Prevents the Pokémon from being burned.",
        "triggers": ["Always Active"]
    },
    "Weak Armor": {
        "description": "Lowers Defense and raises Speed when hit by a physical move.",
        "triggers": ["On Damage Taken"]
    },
    "Well-Baked Body": {
        "description": "Grants immunity to Fire-type moves and sharply raises Defense when hit by one.",
        "triggers": ["On Damage Taken"]
    },
    "White Smoke": {
        "description": "Prevents other Pokémon from lowering this Pokémon's stats.",
        "triggers": ["Always Active"]
    },
    "Wimp Out": {
        "description": "Forces the Pokémon to switch out when its HP drops below half.",
        "triggers": ["On HP Threshold"]
    },
    "Wind Rider": {
        "description": "Grants immunity to wind moves and raises Attack when affected by one or Tailwind.",
        "triggers": ["On Move Targeted", "On Field Effect"]
    },
    "Wonder Guard": {
        "description": "Only super-effective moves can damage the Pokémon.",
        "triggers": ["On Damage Taken"]
    },
    "Wonder Skin": {
        "description": "Makes status moves used against the Pokémon less accurate.",
        "triggers": ["On Status Move Targeted"]
    },
    "Zen Mode": {
        "description": "Changes Darmanitan's form when its HP falls below half.",
        "triggers": ["On HP Threshold"]
    }

}