# Updating a record

```sql
UPDATE users SET name = ?, email = ? WHERE id = ?
```
Notice the `WHERE id = ?` clause. The id must come from `g.user["id"]` (the logged-in user), never from the
form. If you trusted an id sent by the browser, a user could change somebody else's account.

## Task
Complete the POST branch of `profile()` (already protected by `@login_required`):
1. read `name` and `email` (lower-case) from the form; if either is empty flash `Please fill in all fields` (error)
2. `UPDATE` the logged-in user's row with `?` parameters and commit
3. if the new email belongs to someone else (`sqlite3.IntegrityError`) flash `That email is already registered` (error)
4. on success flash `Profile updated` (success) and redirect to `url_for("views.profile")`.
