"""Conversions used:
1 sq. inch = 6.4516 sq. centimeters
1 sq. centimeter = 0.1550 sq. inches
1 sq. foot = 0.0929 sq. meters
1 sq. meter = 1.195986 sq. yards
1 sq. yard = 0.83613 sq. meters
1 sq. kilometer = 0.386101 sq. miles
1 sq. mile = 2.589999 sq. kilometers
1 hectare = 2.471044 acres
1 acre = 0.404687 hectares"""


def square_inches_to_square_centimetres(inches: float) -> float:
    return inches * 6.4516


def square_centimetres_to_square_inches(centimetres: float) -> float:
    return centimetres * 0.1550


def square_feet_to_square_metres(feet: float) -> float:
    return feet * 0.0929


def square_metres_to_square_yards(metres: float) -> float:
    return metres * 1.195986


def square_yards_to_square_metres(yards: float) -> float:
    return yards * 0.83613


def square_kilometres_to_square_miles(kilometres: float) -> float:
    return kilometres * 0.386101


def square_miles_to_square_kilometres(miles: float) -> float:
    return miles * 2.589999


def hectares_to_acres(hectares: float) -> float:
    return hectares * 2.471044


def acres_to_hectares(acres: float) -> float:
    return acres * 0.404687
