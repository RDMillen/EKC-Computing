# Using SQLite from Python

Python's standard library includes `sqlite3`, so no installation is needed.

The `database.py` file in this lesson is practice for using `sqlite3` on its own. In Module 4 the hotel app gets
its own `db.py`, which does the same job inside Flask.

```python
import sqlite3

conn = sqlite3.connect("hotel.db")      # or ":memory:" for a throw-away database
conn.row_factory = sqlite3.Row          # rows behave like dicts: row["name"]
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.execute("SELECT * FROM rooms")
rows = cursor.fetchall()
conn.commit()                           # save INSERT / UPDATE / DELETE
```
- A connection is your link to the database file. A cursor walks through query results.
- SQLite does not enforce foreign keys unless you turn them on for each connection.
- Changes are only saved after `commit()`.

## Task
Complete `get_connection(path)` so that it opens a connection, sets `sqlite3.Row` as the row factory,
turns foreign key enforcement on, and returns the connection.
