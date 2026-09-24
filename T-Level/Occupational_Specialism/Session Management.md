# Sessions

Up until this stage, we have been passing variables between our pages using additional arguments in redirect or render_template functions. For demonstration purposes this works, however when our website start getting more complex, it increases the chance of an error. 

Sessions allows us to have Flask store a small piece of data in the user's browser that we can utilise across pages. It is similar to how a cookie works. 

Let's look at implementing sessions to allow us to carry our name between pages.

The are two things that need setting up for session to work, firstly in our `app.py` file we need to create a secret key that will sign our session file:

```python
app.secret_key = "secretkey"
```

Then, in `views.py` we need to import the `session` module from the `flask` library:

```python
from flask import session
```

Now we can start preparing the data that we want to user as part of our session file, in this case we will be passing our user's name.

```python
name = request.form["name"]
session["name"] = name 
```

Session itself is a dictionary, so in this code ```session["name"]``` is the key and we are assigning the `name` variable as the value. It can be accessed across our routes in the `views.py` file. Handy!

To access data from, we treat it as we would a dictionary:

```python
@views.route("/profile")
def profile():
    if "name" in session:
        return render_template("profile.html", name=session["name"])
    else:
        return redirect(url_for("views.login"))
```

The `if` statement in the above code checks to see whether the name key exists before loading the profile page, if it does not contain any information, it will automatically redirect to the login page.

### Logging out

We also need to have a way of logging our user out and terminating their session. To do this, we will start by creating a simple logout route:

```python
@views.route("/logout")
def logout():
  session.pop["name", None]
  return redirect(url_for("views.login"))
```

This route triggers the `.pop` method which removes the value from the session file stored in the user's browser. You must issue a `.pop` for each held variable to fully clear the data from the users browser!

**Important** - session files held on a user's browser are signed, but not encrypted. This means that you can view the session file's contents through the browser's developer tools - and modify them. Flask signs the session file, if it detects tampering it will discard the session to maintain security.

### Time-based session expiry.

Logged into Facebook for weeks without re-entering your password? Session permanence! Logging into a service every time you open your browser is not a good user experience (UX), we can tell Flask how long the session can last.

In `app.py`, import `timedelta` from `datetime` and then set how long you want the session to persist:

```python
from datetime import timedelta

app.permanent_session_lifetime = timedelta(days=2)
```

`timedelta` can accept weeks, days, minutes, seconds, milliseconds, or even microseconds! 

Now, to initialise a session that uses this timeframe we need to make a small addition alongside the initial creation of our session in `views.py`:

```python
name = request.form["name"]
session.permanent = True
session["name"] = name 
```

And that is it! 

