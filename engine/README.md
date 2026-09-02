# Pokemon-battle-engine

## Battle setup flow

The battle controller does **not** automatically deploy the first two Pokémon on either team.

1. Register each player's complete six-Pokémon team with `register_teams()`.
2. Each player explicitly chooses two leads.
3. Start the battle with `start_battle(player1_leads, player2_leads)`.
4. Switch-in abilities are resolved in Speed order. If multiple weather-setting abilities activate, the later (slower) activation overwrites the earlier weather.
5. The battle can then proceed through the normal turn/action engine.

This keeps team selection and lead selection separate and supports strategic lead choices.
