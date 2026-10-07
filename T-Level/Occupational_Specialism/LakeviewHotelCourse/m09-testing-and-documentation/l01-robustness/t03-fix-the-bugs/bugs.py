"""Three bugs have been planted in this file. Use the failing tests to find and fix them."""
from datetime import date


def nights_between(check_in, check_out):
    """Number of nights between two ISO dates."""
    return (date.fromisoformat(check_out) - date.fromisoformat(check_in)).days


def calculate_price(price_per_night, nights, occupants):
    """Nightly rate covers 2 guests; each extra guest adds 10.00 per night."""
    extra_guests = max(0, occupants - 2)
    return round((price_per_night + extra_guests * 10.0) * nights, 2)


def overlaps(a_start, a_end, b_start, b_end):
    """True if two half-open stays [start, end) share at least one night."""
    return a_start < b_end and a_end > b_start
