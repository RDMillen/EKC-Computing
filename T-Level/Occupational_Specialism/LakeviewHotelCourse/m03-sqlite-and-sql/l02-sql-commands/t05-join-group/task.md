# Combining tables

Foreign keys let you join tables back together:

```sql
SELECT b.id, u.name
FROM bookings b
JOIN users u ON u.id = b.user_id
```
`bookings b` gives the table a short alias, `b`, so `b.id` means the `id` column of `bookings`. Aliases save typing
and make it clear which table a column comes from when two tables share a column name such as `id`.

- `JOIN` (inner join) keeps only rows that match on both sides.
- `LEFT JOIN` keeps every row from the left table (the one after `FROM`), even with no match. The right-hand columns
  are `NULL` for those rows, and `COUNT(b.id)` counts them as 0.
- `GROUP BY` with `COUNT()` summarises rows per group.

`GROUP BY` puts the rows into groups and `COUNT` counts each group. Using the tables from task 3.2.1:

```sql
SELECT g.name, COUNT(o.id) AS order_count
FROM guests g
LEFT JOIN orders o ON o.guest_id = g.id
GROUP BY g.id
```
This lists every guest with their number of orders, including guests with none.

For `ROOM_BOOKING_COUNTS`, start `FROM rooms` so that rooms with no bookings are kept.

## Task
- `BOOKING_DETAILS`: columns in this order: `b.id, u.name, r.number, b.check_in, b.check_out, b.total_price`,
  joining `bookings`, `users` and `rooms`, sorted by `check_in`.
- `ROOM_BOOKING_COUNTS`: each room's `number` and how many bookings it has (`COUNT(b.id)`), including rooms with zero bookings,
  sorted by room number.
