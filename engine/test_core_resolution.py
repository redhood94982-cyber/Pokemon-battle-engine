"""Core regression tests for action selection and turn ordering."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine import Battle, Pokemon


def mon(name, speed, move="Protect", nature="Hardy", ability="Inner Focus"):
    return Pokemon(
        species=name, level=50,
        types=["Normal"], ability=ability, item=None, nature=nature,
        base_stats={"hp": 100, "attack": 100, "defense": 100, "special_attack": 100, "special_defense": 100, "speed": speed},
        ivs={"hp": 31, "attack": 31, "defense": 31, "special_attack": 31, "special_defense": 31, "speed": 31},
        evs={"hp": 0, "attack": 0, "defense": 0, "special_attack": 0, "special_defense": 0, "speed": 252},
        moves=[move],
    )


def test_missing_selection_is_rejected():
    b = Battle()
    p1 = [mon("Gengar", 110)]; p2 = [mon("Gengar", 110)]
    # register_teams requires six; this test uses direct actives.
    b.active_p1, b.active_p2 = p1, p2
    try:
        b.perform_turn({})
    except ValueError:
        return
    raise AssertionError("Engine must not invent an action.")


def test_speed_order_and_priority():
    b = Battle()
    fast = mon("Gengar", 110, "Protect")
    slow = mon("Gengar", 80, "Protect")
    b.active_p1 = [fast, mon("Gengar", 70, "Protect")]
    b.active_p2 = [slow, mon("Gengar", 60, "Protect")]
    order = b.get_turn_order({id(fast): 0, id(slow): 0, id(b.active_p1[1]): 0, id(b.active_p2[1]): 3})
    assert order[0] is b.active_p2[1]
    assert order[1] is fast


def test_weather_speed_ability():
    b = Battle()
    swimmer = mon("Gengar", 70, "Protect", ability="Swift Swim")
    swimmer._battle_side = 1
    b.active_p1 = [swimmer]
    b.active_p2 = [mon("Gengar", 100, "Protect")]
    b.state.weather = "rain"
    order = b.get_turn_order({id(swimmer): 0, id(b.active_p2[0]): 0})
    assert order[0] is swimmer


if __name__ == "__main__":
    test_missing_selection_is_rejected()
    test_speed_order_and_priority()
    test_weather_speed_ability()
    print("Core engine tests passed.")
