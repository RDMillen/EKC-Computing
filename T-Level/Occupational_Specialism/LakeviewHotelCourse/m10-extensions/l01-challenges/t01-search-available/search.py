def find_available_rooms(db, check_in, check_out, occupants):
    """Rooms that sleep `occupants` people and are free for every night of the stay, cheapest first."""
    return db.execute(
        "SELECT * FROM rooms r "
        "WHERE r.available = 1 AND r.capacity >= ? "
        "AND NOT EXISTS ("
        "  SELECT 1 FROM bookings b "
        "  WHERE b.room_id = r.id AND b.check_in < ? AND b.check_out > ?"
        ") ORDER BY r.price_per_night",
        (occupants, check_out, check_in),
    ).fetchall()
