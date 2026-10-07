# Your first route

A route matches the address a user types into the browser to a Python function. Whatever the function returns
is sent back to the browser.

In this project the routes live in `views.py`, inside a Blueprint: a named group of routes. `app.py` creates the
Flask app and registers the blueprint with `app.register_blueprint(views)`. `app.py` is locked in this task, so you
only need to work in `views.py`.

```python
views = Blueprint("views", __name__)

@views.route("/about")
def about():
    return "About us"
```

The decorator `@views.route("/about")` registers the function for the URL `/about`.

## Task
Make the home page (`/`) return the text `Welcome to Lakeview Hotel`.
