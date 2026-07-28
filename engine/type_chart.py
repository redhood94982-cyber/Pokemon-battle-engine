"""
Pokemon Battle Engine
type_chart.py

Generation 6+ type effectiveness.
"""

TYPE_CHART = {
    "Normal": {
        "Rock": 0.5,
        "Ghost": 0.0,
        "Steel": 0.5,
    },

        "Fire": {
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 2.0,
        "Ice": 2.0,
        "Bug": 2.0,
        "Rock": 0.5,
        "Dragon": 0.5,
        "Steel": 2.0,
    },

        "Water": {
        "Fire": 2.0,
        "Water": 0.5,
        "Grass": 0.5,
        "Ground": 2.0,
        "Rock": 2.0,
        "Dragon": 0.5,
    },

    "Grass": {
        "Fire": 0.5,
        "Water": 2.0,
        "Grass": 0.5,
        "Poison": 0.5,
        "Ground": 2.0,
        "Flying": 0.5,
        "Bug": 0.5,
        "Rock": 2.0,
        "Dragon": 0.5,
        "Steel": 0.5,
    },
}