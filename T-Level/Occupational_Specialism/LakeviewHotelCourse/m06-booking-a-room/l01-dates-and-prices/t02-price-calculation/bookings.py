"""Booking rules: dates, prices and clashes. Pure Python plus SQL, no Flask."""
from datetime import date, timedelta

BASE_OCCUPANCY = 2            # guests covered by the nightly rate
EXTRA_GUEST_PER_NIGHT = 10.0  # supplement for each guest above BASE_OCCUPANCY, per night


def add_nights(check_in, nights):
    """Return the check-out date (ISO text) for a stay starting on check_in."""
    return (date.fromisoformat(check_in) + timedelta(days=nights)).isoformat()


def nights_between(check_in, check_out):
    """Return how many nights lie between two ISO dates."""
    return (date.fromisoformat(check_out) - date.fromisoformat(check_in)).days


def calculate_price(price_per_night, nights, occupants):
    """Total price: nightly rate covers 2 guests, each extra guest adds a supplement per night."""
    if nights < 1:
        raise ValueError("Stay must be at least one night")
    if occupants < 1:
        raise ValueError("At least one occupant is required")
    extra_guests = max(0, occupants - BASE_OCCUPANCY)
    nightly = price_per_night + extra_guests * EXTRA_GUEST_PER_NIGHT
    return round(nightly * nights, 2)
