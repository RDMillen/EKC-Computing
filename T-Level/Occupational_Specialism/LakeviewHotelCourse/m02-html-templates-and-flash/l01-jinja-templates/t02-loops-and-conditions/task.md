# Control flow in Jinja

```
{% for room in rooms %}
  ...
{% endfor %}

{% if room.available %}
  ...
{% else %}
  ...
{% endif %}
```
Jinja blocks always need an explicit end (`endfor`, `endif`). Inside a loop you can read dictionary keys
with dot notation: `room.price`.

## Task
Inside the loop in `rooms.html`, show
`<span class="badge available">Available</span>` when `room.available` is true, and
`<span class="badge unavailable">Unavailable</span>` otherwise.
