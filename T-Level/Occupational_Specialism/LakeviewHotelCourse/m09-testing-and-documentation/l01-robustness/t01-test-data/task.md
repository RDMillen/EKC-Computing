# Test data that finds bugs

A test plan lists what you test, with which data, and what you expect. The specification groups test data into five kinds:

| Kind | Meaning | Example for "number of nights" (allowed: 1 to 30) |
|---|---|---|
| Valid | normal, accepted data | 3 |
| Valid extreme | the very edge of what is accepted | 1 and 30 |
| Invalid | clearly outside the rules, should be rejected | -2, 45 |
| Invalid extreme | just outside the edge | 0 and 31 |
| Erroneous | the wrong type or nonsense | "abc", 2.5, empty, `'; DROP TABLE` |

Good testers think about boundaries because bugs hide there (`<` vs `<=`). For this system the interesting
boundaries are:
- guests: 1, 2 (base rate), 3 (first extra guest), room capacity, capacity + 1
- nights: 0, 1, 30, 31
- dates: yesterday, today, a leap day (29 Feb), the last day of a month and year
- collisions: identical dates, back-to-back, one night inside, surrounding, a different room

The automated tests in this course already use data like this. Now practise describing tests in the way the
assessment expects.

## Your notes
Pick three rules from your system and list one test of each kind for each (15 tests). You will put them in `TEST_LOG.md` in task 9.1.5.
