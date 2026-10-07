from flask import Flask

from views import views

app = Flask(__name__)
app.register_blueprint(views)


@app.errorhandler(404)
def page_not_found(error):
    return "Sorry, that page does not exist.", 404


if __name__ == "__main__":
    app.run(debug=True, port=8000)
