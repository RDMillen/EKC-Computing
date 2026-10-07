# One layout, many pages

Repeating the navigation bar on every page is slow and error-prone. With template inheritance you write
the shared layout once in `base.html` and mark the parts that change as blocks:

```
<!-- base.html -->
{% block content %}{% endblock %}

<!-- rooms.html -->
{% extends "base.html" %}
{% block content %} ... page-specific HTML ... {% endblock %}
```

`url_for` builds a URL from the blueprint name and the function name joined with a dot, so links keep working if
you change the URL later. In a template it goes inside `{{ }}`, and the result goes in the `href`:

```html
<a href="{{ url_for('views.about') }}">About us</a>
```

The endpoints you need for this task are `views.home` and `views.rooms`.

`base.html` already has a `title` block with a default value. A child page can replace it, as `rooms.html` does.

## Task
In `templates/base.html`:
1. add navigation links to the home and rooms routes using `url_for`
2. define a block called `content`.

The two page templates already extend your base.
