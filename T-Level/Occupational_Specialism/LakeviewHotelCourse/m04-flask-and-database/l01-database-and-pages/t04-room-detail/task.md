# Routes that look up one record

A URL like `/rooms/3` should show the room whose `id` is 3. Be careful not to mix up `id` and `number`: room
number 101 has the id 1. Capture the id with `<int:room_id>`, then ask the database:

```python
row = db.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()
```
`fetchone()` returns one row, or `None` if nothing matched. When something does not exist, `abort(404)`
stops the request and returns the standard 404 page.

## Task
Complete `room_detail(room_id)`: fetch the room (with a `?` parameter), call `abort(404)` if there isn't one,
otherwise render `room_detail.html` with the variable `room`.
