# flash() and redirect()

```python
flash("Your message", "category")
return redirect(url_for("views.home"))
```

`redirect()` sends the browser to another URL. `url_for("views.home")` builds the URL for the `home` function in the `views` blueprint.

## Task
Complete the `flash_test` function (the `/flash-test` route): flash the message `Flash works!` with the category
`"success"`, then redirect to the home page.
