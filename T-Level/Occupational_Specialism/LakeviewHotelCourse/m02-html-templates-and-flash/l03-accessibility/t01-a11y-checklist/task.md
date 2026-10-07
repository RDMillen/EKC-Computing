# Accessible pages from the start

Accessibility is easier to build in than to bolt on. For each template, check:

| Check | Why it matters |
|---|---|
| `<html lang="en">` | Screen readers choose the right pronunciation |
| One `<h1>`, headings in order | Users navigate by heading |
| Landmarks: `<nav>`, `<main>` | Users can jump to the main content |
| Every input has a `<label for="id">` | Screen readers announce what the field is |
| Meaningful link text (not "click here") | Links make sense out of context |
| Enough colour contrast, and never colour alone | Flash categories need text as well as colour |
| `role="alert"` on error messages | Assistive technology announces them |
| Everything works with the keyboard | Not all users have a mouse |

The occupational specialism assessment expects you to consider accessibility in your design, so build the habit now.

## Your notes
Open the `base.html` from task 2.1.3 and list which of these checks it already passes, and which it does not.
