

from flask import Flask, render_template, request
import game_backend.test as test

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/quotes/")
def quotes():
    return render_template("quotes.html")

@app.route("/credits")
def credits():
    return render_template("credits.html")

@app.route("/tnslp", methods=('GET', 'POST'))
def tnslp():
    return render_template("game_page.html")


@app.route("/accept-input_data", methods=['POST'])
def accept_input_data():
    # request.form
    # request.method
    test.test_path(request.form)
    return "test"


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)