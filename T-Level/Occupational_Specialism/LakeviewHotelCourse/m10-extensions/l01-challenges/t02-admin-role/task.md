# Extension: staff accounts

Real systems separate customers from staff. Design and build an admin role.

## Plan in the notes file before you code
- How do you mark a user as admin? (`ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0` is one option. Note how SQLite handles `ALTER TABLE`.)
- Write an `admin_required` decorator that builds on `login_required`. Which status code do non-admins get, 403 or 404? Argue for your choice.
- Admin pages to build: list all bookings with the guest's name, add a room, disable a room (`available = 0`), cancel any booking.
- Principle of least privilege: which pages should customers never reach?

## Test it
Write tests for: a customer visiting an admin URL, an anonymous visitor, an admin doing the task, and an admin disabling a room that
already has future bookings (what *should* happen?).
