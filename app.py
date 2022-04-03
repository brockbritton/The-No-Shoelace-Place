


from flask import Flask, jsonify, render_template, request
import game_backend.input_organizer as input_organizer
import js2py

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

@app.route("/tnslp/", methods=('GET', 'POST'))
def tnslp():
    input_organizer.start_game()
       
    return render_template("game_page.html")


@app.route("/accept-input-data", methods=['POST'])
def accept_input_data():
    data_dict = request.form.to_dict()
    for key, value in data_dict.items():
        if data_dict[key] == "":
            data_dict[key] = None
    
    #toggle_dynamic_input("unbind")

    print("orig dest ", data_dict['dest'])

    return_tuple = input_organizer.organize_raw_input(data_dict['dest'], data_dict['input'].strip(), data_dict['helper'])
    return_data_dict = {
        'dest': return_tuple[0],
        'helper': return_tuple[1],
        'print': return_tuple[2]
    }

    #if not self.multi_buttons_container.winfo_ismapped():
    #    self.toggle_dynamic_input("bind")
    #    self.game_input.configure(state='normal')
    print(return_data_dict)
    return jsonify(return_data_dict)

@app.route("/tnslp/start-game", methods=['POST'])
def start_game():
    return_tuple = input_organizer.start_game()
    print(return_tuple)
    
    return jsonify({'dest': return_tuple[0], 'helper': return_tuple[1], 'print': return_tuple[2]})


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)