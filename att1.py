from flask import Flask

app = Flask(__name__)


@app.route("/decorator")
def decoratorex():
    return "Welcome to Flask’s documentation. Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications."


if __name__ == "__main__":
    app.run(debug=True)
