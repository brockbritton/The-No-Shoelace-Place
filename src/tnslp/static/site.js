

const rate_of_letters = 20; /* fast: 5, normal: 20, slow: 50 */
const rate_of_header_fadein = 500;
const quote_fadein_rate = 2000;
let on_header_element = false;

/*
const form = document.getElementById('command_input_form');
const game_display_div = document.getElementById("game-text-display");

const text_entry_div = document.getElementById("text_entry_div");
const text_entry = document.getElementById('command_input');
const button_entry_div = document.getElementById("button_entry_div");

const image_header = document.getElementById("image_header");
const foreground_header_image = document.getElementById("foreground_image");
*/

function accept_entry_input() {
    const input_element = document.getElementById("player-text-input");
    const input_text = input_element.value
    printtk(">   " + input_text)
    let data_values = {
        'input' : input_text,
    }
    ajaxAcceptInput(data_values, '/game/accept-input-data');
    input_element.value = "";
}

function accept_button_input(display, button_index) {
    printtk(">   " + display)
    let data_values = {
        'input' : button_index,
    }
    ajaxAcceptInput(data_values, '/game/accept-input-data');
    const button_entry_div = document.getElementById("button-entry-div");
    button_entry_div.style.display = "none";
    while (button_entry_div.firstChild) {
        button_entry_div.removeChild(button_entry_div.firstChild);
    } 
}

function ajaxAcceptInput(data_values, route) {
    $.ajax({
        url: route,
        data: data_values,
        type: 'POST',
        success: function(response) {
            if ('print_all' in response) {
                print_all.apply(null, [response['print_all'], response['build_multiple_choice'], response['rebuild_text_entry']])
                
            } else if (('load_prints' in response)) {
                load_prints(response['load_prints'], response['build_multiple_choice']);
            }
            
            if (('update_inv_visual' in response) && (response['update_inv_visual'].length != 0)) {
                update_inv_visual(response['update_inv_visual']);
            }

            if (('update_ui_values' in response) && (response['update_ui_values'].length != 0)) {
                update_ui_values(response['update_ui_values']);
            } 
        },
        error: function(request, response, errors){
            if (route == "/game/loading-game") {
                ajaxAcceptInput(data_values, "/game/loading-game")
            } else {
                printtk(`Error ${request.status}: see terminal for more information.` );
            }
        }
    }); 
}

function print_all(pars_list, bmc_list, rebuild_text){
    if (pars_list.length == 0) {
        if (bmc_list.length > 0) {
            build_multiple_choice(bmc_list);
        } else {
            toggle_entry_divs("text");
        }
    } else {
        printtk(pars_list[0]);
        if (pars_list[0] instanceof Array) {
            if (pars_list[0][1] == "quote") {
                setTimeout(print_all.bind(null, pars_list.slice(1), bmc_list, rebuild_text), quote_fadein_rate);
            }
        } else {
            setTimeout(print_all.bind(null, pars_list.slice(1), bmc_list, rebuild_text), rate_of_letters*pars_list[0].length);
        }
    }
}

function load_prints(list, bmc_list) {
    const game_text_display = document.getElementById("game-text-display")
    for (let text in list) {
        let par = document.createElement("p");
        if (list[text] instanceof Array) {
            if (list[text][1] == "quote") {
                par.classList.add("quote_text");
                par.innerHTML = list[text][0];
            } 
        } else {
            par.classList.add("standard-display-text");
            par.innerHTML = list[text];
        }
        game_text_display.appendChild(par);
    }
    game_text_display.scrollTop = game_text_display.scrollHeight;

    if (bmc_list != undefined) {
        build_multiple_choice(bmc_list);
    } else {
        toggle_entry_divs("text");
    }
}

function printtk(text) {
    //this function pays tribute to how i wrote the game first in tkinter
    if (text == null) {
        text = "null_data";
    } 
    
    const par = document.createElement("p");
    if (text instanceof Array) {
        if (text[1] == "quote") {
            par.classList.add("quote_text");
            par.innerHTML = text[0];
            par.style.opacity = 0;
            document.getElementById("game-text-display").appendChild(par);
            fade_in_quote_line(par);
        }
    } else {
        par.classList.add("standard-display-text");
        document.getElementById("game-text-display").appendChild(par);
        print_letter_by_letter(text, par);
    }
}

