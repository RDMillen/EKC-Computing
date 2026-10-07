# Querying data

```sql
SELECT name, email
FROM guests
WHERE email LIKE ?          -- filter rows
ORDER BY name ASC           -- sort the result
```
`AND` / `OR` combine conditions. `ORDER BY ... DESC` sorts largest first.

Before running your queries, the tests fill the database with sample rows. This sample data is called seed data.
It contains five rooms (101, 102, 103, 201 and 312), and one of them (102) is unavailable.

## Task
- `AVAILABLE_ROOMS`: columns `number, room_type, price_per_night` for rooms where `available = 1`, cheapest first.
- `ROOMS_FOR_PARTY`: the `number` of available rooms with `capacity >= ?` and `price_per_night <= ?`
  (two parameters, in that order), most expensive first.
