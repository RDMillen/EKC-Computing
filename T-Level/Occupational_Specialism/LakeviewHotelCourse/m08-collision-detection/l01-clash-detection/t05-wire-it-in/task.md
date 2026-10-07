# Use the check where it matters

`has_collision` only helps if it is called before a booking is saved. Put the collision check into both places
that write dates:

- `create_booking`: refuse if the new dates clash
- `update_booking`: refuse if the new dates clash with another booking (so pass `exclude_booking_id=booking_id`)

Raise the exception class already defined at the top of the file:
```python
class BookingConflict(ValueError): ...
raise BookingConflict("Those dates are already booked")
```
Because `BookingConflict` is a `ValueError`, the existing routes already catch it and flash the message. You do not
need to change `views.py`.

> Check before saving. A booking saved and then rejected is a bug.

## Task
Replace the two TODO comments in `bookings.py`.
