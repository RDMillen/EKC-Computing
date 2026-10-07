# Editing without clashing with yourself

If a guest edits booking 1 (1-4 Nov) to be 1-5 Nov, the check would find... booking 1 itself, and refuse.
The fix is to leave the booking being edited out of the check:

```sql
... AND (? IS NULL OR id != ?)
```
When `exclude_booking_id` is `None` (a brand-new booking) nothing is excluded. When it is a number, that booking is skipped.
Pass the value twice (once for each `?`).

Why not just `AND id != ?`? In SQL, any comparison with `NULL` is neither true nor false, so `id != NULL` never
matches a row. For a brand-new booking (`None` becomes `NULL`) every booking would be left out, and no clash would
ever be found. `? IS NULL OR` stops that from happening.

## Task
Your working `has_collision` from the last task is shown in the placeholder. Do not delete it this time: edit it,
adding the new condition to the SQL and the extra values to the parameters.

Remember: excluding booking 1 must not hide a clash with a *different* booking.
