from flask import Flask
from views import views
from db import init_db
from datetime import timedelta
app = Flask(__name__)
app.secret_key = "secretkey"
app.register_blueprint(views, url_prefix="/views")
app.permanent_session_lifetime = timedelta()

init_db()

if __name__ == '__main__':
    app.run(debug=True, port=8080)
