from datetime import date

MAX_NIGHTS = 30


def validate_booking_form(form, today=None):
    """Return a list of error messages for a booking form. An empty list means the form is valid."""
    today = today or date.today()
    errors = []
    try:
        check_in = date.fromisoformat(form.get("check_in", ""))
    except ValueError:
        errors.append("Please enter the check-in date as YYYY-MM-DD")
    else:
        if check_in < today:
            errors.append("Check-in cannot be in the past")
    try:
        nights = int(form.get("nights", ""))
    except ValueError:
        errors.append("Nights must be a whole number")
    else:
        if not 1 <= nights <= MAX_NIGHTS:
            errors.append("Nights must be between 1 and %d" % MAX_NIGHTS)
    try:
        occupants = int(form.get("occupants", ""))
    except ValueError:
        errors.append("Occupants must be a whole number")
    else:
        if occupants < 1:
            errors.append("At least one occupant is required")
    return errors
