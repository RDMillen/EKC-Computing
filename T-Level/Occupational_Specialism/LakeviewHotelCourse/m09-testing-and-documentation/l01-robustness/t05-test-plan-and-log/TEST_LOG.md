# Test log: Lakeview Hotel booking system

## Test plan and results

| No. | Feature / requirement | Test description | Test data | Kind (valid / valid extreme / invalid / invalid extreme / erroneous) | Expected result | Actual result | Pass / Fail | Evidence (screenshot or unit test) | Fix and re-test |
|-----|-----------------------|------------------|-----------|-----------------------------------------------------------------------|-----------------|---------------|-------------|------------------------------------|-----------------|
| 1   | Price calculation | 3 nights, 2 guests, rate 100 | 100, 3, 2 | valid | 300.00 | | | `test_pricing.py`: `test_two_guests_pay_the_base_rate` | |
| 2   | Price calculation | 3 guests, first extra guest | 100, 2, 3 | valid extreme | 220.00 | | | | |
| 3   | Booking form | 0 nights | nights = 0 | invalid extreme | message: Nights must be between 1 and 30 | | | | |
| 4   | Booking form | text instead of a number | nights = "abc" | erroneous | message: Nights must be a whole number | | | | |
| 5   | Collision | stay starts on another guest's check-out day | 4 Nov to 6 Nov, other booking 1 to 4 Nov | valid extreme | booking accepted | | | | |
| 6   | Security | SQL injection text in the room type field | `x'); DROP TABLE rooms;--` | erroneous | saved as plain text, tables intact | | | | |
| 7   | Security | open another user's booking by changing the URL | /bookings/ID of another user | invalid | 403 Forbidden | | | | |

## Summary
- Number of tests:
- Passed first time:
- Failures found and fixed:
- Areas I have not tested, and why:
