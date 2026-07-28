from engine.pokemon import Pokemon
from engine.move import Move
from engine.team import Team
from engine.battle import Battle

flamethrower = Move(
    name="Flamethrower",
    move_type="Fire",
    category="Special",
    power=90,
    accuracy=100,
)

charizard = Pokemon(
    species="Charizard",
    level=50,
    types=("Fire", "Flying"),
    hp=153,
    attack=84,
    defense=78,
    special_attack=109,
    special_defense=85,
    speed=100,
    moves=[flamethrower],

team1 = Team([charizard])
team2 = Team([venusaur])

battle = Battle(team1, team2)

venusaur = Pokemon(
    species="Venusaur",
    level=50,
    types=("Grass", "Poison"),
    hp=155,
    attack=82,
    defense=83,
    special_attack=100,
    special_defense=100,
    speed=80,
    moves=[],
)
)

battle.start()

for entry in battle.state.log_entries:
    print(entry)