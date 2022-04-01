

from flask import Flask, render_template, request
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

@app.route("/tnslp", methods=('GET', 'POST'))
def tnslp():
    return render_template("game_page.html")


@app.route("/accept-input_data", methods=['POST'])
def accept_input_data():
    data_dict = request.form.to_dict()
    print(data_dict)
    
    #toggle_dynamic_input("unbind")

    
    print("orig dest ", data_dict.values()[1])

    return_data_dict = {
        'dest': None,
        'helper': None
    }


    #return_data_dict['dict'], return_data_dict['helper'] = input_organizer.organize_raw_input(data_dict.values()[1], data_dict.values()[0].strip(), data_dict.values()[2])
    
    #if not self.multi_buttons_container.winfo_ismapped():
    #    self.toggle_dynamic_input("bind")
    #    self.game_input.configure(state='normal')
    return return_data_dict


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)