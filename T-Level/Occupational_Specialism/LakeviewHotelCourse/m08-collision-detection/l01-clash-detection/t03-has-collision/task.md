# Write the collision check

Complete `has_collision(db, room_id, check_in, check_out, exclude_booking_id=None)` in `bookings.py`.
For this task ignore `exclude_booking_id`; you will add it in the next task.

- Count the bookings for `room_id` that overlap the new dates, using the rule from the theory task.
- Return `True` if the count is above zero, otherwise `False`.
- Use `?` parameters. The new `check_out` is compared with the existing `check_in`, and the new `check_in` with the existing `check_out`.

Give the count a name so you can read it from the row:

```python
row = db.execute("SELECT COUNT(*) AS clashes FROM bookings WHERE ...", (...)).fetchone()
row["clashes"]   # a number
```

The seed data has these bookings, all in 2026: room id 1 (room 101) from 1 to 4 Nov and from 1 to 3 Dec, and
room id 4 (room 201) from 10 to 12 Nov. `room_id` is the room's id, not its number.
