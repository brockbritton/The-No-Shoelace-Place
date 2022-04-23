
from flask import Flask, render_template, request, session
import game_backend.input_organizer as input_organizer
import game_backend.gl_backend_functions as gl

from flask_session import Session


app = Flask(__name__)
app.secret_key = "ihaveasecretkey"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def home():

    return render_template("home.html")



@app.route("/quotes/")
def quotes():
    return render_template("quotes.html")

@app.route("/credits")
def credits():
    return render_template("credits.html")

@app.route("/tnslp/", methods=('GET', 'POST'))
def tnslp():

    input_organizer.start_game()
    return render_template("game_page.html")


@app.route("/accept-input-data", methods=['POST'])
def accept_input_data():
    print(session)
    data_dict = request.form.to_dict()
    
    print("frontend input ", data_dict['input'])

    actions_dict = input_organizer.organize_raw_input(data_dict['input'])
    return actions_dict
    


@app.route("/tnslp/start-game", methods=['POST'])
def start_game():
    
    session['current_js_actions'] = {
        'build_multiple_choice': None,
    }

    return_dict = input_organizer.start_game()

    print(return_dict)
    return return_dict

     

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=False)