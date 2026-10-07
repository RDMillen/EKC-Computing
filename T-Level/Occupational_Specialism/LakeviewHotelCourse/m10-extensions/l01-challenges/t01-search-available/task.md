# Extension: what is free for these dates?

Guests normally search by dates and party size first. Write `find_available_rooms(db, check_in, check_out, occupants)`
in `search.py`. It returns every room (as `sqlite3.Row` objects, cheapest first) that:
- is marked `available = 1`
- has `capacity >= occupants`
- has no booking that overlaps `[check_in, check_out)` (same rule as Module 8; back-to-back is fine)

A `NOT EXISTS` sub-query is the natural fit:

```sql
SELECT * FROM rooms r
WHERE ... AND NOT EXISTS (SELECT 1 FROM bookings b WHERE b.room_id = r.id AND ...)
```
