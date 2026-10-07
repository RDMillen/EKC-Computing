# Lakeview Hotel: Flask, Jinja and SQLite booking system

A JetBrains Academy course (PyCharm) that takes students from a first Flask route to a hotel booking app with
user accounts, price calculation, editing and collision detection.

| Module | Title | Covers |
|---|---|---|
| 1 | Getting Started with Flask | Routes, URL variables, 404s, project structure, local Git |
| 2 | HTML Templates and Flash Messages | Jinja, inheritance, flash messages, secret keys, accessibility |
| 3 | Databases and SQL | DDL, DML, JOINs, normalisation, `sqlite3`, parameterised queries |
| 4 | Database-Driven Pages | Connections in `db.py`, forms, GET/POST, redirects |
| 5 | User Accounts | Password hashing, sessions, login required, profile |
| 6 | Booking a Room | Dates, price calculation, saving, my bookings |
| 7 | Managing Bookings | Editing and cancelling, ownership checks |
| 8 | Preventing Double Bookings | Collision detection |
| 9 | Testing and Documentation | Validation, debugging, writing your own unit tests, test plan, documentation |
| 10 | Extension Challenges | Availability search, admin role, seasonal pricing, ORM, blueprints |

## Project layout
`app.py` configures Flask and runs the server (`app.run(debug=True, port=8000)`), `views.py` holds the `views` Blueprint
(routes and logic), `db.py` controls the database, and `bookings.py` holds the pure booking rules.
The blueprint is registered without a `url_prefix`, so pages are at `/rooms`, not `/views/rooms`.

Requires Python 3.10+ and `pip install -r requirements.txt` (Flask). Only the standard library is used for SQLite.
