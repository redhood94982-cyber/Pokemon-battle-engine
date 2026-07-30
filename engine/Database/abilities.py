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
    }


    ,
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

}