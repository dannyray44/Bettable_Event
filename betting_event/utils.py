import math


def american_to_decimal(american_odds: int) -> float:
    """Converts American odds to decimal odds."""
    if american_odds >= 100:
        decimal_odds = 1 + (american_odds / 100)
    else:
        decimal_odds = (100 / abs(american_odds)) + 1
    return round(decimal_odds, 2)

def decimal_to_american(decimal_odds: float) -> int:
    """Converts decimal odds to American odds."""
    if decimal_odds >= 2:
        american_odds = (decimal_odds - 1) * 100
    else:
        american_odds = -100 / (decimal_odds - 1)
    return int(american_odds)

def fractional_to_decimal(fractional_odds: str) -> float:
    """Converts fractional odds to decimal odds."""
    numerator, denominator = map(int, fractional_odds.split('/'))
    decimal_odds = 1 + (numerator / denominator)
    return round(decimal_odds, 2)

def decimal_to_fractional(decimal_odds: float) -> str:
    """Converts decimal odds to fractional odds. Ensuring the fraction is in its simplest form."""
    numerator = decimal_odds - 1
    denominator = 1
    while not numerator.is_integer():
        numerator *= 10
        denominator *= 10
    numerator = int(numerator)
    denominator = int(denominator)
    gcd = math.gcd(numerator, denominator)
    numerator /= gcd
    denominator /= gcd
    return f'{int(numerator)}/{int(denominator)}'
