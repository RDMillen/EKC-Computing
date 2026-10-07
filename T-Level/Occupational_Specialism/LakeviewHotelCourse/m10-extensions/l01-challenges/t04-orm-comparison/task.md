# Extension: raw SQL versus an ORM

An ORM (object-relational mapper) such as SQLAlchemy lets you work with Python classes instead of SQL text:

```python
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)

Room.query.filter_by(available=True).order_by(Room.price_per_night).all()
```

## Task
Flask-SQLAlchemy is not part of this course's requirements. In a copy of your own project, install it first with
`pip install Flask-SQLAlchemy`.

Re-implement only the rooms listing and the collision check using Flask-SQLAlchemy, then answer in the notes file:
1. what SQL does the ORM generate? (set `app.config["SQLALCHEMY_ECHO"] = True` to print each query)
2. which was quicker to write? Which was easier to test and to explain to someone who does not know SQLAlchemy?
3. which would you choose when you must show your SQL and DML/DDL knowledge in an assessment, and why?
4. where does the ORM protect you from SQL injection, and where can you still make it unsafe (`text()` with an f-string)?
