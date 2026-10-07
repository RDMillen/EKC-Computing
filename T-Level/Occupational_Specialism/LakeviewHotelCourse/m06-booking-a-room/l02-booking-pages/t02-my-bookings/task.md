# Joining tables for a list page

The page lists the logged-in user's bookings with the room number and type, which live in the `rooms`
table, so you need a `JOIN`:

```sql
SELECT b.id, r.number AS room_number, r.room_type, b.check_in, b.check_out, b.occupants, b.total_price
FROM bookings b
JOIN rooms r ON r.id = b.room_id
WHERE b.user_id = ?
ORDER BY b.check_in
```
`AS room_number` renames a column so the template can read `booking["room_number"]`.

> Filter by `g.user["id"]`, never by an id from the URL or form, so users cannot read each other's bookings.

## Task
Complete `my_bookings()`: run the query for the logged-in user and render `my_bookings.html` with the variable `bookings`.
