


from flask import Flask, jsonify, render_template, request
import game_backend.input_organizer as input_organizer
import jsonpickle
import game_backend.classes.ability_class as ability_class
import game_backend.classes.character_class as character_class
import game_backend.classes.item_class as item_class
import game_backend.classes.calendar_class as calendar_class
import game_backend.classes.condition_class as condition_class
import game_backend.classes.room_class as room_class
import game_backend.classes.npc_class as npc_class



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
        if data_dict[key] == 'null':
            data_dict[key] = None
    
    #toggle_dynamic_input("unbind")

    print("orig dest ", data_dict['dest'])
    print(data_dict)

    return_tuple = input_organizer.organize_raw_input(data_dict['dest'], data_dict['input'].strip(), data_dict['helper'])
    return_data_dict = {
        'dest': return_tuple[0],
        'helper': return_tuple[1],
        'actions': return_tuple[2]
    }
    print("return data dict 1: ", return_data_dict)

    #classes_tuple = (ability_class.Ability, character_class.Character, item_class.Item, calendar_class.Calendar, condition_class.Condition, room_class.Room, npc_class.NPC)
    for key, value in return_data_dict.items():
        if key != 'actions':
            return_data_dict[key] = jsonpickle.encode(value, unpicklable=True)
        else:
            for key, value in return_data_dict['actions'].items():
                if key != 'print_all':
                    return_data_dict['actions'][key] = jsonpickle.encode(value, unpicklable=True)
            
    print("return data dict 2: ", return_data_dict)
    #if not self.multi_buttons_container.winfo_ismapped():
    #    self.toggle_dynamic_input("bind")
    #    self.game_input.configure(state='normal')
    
    return return_data_dict


@app.route("/tnslp/start-game", methods=['POST'])
def start_game():
    print("start game start")
    return_tuple = input_organizer.start_game()
    return_data_dict = {
        'dest': return_tuple[0],
        'helper': return_tuple[1],
        'actions': return_tuple[2]
    }
    print(return_data_dict)
    for key, value in return_data_dict.items():
        if key != 'actions':
            return_data_dict[key] = jsonpickle.encode(value, unpicklable=True)
    print(return_data_dict)
    print("start game end")
    print()
    return return_data_dict


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=False)