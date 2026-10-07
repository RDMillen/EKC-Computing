# Showing messages in the layout

Put the flash loop in `base.html` so every page can show messages. Use
`get_flashed_messages(with_categories=true)`, which returns `(category, message)` pairs, and give
each message a CSS class built from its category, such as `alert-success` or `alert-error`. The theory task 2.2.1
shows the loop. Note that Jinja writes `true` in lower case, unlike Python's `True`.

## Task
In `base.html`, loop over the flashed messages and print each one as
`<p class="alert alert-CATEGORY" role="alert">MESSAGE</p>`.
