# A secret key from the environment

The secret key is Flask configuration, so it belongs in `app.py`. An environment variable is a named setting held
by the operating system, outside your code. Reading the key from one means the real key never appears in your source
code or your Git history. If the variable is not set, fall back to a clearly labelled development value so the app
still runs on your laptop.

```python
import os
value = os.environ.get("NAME", "default")
```

## Task
In `app.py`, set `app.config["SECRET_KEY"]` to the value of the `SECRET_KEY` environment variable, falling back to
`"dev-only-change-me"` when it is not set.
