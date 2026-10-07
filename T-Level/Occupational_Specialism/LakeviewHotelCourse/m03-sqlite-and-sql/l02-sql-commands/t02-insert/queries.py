SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
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

INSERT_ROOM = "INSERT INTO rooms (number, room_type, capacity, price_per_night) VALUES (?, ?, ?, ?)"

INSERT_USER = "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)"
