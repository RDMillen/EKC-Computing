# Edit forms start pre-filled

An edit page works like the booking form, but it starts with the existing values, and only the owner may use it.

Which HTTP status for which problem?
- 404 Not Found: there is no booking with that id
- 403 Forbidden: the booking exists, but it is not yours

The template (`edit_booking.html`) already prints the current dates and guests, and the code at the bottom of the
route works out the number of nights with `nights_between`.

## Task
Complete `edit_booking(booking_id)`. The booking was already loaded for you:
1. `abort(404)` if `booking is None`
2. `abort(403)` if `booking["user_id"]` is not the logged-in user's id
3. on POST call `update_booking(...)`. On `KeyError` or `ValueError` flash `Could not update: ERROR` (error),
   in the same way as the booking form
4. on success flash `Booking updated` (success) and redirect to
   `url_for("views.booking_confirmation", booking_id=booking_id)`.

You do not need to catch `LookupError` or `PermissionError` here. Steps 1 and 2 have already dealt with a missing
booking and someone else's booking, so `update_booking` will not raise them.
