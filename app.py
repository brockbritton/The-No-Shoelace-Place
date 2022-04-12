
from flask import Flask, jsonify, render_template, request, session
import game_backend.input_organizer as input_organizer


app = Flask(__name__)
app.secret_key = "ihaveasecretkey"
app.config['SESSION_TYPE'] = 'filesystem'

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
    print(type(data_dict['input']))

    #use js_return to send the correct part of master_return
    
    actions_dict = input_organizer.organize_raw_input(data_dict['input'])
    
    return actions_dict
    


@app.route("/tnslp/start-game", methods=['POST'])
def start_game():
    
    session['current_js_actions'] = {
        'build_multiple_choice': None,
    }

    js_data_dict = {
        'print_all': input_organizer.start_game()['print_all'],
        'build_multiple_choice': []
    }
    return js_data_dict

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=False)