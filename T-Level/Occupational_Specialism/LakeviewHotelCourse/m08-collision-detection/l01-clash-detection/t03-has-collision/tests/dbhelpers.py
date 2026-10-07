import sqlite3

SCHEMA = """CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER NOT NULL UNIQUE,
    room_type TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    price_per_night REAL NOT NULL CHECK (price_per_night > 0),
    available INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users (id),
    room_id INTEGER NOT NULL REFERENCES rooms (id),
    check_in TEXT NOT NULL,
    check_out TEXT NOT NULL,
    occupants INTEGER NOT NULL CHECK (occupants > 0),
    total_price REAL NOT NULL
);
"""

SEED = """INSERT INTO rooms (number, room_type, capacity, price_per_night, available) VALUES
    (101, 'Single', 1, 80.0, 1),
    (102, 'Double', 2, 120.0, 0),
    (103, 'Double', 2, 110.0, 1),
    (201, 'Family', 4, 180.0, 1),
    (312, 'Suite', 3, 250.0, 1);
INSERT INTO users (name, email, password_hash) VALUES
    ('James Sunderland', 'james@example.com', 'x'),
    ('Mary Sunderland', 'mary@example.com', 'x');
INSERT INTO bookings (user_id, room_id, check_in, check_out, occupants, total_price) VALUES
    (1, 1, '2026-11-01', '2026-11-04', 1, 240.0),
    (2, 4, '2026-11-10', '2026-11-12', 3, 360.0),
    (1, 1, '2026-12-01', '2026-12-03', 1, 160.0);
"""


def make_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    conn.executescript(SEED)
    conn.commit()
    return conn
