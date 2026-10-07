# Extension: growing past one views file

`views.py` is now long. You already use one blueprint, `views`. Split it into several smaller blueprints, and
turn `app.py` into an application factory (`create_app()` that builds and returns an app, so tests can create a fresh one).

```
hotel/
  app.py            # create_app() and app.run(debug=True, port=8000)
  auth_views.py     # register, login, logout (blueprint "auth")
  room_views.py     # blueprint "rooms"
  booking_views.py  # blueprint "bookings"
  bookings.py       # pure booking rules (unchanged)
  db.py
```

## Rules for a safe refactor
1. All tests green first. Commit.
2. Move one blueprint at a time. Run the tests after each move. Commit.
3. `url_for("views.login")` becomes `url_for("auth.login")`. The endpoint starts with the blueprint name, so update every template and redirect that uses `url_for`.
4. Use a Git branch (`git switch -c refactor-blueprints`). If it goes wrong, switch back to `main` (or `master`).

Record what broke and how you found it in your change log.
