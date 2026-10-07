# Welcome to the Lakeview Hotel project

Over this course you will build the booking website for the Lakeview Hotel, on the shore of Toluca Lake, using
Python, Flask, Jinja templates and SQLite.
By the end, a user can register, log in and book a room for a set number of nights, with the price worked out
from the number of guests. They can then edit or cancel the booking, and the system refuses any booking that
clashes with one already made.

## How the course is organised
The course is split into numbered modules. Each module has lessons (1.1, 1.2 and so on) and each lesson has
tasks (1.1.1, 1.1.2 and so on).

| Module | What you build |
|---|---|
| 1 | Your first Flask routes, the project structure and local Git |
| 2 | Jinja templates, flash messages and accessible pages |
| 3 | SQL and SQLite: tables, queries and safe parameterised queries |
| 4 | Pages that read from and write to the database |
| 5 | User accounts: registering, logging in and editing a profile |
| 6 | Booking a room, with the price worked out from nights and guests |
| 7 | Editing and cancelling bookings |
| 8 | Preventing double bookings |
| 9 | Validation, debugging, your own unit tests and documentation |
| 10 | Optional extension challenges |

## How a task works
- Theory tasks explain an idea. Some ask you to write notes. Nothing is checked, so press Next when you are done.
- Quiz tasks ask a multiple-choice question. Choose your answer and press Check.
- Coding tasks have grey placeholders in the code. Delete the placeholder text, write your own code in its place,
  then press Check. Hidden tests run against your code and the result appears in the task panel. If a test fails,
  read its message carefully, as it tells you what the test expected.
- Text shown in code format in a task, such as `Booking confirmed`, must be copied exactly, including capital
  letters, spaces and full stops. The tests look for that exact text.

Each task is its own small copy of the project. Files you need but should not change are locked: you can open and
read them, but you cannot edit them. Read them anyway, as they show you how your code is used.

Your code is not carried from one task to the next. Each task starts from a finished version of the step before,
so a mistake in one task will not hold you back in the next.

## Your own hotel project
The course gives you the pieces one at a time. To prepare for the assessment, also build your own copy of the hotel
app in a separate PyCharm project, adding each feature as you complete it here. Some tasks (Git, testing and
documentation) ask you to work in that project.

## Set-up checklist
1. In PyCharm open Settings | Project | Python Interpreter and add a new virtual environment for this course.
2. Open the PyCharm terminal and run `pip install -r requirements.txt`. PyCharm may offer to do this for you.
3. Check Flask is installed by running `python -c "import flask; print('Flask is installed')"`.

You need Python 3.10 or newer.

## Running the website
From task 1.1.2 onwards, each coding task has an `app.py`. Right-click it and choose Run. The console prints a
link such as `http://127.0.0.1:8000`. Click it to open the site in your browser.

The link always opens the home page (`/`). Many tasks only build one page, so the home page may not exist yet and
you will see "Not Found". That does not mean your code is broken. Look at the route in `views.py`, for example
`@views.route("/rooms")`, and add that path to the end of the address: `http://127.0.0.1:8000/rooms`.

Press the red Stop button before you run a different task. Only one program can use port 8000 at a time, so a
second one fails with an "address already in use" error. If you forget, the browser may keep showing the site from
the previous task.

If the page shows "Internal Server Error", check the console in PyCharm. The last lines of the error tell you
which line of your code went wrong. An empty placeholder (`pass`) causes this, because the route returns nothing.

`debug=True` in `app.run(...)` makes Flask reload when you save and shows a detailed error page when something
goes wrong. It is for development only and must never be left on for a live website.

When you have finished the checklist, press Next.
