"""Conversions used:
1 teaspoon = 5 milliliters
1 milliliter = 0.0338147 fluid ounces
1 tablespoon = 15 milliliters
1 liter = 2.11342 pints = 1000 cubic centimeters
1 fluid ounce = 30 milliliters
1 liter = 1.05671 quarts = 0.264178 gallons
1 gallon = 3.785332 liters = 231 cubic inches
1 cup = 0.23658 liters
1 pint = 0.473167 liters
1 cubic meter = 35.3144 cubic feet = 1.30794 cubic yards
1 cubic foot = 0.0283170 cubic meters
1 cubic yard = 0.764559 cubic meters"""


def teaspoons_to_millimetres(teaspoons: float) -> float:
    return teaspoons * 5


def millimetres_to_fluid_ounces(millinetres: float) -> float:
    return millinetres * 0.0338147


def tablespoons_to_millimetres(tablespoons: float) -> float:
    return tablespoons * 15


def litres_to_pints(litres: float) -> float:
    return litres * 2.11342


def litres_to_cubic_centimetres(litres: float) -> float:
    return litres * 1000


def pints_to_cubic_centimetres(pints: float) -> float:
    return pints * 473.167


def fluid_ounces_to_millimetres(ounces: float) -> float:
    return ounces * 30


def litres_to_quarts(litres: float) -> float:
    return litres * 1.05671


def gallons_to_litres(gallons: float) -> float:
    return gallons * 3.785332


def cups_to_litres(cups: float) -> float:
    return cups * 0.23658


def pints_to_litres(pints: float) -> float:
    return pints * 0.473167


def cubic_metres_to_cubic_feet(metres: float) -> float:
    return metres * 35.3144


def cubic_feet_to_cubic_metres(feet: float) -> float:
    return feet * 0.0283170


def cubic_yards_to_cubic_metres(yards: float) -> float:
    return yards * 0.764559
