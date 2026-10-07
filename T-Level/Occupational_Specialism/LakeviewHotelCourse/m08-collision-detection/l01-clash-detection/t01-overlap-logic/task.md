# The double-booking problem

Two guests must never have the same room on the same night. Before saving (or changing) a booking you must check the
requested dates against the bookings already stored for that room.

## Stays are half-open intervals
A stay from `check_in` to `check_out` occupies the nights `check_in ... check_out - 1`. The guest leaves in the morning of
`check_out`, so the next guest may arrive that same day.

In the chart below, each `#` is one night in the room. The dates in brackets are check-in to check-out, so the
existing booking (check in 1 Nov, check out 4 Nov) uses the nights of 1, 2 and 3 November. Two stays clash when
they both have a `#` in the same column.

```
Night of                 28 29 30 31  1  2  3  4  5
existing (1 to 4 Nov)     .  .  .  .  #  #  #  .  .
new A (1 to 3 Nov)        .  .  .  .  #  #  .  .  .   clash
new B (3 to 6 Nov)        .  .  .  .  .  .  #  #  #   clash
new C (30 Oct to 6 Nov)   .  .  #  #  #  #  #  #  #   clash (surrounds)
new D (4 to 6 Nov)        .  .  .  .  .  .  .  #  #   OK (back-to-back)
new E (28 Oct to 1 Nov)   #  #  #  #  .  .  .  .  .   OK (back-to-back)
```

## The rule
Two intervals overlap exactly when each one starts before the other ends:

```
new_check_in < existing_check_out   AND   new_check_out > existing_check_in
```
Using `<` and `>` (not `<=` and `>=`) is what allows back-to-back bookings.

## In SQL
```sql
SELECT COUNT(*) FROM bookings
WHERE room_id = ? AND check_in < ? AND check_out > ?
```
with the parameters `(room_id, new_check_out, new_check_in)`. Note the order: the new check-out is compared
with the existing check-in.

## Editing a booking
When editing booking 7, its old dates are still in the table, so moving it by one day would clash with itself.
The check must leave booking 7 out. Task 8.1.4 shows how to write this safely in SQL.

## Your notes
Draw three of your own timelines (one clash, one back-to-back, one booking being edited) in the notes file
or on paper, and keep them. They make good evidence of your design thinking.
