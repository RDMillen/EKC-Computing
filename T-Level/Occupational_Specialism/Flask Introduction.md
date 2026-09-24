# Introduction to Flask

This document serves as an introduction to setting up a Flask-powered website with dynamic elements and interactivity. It utilises languages that should already be somewhat familiar: Python, HTML, and CSS.

Your choice of IDE will affect the configuration process. PyCharm will automate the steps relating to setting up the Python virtual environment; this must be done manually through the terminal if you are using VS Code, Zed, or another editor.

## Initial Flask Setup

Start with a new pure Python project and use the package manager built into PyCharm to install the `flask` package.

We need to configure the basic directory structure that Flask expects:

```text
booknook/
├── app.py
├── views.py
└── templates/
```

`app.py` acts as the main area for configuring Flask itself, and all data relating to it should remain here. When executing Flask (`app.run(debug=True, port=8000)`), ensure that `debug=True` is set. This makes Flask automatically reload as you make changes to your codebase.

In `app.py`:

```python
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
```

Running the script should work without error, and a link will be printed to the console: `127.0.0.1:8000`

Initially, this will not open a page as we do not have any `html` files to present to the end user. We'll set that up next.

## Creating Routes

Flask operates using routes. A route matches the address a user types into the browser to a Python function, and whatever that function returns is sent back to the user. We will keep ours in a separate file, `views.py`, using a Blueprint.

In `views.py`:

```python
from flask import Blueprint

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return "This is the homepage."
```

Then, in `app.py`, import the blueprint and register it with the app:

```python
from flask import Flask
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/views")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
```

The `url_prefix` places every route from `views.py` under `/views`, so the homepage is now found at `127.0.0.1:8000/views/`.

## Templates

HTML lives in the `templates` folder. Add a new file called `index.html`, change the title, and add some content to the body inside a div.

In `views.py`, import `render_template` and use it in the `home` function:

```python
from flask import Blueprint, render_template

@views.route("/")
def home():
    return render_template("index.html")
```

You can pass a keyword argument to `render_template` to make Python variables accessible in your HTML:

```python
def home():
    return render_template("index.html", name="Ross")
```

The variable is now accessible in our HTML file. In `index.html`, add:

```html
<p>
    Hello, {{ name }}
</p>
```

You can also write semi-native Python in an HTML file using Flask. This is Jinja, the templating language that Flask uses:

```html
{% for i in range(3) %}
    {% if i % 2 == 0 %}
        <p>{{ i }}</p>
    {% endif %}
{% endfor %}
```

Add another variable of your own to `render_template` and display it on the page to check that you understand how it works.

## Dynamic URLs

Pages can change based on the URL that is typed in. Anything inside `<>` in a route is a parameter that gets passed to the function.

Create a new `profile` route:

```python
@views.route("/profile/<username>")
def profile(username):
    return render_template("index.html", name=username)
```

In the browser, go to `/views/profile/Derek` and try different names.

## Query Strings

We can also read values from the URL after a question mark. Let's query:

`/views/profile?name=ross`

To do this, add `request` to the `flask` import:

```python
from flask import Blueprint, render_template, request
```

Then update the `profile` route to read from `request.args`:

```python
@views.route("/profile")
def profile():
    args = request.args  # This behaves like a dictionary
    name = args.get("name")
    return render_template("index.html", name=name)
```

Now that we are using `args`, the username has been removed from the route and from the function's parameters. Visit `/views/profile?name=ross` and change the value after the equals sign to see the page update.

## Redirects

To send users to another page, first import `redirect` and `url_for` from `flask`:

```python
from flask import Blueprint, render_template, request, redirect, url_for
```

```python
@views.route("/go-home")
def go_home():
    return redirect(url_for("views.home"))
```

`url_for` takes the name of the blueprint and the name of the function, joined with a dot, rather than the URL itself. This means the URL can change later without breaking any of your redirects.

You can pass variables alongside the redirect too if you need to, for example:

```python
return redirect(url_for("views.myaccount", username="DestroyerOfWorlds"))
```

As `username` is not part of the route, Flask adds it to the end of the URL as a query string, which we read in the same way as before:

```python
@views.route("/myaccount")
def myaccount():
    username = request.args.get("username")
    return render_template("index.html", name=username)
```

## Getting Data: GET and POST

GET sends data in the URL itself. Anything sent this way is visible in the address bar and is kept in the browser history, so it should never be used for sensitive information.

POST sends data in the body of the request, which keeps it out of the URL. This is the method to use for forms. Note that POST does not encrypt the data on its own; that is the job of HTTPS.

We are aiming for a login page. By default a route only accepts GET requests, so we need to tell the login route to accept POST as well:

```python
@views.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

@views.route("/<username>")
def user(username):
    return f"<h1>Hi {username}</h1>"
```

The keyword is `methods`, with an s. The second route is where users will land once they have logged in.

## Template Inheritance

Most pages on a site share the same overall structure, so rather than copying it into every file we can build a base template and let other pages extend it. Create a new file in the `templates` folder called `base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <div>
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

The `block` tags mark the areas that a child page is allowed to fill in. Anything outside of a block is inherited unchanged.

Now we can strip `index.html` back and have it extend the base instead:

```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <h1>Home Page</h1>
    <p>Hello {{ name }}</p>
{% endblock %}
```

Reload `/views/` and the page should look exactly the same as before. The difference is that the layout now lives in one place. Create `login.html` in the `templates` folder in the same way:

```html
{% extends "base.html" %}

{% block title %}Login{% endblock %}

{% block content %}
    <h1>Login Page</h1>
    <form action="#" method="post">
        <p>Name: </p>
        <p><input type="text" name="nm"></p>
        <p><input type="submit" value="submit"></p>
    </form>
{% endblock %}
```

## Handling the Login Form

In this example, `name="nm"` refers to how we are going to pull the data into our Python code. We need to expand on our login code from earlier, adding an `if` statement for request handling:

```python
@views.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["nm"]  # This gives us the data from the name field of our form.
        return redirect(url_for("views.user", username=username))
    else:
        return render_template("login.html")
```

Visiting `/views/login` sends a GET request, so the form is displayed. Submitting the form sends a POST request to the same address, so the `if` branch runs and the user is redirected to their greeting.
