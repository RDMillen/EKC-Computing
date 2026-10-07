# Labelled inputs

A label is connected to an input by matching `for` and `id`:

```html
<label for="email">Email address</label>
<input id="email" name="email" type="email" required>
```

## Task
Complete `templates/enquiry.html`:
1. set the page language to English with `lang="en"`
2. add a name input and an email input, each with a matching `<label>`, and a submit button.

This task is about the HTML only. There is no route to receive the form yet, so submitting it in the browser shows
"Method Not Allowed". That is expected.
