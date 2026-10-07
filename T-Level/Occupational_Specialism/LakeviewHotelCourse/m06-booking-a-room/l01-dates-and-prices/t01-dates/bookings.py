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
