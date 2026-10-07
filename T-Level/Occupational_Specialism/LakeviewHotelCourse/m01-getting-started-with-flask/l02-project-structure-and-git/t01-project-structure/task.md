# Project structure

The hotel project is split into files that each have one job:

```
hotel/
  app.py           # Flask itself: the app object, config (secret key, database path), registers the blueprint, runs the server
  views.py         # a Blueprint holding the routes and the logic behind them
  db.py            # database control: opening, closing and creating the database (from Module 4)
  bookings.py      # pure booking rules: dates, prices, clashes (from Module 6)
  validation.py    # checks form input before it is used (from Module 9)
  schema.sql       # the table definitions
  templates/       # Jinja HTML templates
  static/          # CSS, images, JavaScript
  tests/           # automated tests
  requirements.txt # packages the project needs
```

Why separate things?
- `app.py` is the one place to look for settings.
- `views.py` keeps the routes together, and `Blueprint("views", __name__)` gives the group the name `views`.
  `app.py` registers it with `app.register_blueprint(views)`.
- `url_for` takes the name of the blueprint and the name of the function, joined with a dot. The `home` function
  in the `views` blueprint is `url_for("views.home")`. Flask calls this name the endpoint.
- Templates hold HTML, so your Python is not full of HTML strings.
- Tests can import your code without starting a server.

> You may have registered a blueprint with `url_prefix="/views"` before. That puts every route under `/views/...`.
> In this course the blueprint is registered without a prefix, so the rooms page is at `/rooms` rather than
> `/views/rooms`. Because every link is built with `url_for`, adding the prefix back later only means changing
> the `register_blueprint` line in `app.py`.

Flask finds `templates/` and `static/` relative to the file that created the app (`Flask(__name__)` in `app.py`).

## Your notes
Sketch the folder structure you expect the finished hotel app to have, and write one sentence about the
job of each file or folder.
