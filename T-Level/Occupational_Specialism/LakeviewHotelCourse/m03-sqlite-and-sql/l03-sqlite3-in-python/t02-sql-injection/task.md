# SQL injection

If user input is pasted into a SQL string, a user can type SQL instead of data.

```python
email = request.form["email"]
sql = f"SELECT * FROM users WHERE email = '{email}'"
```
If the user types `' OR '1'='1` the query becomes:
```sql
SELECT * FROM users WHERE email = '' OR '1'='1'
```
which matches every row. A login form built this way can be bypassed. Worse, an attacker can end the
statement and run another (`'; DROP TABLE users; --`).

## The fix
Use parameterised queries. The SQL text and the values travel separately, so the values can never be
treated as SQL:

```python
conn.execute("SELECT * FROM users WHERE email = ?", (email,))
```

## Evidence for your assessment
The assessment rewards secure coding practice. Keep a short note of where you used parameterised queries and how
you tested them. The next task is checked with two injection attempts, `' OR '1'='1` and
`Mary'); DROP TABLE users;--`. Try strings like these in your own project and record the result in your test log.

## Your notes
Find one place in your own code where you could have built SQL with an f-string, and explain in two sentences
what would have gone wrong.
