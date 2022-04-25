
from flask import Flask, render_template, request, session
import game_backend.input_organizer as input_organizer
import game_backend.gl_backend_functions as gl
from flask_session import Session


app = Flask(__name__)
app.secret_key = "ihaveasecretkey"
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = False
Session(app)


@app.before_first_request
def before_first_request():
    app.logger.info("before_first_request")
    session.clear()
    session['save_prints'] = []
    session['current_js_actions'] = {
        'build_multiple_choice': None,
    }
    input_organizer.create_character()

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
    data_dict = request.form.to_dict()
    
    print("frontend input ", data_dict['input'])

    actions_dict = input_organizer.organize_raw_input(data_dict['input'])
    return actions_dict
    


@app.route("/tnslp/loading-game", methods=['POST'])
def loading_game():
    
    if len(session['save_prints']) <= 9:
        session['save_prints'] = []
        return_dict = input_organizer.start_game()
    else:
        return_dict = input_organizer.load_game()

    return return_dict

     

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)