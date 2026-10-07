# Connecting Flask to SQLite

Opening a database connection is relatively slow, and each web request should have its own. Flask provides
two helpers for this:

- `g`: an object that lives for one request. Anything stored on it is thrown away when the request ends.
- `app.teardown_appcontext(close_db)`: tells Flask to call `close_db` when each request finishes, even if an error
  happened. From the next task, `app.py` contains this line.

The pattern:
1. `get_db()` creates the connection the first time it is needed during a request, stores it in `g.db` and returns it.
2. `close_db()` closes it at the end of the request.

`current_app` means "the Flask app handling this request". `db.py` uses it rather than importing `app` from
`app.py`, because `app.py` already imports `db.py`. If each file imported the other, Python would hit a circular import.
`current_app.config["DATABASE"]` holds the database file path, which lets the tests point the app at a temporary database.

## Task
Complete `get_db()` and `close_db()` in `db.py`:
- `get_db()` opens `sqlite3.connect(current_app.config["DATABASE"])` only if `g` has no `db` yet, sets `row_factory = sqlite3.Row`,
  runs `PRAGMA foreign_keys = ON`, and returns `g.db`.
- `close_db()` removes `db` from `g` (use `g.pop("db", None)`) and closes it if it exists.

`init_db()` is already written: it runs `schema.sql`. Read it and the schema before you start.
