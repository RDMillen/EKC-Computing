# Changing and removing rows

```sql
UPDATE guests SET name = ? WHERE id = ?
DELETE FROM guests WHERE id = ?
```

> Always include a `WHERE` clause. `UPDATE rooms SET price_per_night = 0` changes *every* row.
> `DELETE FROM bookings` empties the whole table.

## Task
Write three statements, each using `?` parameters:
- `UPDATE_ROOM_PRICE`: set `price_per_night` (first parameter) for the room with a given `number` (second parameter).
- `MARK_ROOM_UNAVAILABLE`: set `available = 0` for the room with a given `number`.
- `DELETE_BOOKING`: delete the booking with a given `id`.
