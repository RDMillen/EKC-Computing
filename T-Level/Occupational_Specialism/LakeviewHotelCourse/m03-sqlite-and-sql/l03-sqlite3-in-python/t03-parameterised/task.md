# Safe queries with parameters

Never build SQL by gluing user input into a string:

```python
# DANGEROUS: SQL injection
conn.execute(f"SELECT * FROM users WHERE email = '{email}'")
```
Pass values separately and let the database library handle them:

```python
conn.execute("SELECT * FROM users WHERE email = ?", (email,))   # note the tuple
```
`(email,)` is a tuple with one item. The trailing comma matters: `(email)` without it is just `email` in brackets.

`fetchone()` returns the first matching row, or `None` when nothing matches, which is exactly what `get_room` and
`find_user_by_email` need:

```python
row = conn.execute("SELECT * FROM rooms WHERE number = ?", (101,)).fetchone()
```

## Task
Complete three functions. Each must use `?` parameters.
- `get_room(conn, number)`: return the room row with that number, or `None`.
- `add_user(conn, name, email, password_hash)`: insert a user, commit, and return the new user's id (`cursor.lastrowid`).
- `find_user_by_email(conn, email)`: return the user row, or `None`.
