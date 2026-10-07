# A route that brings it all together

The form posts `check_in`, `nights` and `occupants`. The route (which is protected by `@login_required`):

1. reads the form values, converting `nights` and `occupants` with `int(...)` (`check_in` stays as text)
2. calls `create_booking(...)` with the logged-in user's id (`g.user["id"]`)
3. shows errors with `flash()` and the form again, or redirects to the confirmation page.

`bookings.py` is complete and locked. Read it to see what `create_booking` can raise.

## Task
Complete the POST branch of `book(room_id)`:
- wrap the conversion and the `create_booking(...)` call in `try`
- catch both problems with `except (KeyError, ValueError) as error:`. `request.form["nights"]` raises a `KeyError` if
  the field is missing, and `int("abc")` or `create_booking` raise a `ValueError`
- in the `except`, flash `Could not book: ERROR` (error), where ERROR is the exception's message, for example
  `flash(f"Could not book: {error}", "error")`, and let the form show again
- on success flash `Booking confirmed` (success) and redirect to the confirmation page with
  `url_for("views.booking_confirmation", booking_id=booking_id)`. `url_for` fills the id into the URL for you.
