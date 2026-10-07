# Debugging with tests

`bugs.py` contains three functions. Each has one bug and the tests tell you the symptoms. The placeholders
show the current (buggy) code.

Work like a developer:
1. press Check and read one failure message
2. form a hypothesis about the cause
3. change one thing
4. press Check again.

Resist guessing several changes at once. In your own project, record each bug you find in `CHANGE_LOG.md` (task
9.1.6 sets this up) like this: *what was wrong, how I found it, what I changed*.

Two of these are classic off-by-one / boundary errors. Think about what `+ 1` and `<=` do at the edges.
