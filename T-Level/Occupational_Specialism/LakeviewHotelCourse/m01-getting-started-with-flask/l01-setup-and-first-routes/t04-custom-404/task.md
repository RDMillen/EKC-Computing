# Custom error pages

When a URL does not match any route, Flask returns a 404 response. You can replace the default page
with an error handler. Error handlers are part of configuring the Flask app itself, so this one goes in `app.py`:

```python
@app.errorhandler(404)
def page_not_found(error):
    return "Nothing here", 404
```

`return "Nothing here", 404` returns two values separated by a comma: the page content and the HTTP status code.
If you leave out the 404, Flask sends 200 OK, which tells the browser the page was found.

## Task
Return the message `Sorry, that page does not exist.` together with the status code `404`.
