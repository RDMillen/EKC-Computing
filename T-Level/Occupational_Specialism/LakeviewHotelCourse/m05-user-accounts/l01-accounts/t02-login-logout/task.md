# Sessions

A session remembers a user between requests. Flask stores it in a signed cookie (this is why you set
`SECRET_KEY`). The browser sends the cookie back with every request, and Flask checks the signature. Signed is not
the same as encrypted: the user can read what is in the cookie but cannot change it without Flask noticing. This is
another reason to store only the user's id.

```python
session["user_id"] = 5     # remember who logged in
session.get("user_id")     # read it later
session.clear()            # forget everything (log out)
```
The `load_logged_in_user()` function is already written. `@views.before_app_request` makes Flask run it before
every request. It looks up the id stored in the session and puts that user's row in `g.user` (or `None` if nobody
is logged in), so every route and template can use `g.user`.

## Security tips
- Use the same message for "unknown email" and "wrong password" (`Invalid email or password`) so an attacker
  cannot discover which emails are registered.
- Call `session.clear()` before storing the new `user_id`.

## Task
Complete both routes.
- `login()` on POST: find the user by email (lower-case it), check `check_password_hash`. On failure flash
  `Invalid email or password` (error). On success clear the session, store `user_id`, flash
  `Welcome back, NAME` (success), where NAME is the user's name from the database (for example
  `Welcome back, James Sunderland`), and redirect to `url_for("views.rooms")`.
- `logout()`: clear the session, flash `You have been logged out` (success) and redirect to `url_for("views.login")`.