function print_letter_by_letter(text, par_element) {
    const game_text_display = document.getElementById("game-text-display")
    if (text.length == 1) {
        par_element.innerHTML += text
    } else {
        par_element.innerHTML += text[0]
        setTimeout(print_letter_by_letter.bind(null, text.slice(1), par_element), rate_of_letters)
    }
    game_text_display.scrollTop = game_text_display.scrollHeight;
}

const quote_opacity_rate = 0.01;
function fade_in_quote_line(par_element) {
    
    if (par_element.style.opacity != 1) {
        if (parseFloat(par_element.style.opacity) + quote_opacity_rate >= 1) {
            par_element.style.opacity = 1;
        } else {
            par_element.style.opacity = parseFloat(par_element.style.opacity) + quote_opacity_rate;
        }
        setTimeout(fade_in_quote_line.bind(null, par_element), quote_fadein_rate * quote_opacity_rate);
    } 
    game_display_div.scrollTop = game_display_div.scrollHeight;
}

function build_multiple_choice(display_strings) {
    toggle_entry_divs("button");
    const button_entry_div = document.getElementById("button-entry-div");
    for (let i=0; i < display_strings.length; i++) {
        let btn = document.createElement("button");
        btn.classList.add("gameplay-buttons");
        btn.innerHTML = display_strings[i].toLowerCase();
        btn.value = i;
        btn.onclick = accept_button_input.bind(null, display_strings[i], i);
        button_entry_div.appendChild(btn);
    }
}

function toggle_entry_divs(element_type) {
    const text_entry_div = document.getElementById("text-entry-div");
    const button_entry_div = document.getElementById("button-entry-div");
    if (element_type == "button") {
        text_entry_div.style.display = "none";
        button_entry_div.style.display = "block";
    } else if (element_type == "text") {
        button_entry_div.style.display = "none";
        text_entry_div.style.display = "block";
    }
}

function update_inv_visual(inv_strings) {
    for (let i=0; i < 6; i++) {
        let elem_id = "inv-slot-" + (i+1).toString();
        if (document.getElementById(elem_id).innerHTML != inv_strings[i]) {
            document.getElementById(elem_id).innerHTML = "";
            build_inv_labels_letter_by_letter(elem_id, inv_strings[i]);
        } 
    }
}

function build_inv_labels_letter_by_letter(id, text_string) {
    let elem = document.getElementById(id);
    if (text_string.length == 0) {
        elem.innerHTML = "";
    } else {
        if (text_string.length == 1) {
            elem.innerHTML += text_string
        } else {

            elem.innerHTML += text_string[0]
            setTimeout(build_inv_labels_letter_by_letter.bind(null, id, text_string.slice(1)), rate_of_letters * (text_string.length)/4)
        }
    }
}

function update_ui_values(list_pairs) {
    for (let id_value_pair of list_pairs) {
        if (document.getElementById(id_value_pair[0]).innerHTML != id_value_pair[1]) {
            document.getElementById(id_value_pair[0]).innerHTML = id_value_pair[1];
        } 
    }
}


// Frontend Map Functions \\

function toggleGameMap() {
    const map_window = document.getElementById("game-map")
    const game_window = document.getElementById("game_gui")
    if (map_window.style.display == "block") {
        map_window.style.display = "none";
        game_window.style.filter = "none";
    } else {
        get_map_data()
        map_window.style.display = "block";
        game_window.style.filter = "blur(5px)";
    }

}

function get_map_data() {
    $.ajax({
        url: '/game/request-map-data',
        type: 'GET',
        success: function(response) {
            //const map_levels = ["ward", "basement"]
            const map_levels = ["ward"]
            for (let i in map_levels) {
                const map_objects = ["rooms", "doors"]
                for (let j in map_objects) {
                    let html_key = `${map_levels[i]}-${map_objects[j]}-map`
                    for (let r in response[`${map_levels[i]}-${map_objects[j]}`]) {
                        if (response[`${map_levels[i]}-${map_objects[j]}`][r]) {
                            document.getElementById(html_key).children[r].classList.add("discovered-map")
                        } else {
                            document.getElementById(html_key).children[r].classList.remove("discovered-map")
                        }
                    }
                }
            }
        },
        error: function(request, response, errors) {
            console.log(`Map Data Request: ${errors}`)
        }
    });
}

function update_map_objects(bool_list) {

}