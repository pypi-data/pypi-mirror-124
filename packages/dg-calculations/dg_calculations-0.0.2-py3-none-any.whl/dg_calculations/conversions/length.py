"""Conversions used:
1 inch = 2.540 centimeters
1 millimeter = 0.03937 inches
1 foot = 30.4878 centimeters
1 centimeters = 0.3937 inches
1 yard = 0.9144028 meters
1 meter = 3.281 feet
1 mile = 1.6093419 kilometer
1 kilometer = 0.621372 miles"""


def inches_to_centimetres(inches: float) -> float:
    return inches * 2.54


def millimetres_to_inches(millimetres: float) -> float:
    return millimetres * 0.03937


def feet_to_centimetres(feet: float) -> float:
    return feet * 30.4878


def centimetres_to_inches(centimetres: float) -> float:
    return centimetres * 0.3937


def yards_to_metres(yards: float) -> float:
    return yards * 0.9144028


def metres_to_feet(metres: float) -> float:
    return metres * 3.281


def miles_to_kilometres(miles: float) -> float:
    return miles * 1.6093419


def kilometres_to_miles(kilometres: float) -> float:
    return kilometres * 0.621372
