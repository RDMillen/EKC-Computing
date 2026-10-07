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


def get_booking(db, booking_id):
    """Return one booking (with its room number and type), or None."""
    return db.execute(
        "SELECT b.*, r.number AS room_number, r.room_type "
        "FROM bookings b JOIN rooms r ON r.id = b.room_id WHERE b.id = ?",
        (booking_id,),
    ).fetchone()


def create_booking(db, user_id, room_id, check_in, nights, occupants):
    """Insert a booking and return its id. Raises ValueError for anything invalid."""
    room = db.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()
    if room is None:
        raise ValueError("That room does not exist")
    if not room["available"]:
        raise ValueError("That room is not available")
    if occupants > room["capacity"]:
        raise ValueError("That room sleeps at most %d guests" % room["capacity"])
    check_out = add_nights(check_in, nights)
    total = calculate_price(room["price_per_night"], nights, occupants)
    cursor = db.execute(
        "INSERT INTO bookings (user_id, room_id, check_in, check_out, occupants, total_price) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, room_id, check_in, check_out, occupants, total),
    )
    db.commit()
    return cursor.lastrowid


def update_booking(db, booking_id, user_id, check_in, nights, occupants):
    """Change a booking's dates and guests, recalculating the price.

    Raises LookupError (no such booking), PermissionError (not the owner) or ValueError.
    """
    booking = get_booking(db, booking_id)
    if booking is None:
        raise LookupError("Booking not found")
    if booking["user_id"] != user_id:
        raise PermissionError("You can only change your own bookings")
    room = db.execute("SELECT * FROM rooms WHERE id = ?", (booking["room_id"],)).fetchone()
    if occupants > room["capacity"]:
        raise ValueError("That room sleeps at most %d guests" % room["capacity"])
    check_out = add_nights(check_in, nights)
    total = calculate_price(room["price_per_night"], nights, occupants)
    db.execute(
        "UPDATE bookings SET check_in = ?, check_out = ?, occupants = ?, total_price = ? WHERE id = ?",
        (check_in, check_out, occupants, total, booking_id),
    )
    db.commit()
