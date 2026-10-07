import os
import tempfile

from werkzeug.security import generate_password_hash

from app import app as flask_app
from db import get_db, init_db

PASSWORD = "password123"
_HASH = generate_password_hash(PASSWORD)

SEED = """INSERT INTO rooms (number, room_type, capacity, price_per_night, available) VALUES
    (101, 'Single', 1, 80.0, 1),
    (102, 'Double', 2, 120.0, 0),
    (103, 'Double', 2, 110.0, 1),
    (201, 'Family', 4, 180.0, 1),
    (312, 'Suite', 3, 250.0, 1);
"""


def make_client():
    """Fresh temporary database, seeded, plus a Flask test client."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    flask_app.config.update(TESTING=True, DATABASE=path, SECRET_KEY="test-key")
    with flask_app.app_context():
        init_db()
        db = get_db()
        db.executescript(SEED)
        db.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                   ("James Sunderland", "james@example.com", _HASH))
        db.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                   ("Mary Sunderland", "mary@example.com", _HASH))
        db.commit()
    return flask_app.test_client(), path


def login(client, user_id=1):
    with client.session_transaction() as sess:
        sess["user_id"] = user_id


def query(sql, params=()):
    with flask_app.app_context():
        return [tuple(row) for row in get_db().execute(sql, params).fetchall()]


def execute(sql, params=()):
    with flask_app.app_context():
        db = get_db()
        db.execute(sql, params)
        db.commit()


def add_booking(user_id, room_id, check_in, check_out, occupants=1, total=100.0):
    with flask_app.app_context():
        db = get_db()
        cur = db.execute(
            "INSERT INTO bookings (user_id, room_id, check_in, check_out, occupants, total_price) "
            "VALUES (?, ?, ?, ?, ?, ?)", (user_id, room_id, check_in, check_out, occupants, total))
        db.commit()
        return cur.lastrowid


def cleanup(path):
    try:
        os.remove(path)
    except OSError:
        pass
