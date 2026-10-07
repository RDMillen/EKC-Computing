# Decorators that guard pages

Some pages should only work for logged-in users. Rather than repeating the check in every route, write it once
as a decorator:

```python
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        ...  # decide whether to run the view
        return view(*args, **kwargs)
    return wrapped_view
```
A decorator is a function that takes another function (here, a route) and returns a new function that does
something extra first. `wrapped_view` is the new function. When someone visits the page, Flask calls
`wrapped_view`, which can either send the user elsewhere or call the original `view`.

`functools.wraps(view)` copies the original function's name onto the wrapper. Without it, every decorated
route would be called `wrapped_view` and Flask would complain about duplicate endpoints.

Use it under `@views.route(...)`, so Flask registers the protected version:
```python
@views.route("/account")
@login_required
def account(): ...
```

## Task
Complete `login_required(view)`. If `g.user is None`, flash `Please log in first` (error) and redirect to `url_for("views.login")`.
Otherwise run the view. `/account` already uses your decorator, and you will add `/profile` in the next task.
