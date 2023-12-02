
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
import tnslp.game_backend.classes.game_class as game_class
import re

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
app.debug = True 
Session(app)

@app.before_first_request 
def before_first_request(): 
    session.clear() 

    session['current_js_actions'] = {
        'build_multiple_choice': None,
    }

    try:
        if session['game'] is not None:
            print("--- game already exists ---")

    except KeyError: 
        session['game'] = game_class.Game()
        print("--- game created ---")

    session.modified = True

    return session

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

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


@app.route("/game/accept-data", methods=['POST'])
def accept_data():
    input_data = request.json['input']
    print("frontend input ", input_data)
    return session['game'].organize_raw_input(input_data)
    
@app.route("/game/request-map-data", methods=['GET'])
def request_map_data():
    return session['game'].return_map_data()

@app.route("/game/request-player-data", methods=['GET'])
def request_backend_player_data():
    ui_dict = {
        #patient stats
        "stats" : session['game'].get_player_attr(),
        #inventory
        "inventory" : session['game'].get_player_inventory(),
        #skills levels
        "skills" : session['game'].get_player_skills_lvl()
    }
    return ui_dict

@app.route("/game/loading-game", methods=['POST'])
def loading_game():
    if len(session['game'].save_prints) <= session['game'].starting_pars: 
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
    

    