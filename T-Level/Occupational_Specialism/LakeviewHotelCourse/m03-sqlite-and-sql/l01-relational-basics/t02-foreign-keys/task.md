# Spot the foreign keys

Here are some rows from the three hotel tables.

`users`

| id | name | email |
|---|---|---|
| 1 | James Sunderland | james@example.com |
| 2 | Mary Sunderland | mary@example.com |

`rooms`

| id | number | room_type | capacity | price_per_night |
|---|---|---|---|---|
| 1 | 101 | Single | 1 | 80.0 |
| 4 | 201 | Family | 4 | 180.0 |

`bookings`

| id | user_id | room_id | check_in | check_out | occupants | total_price |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 2026-11-01 | 2026-11-04 | 1 | 240.0 |
| 2 | 2 | 4 | 2026-11-10 | 2026-11-12 | 3 | 360.0 |
| 3 | 1 | 1 | 2026-12-01 | 2026-12-03 | 1 | 160.0 |

Which columns in the `bookings` table are foreign keys? Select all that apply.
