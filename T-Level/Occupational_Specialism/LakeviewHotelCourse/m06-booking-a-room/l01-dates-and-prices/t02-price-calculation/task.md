# A pricing rule you can test

Business rules belong in small, testable functions with no web or database code in them.

The hotel's rule
- the nightly rate covers up to 2 guests
- each guest above 2 adds £10 per night
- total = (nightly rate + extra guest supplement) x number of nights, rounded to 2 decimal places
- a stay must be at least 1 night and have at least 1 guest, otherwise raise `ValueError`

Examples: rate £100, 3 nights, 2 guests = £300.00. Rate £100, 2 nights, 4 guests = (100 + 2 x 10) x 2 = £240.00.

Work out the number of extra guests first: `occupants - BASE_OCCUPANCY`, but never less than 0, because 1 guest
does not earn a discount. `max(0, ...)` does this in one step.

Use `round(value, 2)` for money. Think about what happens at the boundaries: exactly 2 guests, 3 guests,
1 night, 0 nights. Those are the values a tester picks.

## Task
Complete `calculate_price(price_per_night, nights, occupants)`. The constants `BASE_OCCUPANCY` and
`EXTRA_GUEST_PER_NIGHT` are defined at the top of the file. Use them instead of typing `2` and `10.0`.
