# DDL: defining tables

DDL (Data Definition Language) commands such as `CREATE TABLE` define the structure of the database.

```sql
CREATE TABLE IF NOT EXISTS guests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_id INTEGER NOT NULL REFERENCES guests (id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    paid INTEGER NOT NULL DEFAULT 0
);
```
`REFERENCES guests (id)` makes `guest_id` a foreign key. `CHECK (...)` rejects values that break a rule, and
`DEFAULT` supplies a value when an `INSERT` leaves the column out. SQLite has no true/false type, so `1` and `0`
are used instead.

## Task
Write the SQL in the `SCHEMA` string to create these three tables. Write it between the triple quotes; the tests run
your SQL against a new, empty database.

users: `id` (PK, autoincrement), `name` (text, required), `email` (text, required, unique), `password_hash` (text, required)

rooms: `id` (PK, autoincrement), `number` (integer, required, unique), `room_type` (text, required), `capacity` (integer, required, greater than 0),
`price_per_night` (real, required, greater than 0), `available` (integer, required, default 1)

bookings: `id` (PK, autoincrement), `user_id` (integer, required, FK to users), `room_id` (integer, required, FK to rooms),
`check_in` (text, required), `check_out` (text, required), `occupants` (integer, required, greater than 0), `total_price` (real, required)
