"""
Pokemon Battle Engine
battle_state.py
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BattleState:
    # Turn
    turn: int = 1

    # Weather
    weather: Optional[str] = None
    weather_turns: int = 0

    # Terrain
    terrain: Optional[str] = None
    terrain_turns: int = 0

    # Room effects
    trick_room: bool = False
    trick_room_turns: int = 0

    # Side effects
    reflect_p1: int = 0
    reflect_p2: int = 0

    light_screen_p1: int = 0
    light_screen_p2: int = 0

    aurora_veil_p1: int = 0
    aurora_veil_p2: int = 0

    tailwind_p1: int = 0
    tailwind_p2: int = 0

    # Hazards
    stealth_rock_p1: bool = False
    stealth_rock_p2: bool = False

    spikes_p1: int = 0
    spikes_p2: int = 0

    toxic_spikes_p1: int = 0
    toxic_spikes_p2: int = 0

    sticky_web_p1: bool = False
    sticky_web_p2: bool = False

    last_damage: int = 0

    # Battle log
    battle_log: list[str] = field(default_factory=list)

    def log(self, message: str):
        self.battle_log.append(message)

    def next_turn(self):
        self.turn += 1
        self.log(f"Turn {self.turn}")

    def clear_weather(self):
        self.weather = None
        self.weather_turns = 0

    def clear_terrain(self):
        self.terrain = None
        self.terrain_turns = 0

    def decrement_timers(self):
        timers = [
            "weather_turns",
            "terrain_turns",
            "trick_room_turns",
            "reflect_p1",
            "reflect_p2",
            "light_screen_p1",
            "light_screen_p2",
            "aurora_veil_p1",
            "aurora_veil_p2",
            "tailwind_p1",
            "tailwind_p2",
        ]

        for timer in timers:
            value = getattr(self, timer)

            if value > 0:
                setattr(self, timer, value - 1)