# Rendering templates

Putting HTML inside Python strings gets messy quickly. Flask uses Jinja templates instead. A template
is an HTML file with special markers:

- `{{ value }}` prints a value
- `{% ... %}` runs logic such as loops and conditions

```python
return render_template("page.html", title="Hello", items=[1, 2, 3])
```
Every keyword argument becomes a variable inside the template.

## Task
In `views.py`, render `rooms.html` and pass it two variables: `hotel_name` (the text `"Lakeview Hotel"`) and `rooms` (the `ROOMS` list).
Open `templates/rooms.html` to see how the variables are used.
