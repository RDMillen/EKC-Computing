# Reading from the database in a route

```python
db = get_db()
rows = db.execute("SELECT ... FROM ... ORDER BY ...").fetchall()
return render_template("page.html", things=rows)
```
`fetchall()` returns a list of `sqlite3.Row` objects. Inside the template, use `row["column"]`.

## Task
In the `/rooms` route, fetch `id, number, room_type, capacity, price_per_night, available` for every room,
ordered by `number`, and render `rooms.html` with the variable `rooms`.

To try it in a browser, run `app.py`. It creates an empty database the first time it runs, so the rooms list will
be empty until you add rooms with the form in the next task.
