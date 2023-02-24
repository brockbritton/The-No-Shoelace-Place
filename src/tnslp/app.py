
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
import tnslp.game_backend.classes.game_class as game_class


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
Session(app)

@app.before_first_request
def before_first_request():
    session.clear()

    session['current_js_actions'] = {
        'build_multiple_choice': None,
    }

    try:
        if session['game'] is not None:
            print("game already exists")

    except KeyError:
        session['game'] = game_class.Game()
        print("game created")

    session.modified = True

@app.route("/")
def home():
    return redirect(url_for('welcome'))

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/unlocked-quotes/")
def quotes():
    return render_template("quotes.html")

@app.route("/credits")
def credits():
    return render_template("credits.html")

@app.route("/game/", methods=('GET', 'POST'))
def play_game():
    return render_template("game.html")


@app.route("/game/accept-input-data", methods=['POST'])
def accept_input_data():
    data_dict = request.form.to_dict()
    print("frontend input ", data_dict['input'])
    return session['game'].organize_raw_input(data_dict['input'])
    
@app.route("/game/request-map-data", methods=['GET'])
def request_map_data():
    return session['game'].return_map_data()

@app.route("/game/loading-game", methods=['POST'])
def loading_game():
    if len(session['game'].save_prints) == 0: 
        return_dict = session['game'].start_game()
    else:
        return_dict = session['game'].load_game() 

    return return_dict

@app.route("/game/instructions")
def cheat_sheet():
    return render_template("instructions.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.errorhandler(405)
def page_not_found(error):
    return render_template('method_not_allowed.html'), 405


if __name__ == '__main__':
    app.secret_key = "ihaveasecretkey5"
    app.run(host="localhost", port="5000")