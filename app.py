

from flask import Flask
from datetime import datetime
import re
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/quotes/")
def quotes():
    return render_template("quotes.html")

@app.route("/credits/")
def credits():
    return render_template("credits.html")

@app.route("/tnslp")
def tnslp():
    return render_template("tnslp.html")

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    return render_template(
        "hello_there.html",
        name=clean_name,
        date=datetime.now()
        )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")