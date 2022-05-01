
from flask import Flask, render_template, request, session, redirect, url_for
import game_backend.classes.game_class as game_class
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

    session['current_js_actions'] = {
        'build_multiple_choice': None,
    }

    try:
        if session['game'] is not None:
            print("game already exists")

    except KeyError:
        session['game'] = game_class.Game()
        print("game created")

@app.route("/")
def home():
    return redirect(url_for('welcome'))

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/quotes/")
def quotes():
    return render_template("quotes.html")

@app.route("/credits")
def credits():
    return render_template("credits.html")

@app.route("/game/", methods=('GET', 'POST'))
def play_game():
    session['game'].start_game()
    return render_template("game.html")


@app.route("/game/accept-input-data", methods=['POST'])
def accept_input_data():
    data_dict = request.form.to_dict()
    
    print("frontend input ", data_dict['input'])

    actions_dict = session['game'].organize_raw_input(data_dict['input'])
    return actions_dict
    

@app.route("/game/loading-game", methods=['POST'])
def loading_game():
    
    if len(session['game'].save_prints) <= 9:
        session['game'].save_prints = []
        return_dict = session['game'].start_game()
    else:
        return_dict = session['game'].load_game()

    return return_dict

@app.route("/game/cheat-sheet")
def cheat_sheet():
    return render_template("cheat_sheet.html")


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
    app.run(host="localhost", port=5000, debug=True)