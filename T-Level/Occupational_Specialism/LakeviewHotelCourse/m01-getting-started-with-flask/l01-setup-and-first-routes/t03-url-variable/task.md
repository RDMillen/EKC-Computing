# Dynamic URLs

Pages can change based on the URL that is typed in. Anything inside `<>` in a route is a parameter that gets
passed to the function. Adding `int:` makes Flask check that the value is a whole number and convert it for you.

```python
@views.route("/guest/<int:guest_id>")
def guest(guest_id):
    return f"Guest number {guest_id}"
```

A request for `/guest/7` calls `guest(7)`. A request for `/guest/abc` is not a match, so Flask returns a
404 Not Found automatically.

## Task
Complete the route `/room/<int:number>` so that `/room/312` returns the text `Room 312`, `/room/9` returns
`Room 9`, and so on. An f-string, as in the example above, is the neatest way to build the text.
