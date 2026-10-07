# Documentation that someone else can use

Another developer, or the person marking your work, should be able to run, understand and maintain your system from the files alone.

## Task
Fill in the three files:

1. `README.md`: what the system does, the requirements (Python version, `pip install -r requirements.txt`), how to create the database
   (running `app.py` creates it), how to run it, how to run the tests, and the known limitations.
2. `ROUTES.md`: one row per route: URL, methods, who can use it, what it does.
3. `CHANGE_LOG.md`: every significant change and every source you used (code, images, tutorials, AI output)
   with its licence. Maintainers need this to know what they can legally reuse.

## Evaluate
Finish `README.md` with a short evaluation: what works well, what you would improve with more time
(e.g. password reset, seasonal pricing, an admin role), and what risks remain (e.g. no CSRF protection, which means another website could trick a logged-in user's browser into submitting
your forms, or SQLite struggling with many users at once).

> These files are for practice. In the assessment you must use Pearson's official Change/Source Log and AI Log
> templates, which your teacher will give you.
