# DML: adding rows

DML (Data Manipulation Language) commands change the *data*: `INSERT`, `SELECT`, `UPDATE`, `DELETE`.

```sql
INSERT INTO guests (name, email) VALUES (?, ?)
```
The `?` marks are parameters: the values are supplied separately by Python, never pasted into the
text. You will see why this matters in the next lesson.

## Task
Write two `INSERT` statements with `?` parameters:
- `INSERT_ROOM` fills `number, room_type, capacity, price_per_night` (in that order). `available` takes its default.
- `INSERT_USER` fills `name, email, password_hash` (in that order).
