# Never trust the browser

Everything sent by a browser can be wrong or malicious. A friendly error is better than a crash with the
message `invalid literal for int()`.

Complete `validate_booking_form(form, today=None)` in `validation.py`. It returns a list of error messages (an empty list when everything is fine)
and reports every problem, not just the first.

| Field | Rule | Message |
|---|---|---|
| `check_in` | must be a real date as `YYYY-MM-DD` | `Please enter the check-in date as YYYY-MM-DD` |
| `check_in` | must not be before `today` (use `date.today()` if `today` is `None`) | `Check-in cannot be in the past` |
| `nights` | must be a whole number | `Nights must be a whole number` |
| `nights` | between 1 and `MAX_NIGHTS` (30) | `Nights must be between 1 and 30` |
| `occupants` | must be a whole number | `Occupants must be a whole number` |
| `occupants` | at least 1 | `At least one occupant is required` |

Use `form.get("check_in", "")` so a missing field is treated as invalid, not as a crash.

Each field has two rules, and the second only makes sense if the first passed: you cannot check whether `"abc"`
is between 1 and 30. Use `try`, `except ValueError` and `else` for each field, and put the second check in the `else`.
`date.fromisoformat` and `int` both raise `ValueError` for bad input, including an empty string.
The `today` parameter exists so a test can pick a fixed date. This is a useful technique called dependency injection.

The routes in `views.py` (locked) already call your function and flash every message. Look at `book()`: because
the form is checked first, the route no longer needs to catch `KeyError`, and each message is flashed on its own,
without the `Could not book:` prefix from task 6.2.1.
