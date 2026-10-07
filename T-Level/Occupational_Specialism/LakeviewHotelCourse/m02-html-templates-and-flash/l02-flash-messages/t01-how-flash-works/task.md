# Flash messages

After a user does something (saves a form, logs in) you want to tell them what happened on the next
page they see. Flask's `flash()` does exactly this.

```python
from flask import flash, redirect, url_for

@views.route("/save")
def save():
    flash("Saved!", "success")              # message, category
    return redirect(url_for("views.home"))  # then go to another page
```

```
{% with messages = get_flashed_messages(with_categories=true) %}
  {% for category, message in messages %}
    <p class="alert alert-{{ category }}" role="alert">{{ message }}</p>
  {% endfor %}
{% endwith %}
```

Key points:
- Messages are stored in the session, which is a signed cookie. Flask needs `app.secret_key`
  (or `SECRET_KEY` in config) to sign it. Without one, `flash()` raises an error.
- A flashed message is shown once: it disappears after the next page that reads it.
- Categories (`success`, `error`, `info`) let CSS style each kind differently.
- Flashing and then redirecting is the standard pattern after a form: the user can refresh the result
  page without re-submitting the form (you will meet this again in Module 4).

## Security note
A hard-coded secret key in code that goes to a repository is a real vulnerability. The next task reads
it from an environment variable.
