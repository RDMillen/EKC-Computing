import sqlite3


def get_connection(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_room(conn, number):
    return conn.execute("SELECT * FROM rooms WHERE number = ?", (number,)).fetchone()


def add_user(conn, name, email, password_hash):
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    conn.commit()
    return cursor.lastrowid


def find_user_by_email(conn, email):
    return conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
