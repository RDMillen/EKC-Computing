# Forms: GET shows, POST saves

One URL can do two jobs, depending on the HTTP method:
- `GET` shows the empty form.
- `POST` receives the submitted values in `request.form`.

```python
@views.route("/thing", methods=["GET", "POST"])
def thing():
    if request.method == "POST":
        value = request.form.get("field", "")
        ...
    return render_template("thing.html", form=request.form)
```

After a successful POST, `flash()` a message and `redirect()` to another page. If the user then presses
refresh, the browser repeats the harmless GET and does not submit the form twice. This is the
Post/Redirect/Get pattern.

The `number` column is `UNIQUE`, so inserting a room number that already exists makes SQLite raise
`sqlite3.IntegrityError`. Catch it with `try`, `except` and `else`:

```python
try:
    db.execute("INSERT INTO ...", (...))
    db.commit()
except sqlite3.IntegrityError:
    ...  # runs if the INSERT failed
else:
    ...  # runs only if the INSERT worked
```

## Task
`parse_room_form()` already validates and converts the form. Complete the POST branch of `new_room()`:
1. call `parse_room_form(request.form)`. It returns two values, so unpack them: `room, error = parse_room_form(request.form)`
2. if it returns an `error`, `flash(error, "error")`. Do not return here: the last line of the function already
   shows the form again, with the error message
3. otherwise `INSERT` the room with `?` parameters and commit
4. if the room number already exists (`sqlite3.IntegrityError`) flash `That room number already exists` (error)
5. on success, flash `Room added` (success) and redirect to the rooms list with `url_for("views.rooms")`.
