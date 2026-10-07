# Dates in Python

Python's `datetime` module can parse and calculate with dates:

```python
from datetime import date, timedelta

d = date.fromisoformat("2026-12-30")      # text -> date   (raises ValueError if invalid)
later = d + timedelta(days=3)              # date arithmetic
later.isoformat()                          # date -> "2027-01-02"
(date(2027, 1, 2) - d).days                # difference in days -> 3
```
We store dates as ISO text (`YYYY-MM-DD`), and a booking stores `check_in` and `check_out`. A stay of 3 nights
starting on 1 November checks out on 4 November.

Let Python do the calendar maths: months have different lengths and leap years exist.

## Task
In `bookings.py` complete:
- `add_nights(check_in, nights)`: return the check-out date as ISO text
- `nights_between(check_in, check_out)`: return the number of nights as an `int`.
