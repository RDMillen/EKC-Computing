# Storing and Retrieving User Data

## Python, Flask, and SQLite

In this session we will be capturing user data from a registration form and storing it into a SQLite database. This data can then be retrieved in order to authenticate a user attempting to login. 

SQLite is built into Python 3.x so you do not need to install the package through `pip`. 

Your file directory for this session should look like this:

```Markdown
booknook/
├── app.py
├── views.py
└── templates/
    ├── base.html
    ├── index.html
    ├── register.html
    ├── login.html
    ├── account.html
    └── logout.html
```

### Setting up to handle a database.

Firstly, we need to create a new Python script that will allow us to control initialisation and modification of our database. As these functions are separate from the rest of our website, it is good practice to keep them in a separate file and  bring them into other scripts using `from X import Y`. 

Create a Python file called `db.py`

```python
import sqlite3

def init_db():
    connection = sqlite3.connect("booknook.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        email TEXT,
        password_hash TEXT
        )
        """)
    connection.commit
    connection.close

init_db()
```

Note: You ***Must*** use `CREATE TABLE IF NOT EXISTS` otherwise every time you run this Python file, your existing database file will be replaced with the newly initialised one.

Now, open the `booknook.db` file in DB Browser for SQLite, you should now see the table and associated fields specified in the Python file. 

Next, create a function for opening and submitting data to your database:

```python
def db_connection():
    connection = sqlite3.connect("books.db")
    connection.row_factory = sqlite3.Row
    return connection
```

Reference `init.db` in `app.py`, and `db_connection` in `views.py`:

```python
# In app.py:
from db import init_db
# In views.py:
from db import db_connection
```

Finally, add the following to your `app.py` file to initialise your database. The `.db` file will be created automatically if it does not already exist.

```python
app = Flask(__name__)
app.secret_key = "secretkey"
app.register_blueprint(views, url_prefix="/views")
app.permanent_session_lifetime = timedelta(days=2)

init_db()

if __name__ == '__main__':
    app.run(debug=True, port=8080)
```

### Accepting Data

Now we need to configure our views to allow a user to register. Create a new html page called `register.html` and create three form fields: username, email, and password. This should feature the `method="post"` flag in the <form> tag.

```html
    <form action="#" method="post">
        <p>Username:</p>
        <input type="text" name="username" />
        <p>Email:</p>
        <input type="text" name="email" />
        <p>Password:</p>
        <input type="password" name="password" />
        <input type="submit" value="submit" />
    </form>
```

This allows the users data to be captured as before when we captured a user's name.

Next, we need to program the logic into our `views.py` file to store this data into our database. But before we do this, we need to import some additional modules for security:

```python
from werkzeug.security import generate_password_hash
```

This will allow us to hash the users password for secure storage. 

Let's create the route, for this route we need to consider the three possible states that can occur on this page: the user is already logged in, the user is not logged in, or the user has submitted data to this page: 

```python
@views.route("/register", methods=["POST", "GET"])
def register():
    if "username" in session:
        return redirect(url_for("views.profile"))
    elif request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password_hash = generate_password_hash(password)

        # Parse user data to main database.
        connection = db_connection()
        connection.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash)
        )
        connection.commit()
        connection.close()

        session.permanent = True
        session["username"] = username

        return redirect(url_for("views.login"))

    else:
        return render_template("register.html")
```

As before, check the database in DB Browser for SQLite, you should see all of the data pull through.

### Logging in using stored credentials.

To complete the login, we will need to check the user's password hash from before against the submitted password. So we need to import another tool:

```python
from werkzeug.security import generate_password_hash, check_password_hash
```

Next, we need to update our `login.html` page to accept a password input from our user.

```html
    <form action="#" method="post">
        <p>Username:</p>
        <p><input type="text" name="username" />
        <p>Password:</p>
        <input type="password" name="password" />
        <p><input type="submit" value="submit" />
    </form>
```

Now that we are going to receive the username and password, we need to update the logic in `views.py` to use this data to query our database and verify our user.

```python
@views.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = db_connection()
        username = connection.execute(
            "SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        connection.close()

        if username and check_password_hash(username["password_hash"], password):
            session["username"] = username["username"]
            return redirect(url_for("views.profile"))

        return redirect(url_for("views.profile"))
    else:
        if "username" in session:
            return redirect(url_for("views.profile"))
        return render_template("login.html")
```

We can now test this in browser, and we should see the login pass through to the profile / account page if the username and password match a record in our database file. 

