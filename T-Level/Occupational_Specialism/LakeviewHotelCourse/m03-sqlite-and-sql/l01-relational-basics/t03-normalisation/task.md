# From one big table to three

A first attempt at the hotel database might put everything in one table:

| booking_id | guest_name | guest_email | room_number | room_type | room_price | check_in | nights |
|---|---|---|---|---|---|---|---|
| 1 | James Sunderland | james@example.com | 101 | Single | 80 | 2026-11-01 | 3 |
| 2 | Mary Sunderland | mary@example.com | 201 | Family | 180 | 2026-11-10 | 2 |
| 3 | James Sunderland | james@example.com | 101 | Single | 80 | 2026-12-01 | 2 |

Problems: James's details are repeated, and if room 101's price changes you must update many rows
(update anomaly). Deleting Mary's only booking would lose her details (deletion anomaly).

The normalised `bookings` table you design later stores a `check_out` date instead of `nights`. You can always work
out the number of nights from the two dates, and storing both dates makes it much easier to check for clashing
bookings in Module 8.

## Normal forms in brief
- 1NF: every cell holds one value; no repeating groups.
- 2NF: (1NF) and no column depends on only *part* of a composite key.
- 3NF: (2NF) and no column depends on another non-key column (no transitive dependency).
  Here `room_type` and `room_price` depend on `room_number`, not on `booking_id`.

## Task
In `normalisation.md`:
1. Identify each repeated or transitive dependency in the flat table.
2. Show the three tables you end up with (`users`, `rooms`, `bookings`) and mark the PK and FK of each.
3. Explain in two sentences why this design is easier to maintain.
