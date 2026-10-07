# Destructive actions use POST

Deleting data must never be a plain link (`GET`). Browsers, search engines and prefetching tools follow
links automatically. Use a form with `method="post"` and restrict the route:

```python
@views.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
```
A `GET` request to this URL then receives 405 Method Not Allowed. The Cancel button on the
"My bookings" page is already a small POST form.

## Task
Complete `cancel_booking(booking_id)`:
1. fetch the booking with `get_booking`; `abort(404)` if missing and `abort(403)` if it is not the user's
2. `DELETE FROM bookings WHERE id = ?`, then commit
3. flash `Booking cancelled` (success) and redirect to `url_for("views.my_bookings")`.
