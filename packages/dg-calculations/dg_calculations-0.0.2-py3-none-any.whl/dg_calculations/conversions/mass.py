"""Conversions used:
1 grain = 0.05 scruples = 0.016667 drams = 0.00208 ounces
1 ounce = 28.3495 grams
1 gram = 0.03527396 ounces
1 pound = 16 oz = 0.4535924 kilograms
1 kilogram = 2.2046223 pounds
1 short ton = 0.892857 metric ton
1 metric ton = 1.1200 short tons
1 long ton = 1.01605 metric tons"""

# TODO: 1 grain = 0.05 scruples = 0.016667 drams = 0.00208 ounces ... wtf?


def ounces_to_grams(ounces: float) -> float:
    return ounces * 28.3495


def grams_to_ounces(grams: float) -> float:
    return grams * 0.03527396


def pounds_to_ounces(pounds: float) -> float:
    return pounds * 16


def pounds_to_kilograms(pounds: float) -> float:
    return pounds * 0.4535924


def kilograms_to_pounds(kilograms: float) -> float:
    return kilograms * 2.2046223


def short_tons_to_metric_tons(tons: float) -> float:
    return tons * 0.892857


def metric_tons_to_short_tons(tons: float) -> float:
    return tons * 1.1200


def longs_tons_to_metric_tons(tons: float) -> float:
    return tons * 1.01605
