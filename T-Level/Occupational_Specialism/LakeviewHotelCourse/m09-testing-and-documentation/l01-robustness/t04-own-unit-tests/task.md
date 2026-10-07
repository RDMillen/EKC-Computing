# Write your own unit tests

The Check button runs tests written for this course. For the assessment you need tests that you wrote yourself,
so you can show what you tested and that it passed. Python's built-in `unittest` module is all you need.

```python
import unittest

from bookings import calculate_price


class TestCalculatePrice(unittest.TestCase):
    def test_two_guests_pay_the_base_rate(self):
        self.assertEqual(300.00, calculate_price(100.0, 3, 2))
```
- A test class inherits from `unittest.TestCase`.
- Every method whose name starts with `test_` is one test.
- `self.assertEqual(expected, actual)` makes the test fail if the two values are different.
- To check that something raises an error, call it inside `with self.assertRaises(ValueError):`.

You can run your tests yourself: right-click `test_pricing.py` and choose Run. PyCharm shows a green tick or a
red cross for each test.

## Task
`bookings.py` (locked) contains the finished `calculate_price` from task 6.1.2. Add at least three more tests to
`test_pricing.py`, so you have four or more in total. Between them, your tests must check that:
1. the first extra guest is charged: rate £100, 2 nights, 3 guests costs £220.00
2. a single guest pays the normal rate, with no discount for being under 2 guests
3. 0 nights raises a `ValueError`

When you press Check, your tests run against the correct `calculate_price` and must all pass. They then run
against four broken versions of it, and each broken version must make at least one of your tests fail.

## Testing a route (optional)
Flask's test client lets you test routes in the same way:
```python
from app import app

client = app.test_client()
response = client.get("/rooms")
self.assertEqual(200, response.status_code)
```
