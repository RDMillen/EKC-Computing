# Extension: prices that change with the calendar

Summer costs more than January. A `price_rules` table could hold `start_date`, `end_date` and `multiplier`.

## The hard part
A stay can span two seasons (e.g. 29 Aug to 3 Sep). Decide and document:
- is the price calculated per night using the rule for that night, or once, using the check-in date?
- what happens when two rules overlap?
- how do you test the boundary night between two seasons?

Write the rule down in your own project's `README.md`, build the function so it is testable without a database (pass the rules in as data),
then write boundary tests first.
