import os

from flask import Flask

from db import close_db, init_db
from views import views

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["DATABASE"] = os.path.join(app.root_path, "hotel.db")
app.teardown_appcontext(close_db)
app.register_blueprint(views)

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True, port=8000)
