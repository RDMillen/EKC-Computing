# Relational basics

A relational database stores data in tables. Each table has columns (the attributes) and
rows (the records).

| id | number | room_type | capacity | price_per_night |
|----|--------|-----------|----------|-----------------|
| 1  | 101    | Single    | 1        | 80.0            |
| 2  | 102    | Double    | 2        | 120.0           |

## Keys
- A primary key (PK) uniquely identifies each row. Here, `id`.
- A foreign key (FK) is a column holding the primary key of a row in another table. It links the tables:
  `bookings.room_id` refers to `rooms.id`.
- A unique constraint stops duplicates (for example, two users with the same email).

## SQLite data types
SQLite has a small set of types: `INTEGER`, `REAL`, `TEXT`, `BLOB`. There is no separate date type, so
we store dates as ISO text (`YYYY-MM-DD`). ISO dates sort correctly as text and are easy to compare in SQL.

## Constraints you will use
`PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK (capacity > 0)`, `REFERENCES other_table (id)`.

## The hotel database
```
users    (id PK, name, email UNIQUE, password_hash)
rooms    (id PK, number UNIQUE, room_type, capacity, price_per_night, available)
bookings (id PK, user_id FK -> users, room_id FK -> rooms, check_in, check_out, occupants, total_price)
```
You will create these three tables in the next lesson.
