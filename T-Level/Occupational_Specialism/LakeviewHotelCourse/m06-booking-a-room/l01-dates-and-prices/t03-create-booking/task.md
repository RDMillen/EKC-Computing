# From rules to a database row

`create_booking()` brings the earlier pieces together. It receives a database connection and the booking details,
checks the rules, works out the check-out date and price, saves the row, and returns the new booking's id.

Rules to enforce (raise `ValueError` with these messages):
- room does not exist: `That room does not exist`
- room not available (`available` is 0): `That room is not available`
- more guests than the room's capacity: `That room sleeps at most N guests`, where N is the room's capacity,
  for example `That room sleeps at most 2 guests`

Start by loading the room with `SELECT * FROM rooms WHERE id = ?` and `fetchone()`.

Then:
1. `check_out = add_nights(check_in, nights)`
2. `total = calculate_price(room["price_per_night"], nights, occupants)`
3. `INSERT` into `bookings` with `?` parameters, `commit()`, and `return cursor.lastrowid`.

Validate before inserting, so a failed booking leaves no half-written data.
`create_booking` receives the room's `id`, not its number. In the seed data: id 1 = room 101 (sleeps 1),
id 2 = room 102 (unavailable), id 3 = room 103 (sleeps 2), id 4 = room 201 (sleeps 4), id 5 = room 312 (sleeps 3).
