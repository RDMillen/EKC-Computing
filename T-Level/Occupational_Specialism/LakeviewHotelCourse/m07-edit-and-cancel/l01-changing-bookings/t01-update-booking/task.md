# Changing a booking safely

Editing is riskier than creating: you must make sure the booking exists and belongs to the user, and
the price must be recalculated with the new nights and guests. Three different failures deserve three
different exceptions, so the route can respond properly. All three are built into Python, so you do not need to
import or define them:

| Situation | Exception |
|---|---|
| booking id not found | `LookupError("Booking not found")` |
| booking belongs to someone else | `PermissionError("You can only change your own bookings")` |
| more guests than the room allows | `ValueError("That room sleeps at most N guests")` |

## Task
Complete `update_booking(...)`:
1. load the booking with `get_booking(db, booking_id)`. Raise `LookupError` if it is `None`
2. raise `PermissionError` if `booking["user_id"]` is not `user_id`
3. load the room with `SELECT * FROM rooms WHERE id = ?` using `booking["room_id"]`, because the booking row does not
   hold the room's capacity or price. Raise `ValueError` if `occupants` is more than the capacity
4. work out the new `check_out` with `add_nights` and the new total with `calculate_price`
5. `UPDATE` the booking's `check_in`, `check_out`, `occupants` and `total_price` (`WHERE id = ?`), then `commit()`
`get_booking(db, booking_id)` already exists in the file. It returns the booking row (including `user_id` and
`room_id`) or `None`. Check in the order shown in the table: you cannot check who owns a booking that does not exist.
