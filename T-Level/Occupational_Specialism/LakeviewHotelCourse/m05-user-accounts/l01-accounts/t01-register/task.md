# Never store passwords

If a database leaks and passwords are stored as plain text, every account is compromised. Instead store a
hash: a one-way scrambled value. When someone logs in, hash what they typed and compare.

```python
from werkzeug.security import generate_password_hash, check_password_hash

stored = generate_password_hash("my password")      # salted hash, safe to store
check_password_hash(stored, "my password")           # True
```
Werkzeug is installed with Flask. It adds a random salt, so two users with the same password get different hashes.

`load_logged_in_user()` near the bottom of `views.py` is explained in the next task. You can ignore it for now.

## Task
Complete the POST branch of `register()`:
1. read `name`, `email` (strip it and make it lower-case) and `password` from `request.form`
2. if anything is empty, flash `Please fill in all fields` (error)
3. if the password is shorter than 8 characters, flash `Password must be at least 8 characters` (error)
4. otherwise INSERT the user with `generate_password_hash(password)`. If the email already exists
   (`sqlite3.IntegrityError`) flash `That email is already registered` (error)
5. on success flash `Registered successfully. Please log in.` (success) and redirect to the login page with `url_for("views.login")`.
