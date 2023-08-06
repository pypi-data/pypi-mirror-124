"""Conversions used:
Fahrenheit Subtract 32, then multiply by 5/9ths Celsius
Celsius Multiply by 9/5ths, then add 32 Fahrenheit"""


def centigrade_to_fahrenheit(centigrade: float) -> float:
    return (centigrade * (9 / 5)) + 32


def fahrenheit_to_centigrade(fahrenheit: float) -> float:
    return (fahrenheit - 32) * (5 / 9)
