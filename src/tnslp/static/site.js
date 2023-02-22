

const rate_of_letters = 20; /* fast: 5, normal: 20, slow: 50 */
const rate_of_header_fadein = 500;
const quote_fadein_rate = 2000;
let on_header_element = false;


function ajax_accept_input(data_values, route) {
    toggle_return_listener("off");
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
                ajax_accept_input(data_values, "/game/loading-game")
            } else {
                printtk(`Error ${request.status}: see terminal for more information.` );
            }
        }
    }); 
}

function get_map_data() {
    $.ajax({
        url: '/game/request-map-data',
        type: 'GET',
        success: function(response) {
            //for (const [key, value] of response.entries())
            const ward_doors_container = document.getElementById("ward-doors-map")
            const ward_rooms_container = document.getElementById("ward-rooms-map")
            
            const key = "ward-rooms"
            const html_key = `${key}-map`
            for (i in response[key]) {
                if (response[key][i]) {
                    document.getElementById(html_key).children[i].classList.add("discovered-map")
                } else {
                    document.getElementById(html_key).children[i].classList.remove("discovered-map")
                }
            }

        },
        error: function(request, response, errors) {
            console.log(`Map Data Request: ${errors}`)
        }
    });
}

function accept_entry_input(event) {
    event.preventDefault();
    let input_text = form.elements[0].value;
    printtk(">   " + input_text)
    let data_values = {
        'input' : input_text,
    }
    ajax_accept_input(data_values, '/game/accept-input-data');
    form.elements[0].value = "";
}

function update_map_objects(bool_list) {

}

function default_return_press(event) {
    event.preventDefault()
}

function toggle_return_listener(on_off) {
    if (on_off == "on") {
        document.getElementById("text_entry_enter_button").disabled = false;
        document.getElementById("text_entry_enter_button").style.color = 'white';
        document.getElementById("text_entry_enter_button").style.borderColor = 'white';
        document.getElementById('command_input_form').removeEventListener('submit', default_return_press);  
        document.getElementById('command_input_form').addEventListener('submit', accept_entry_input);
        document.getElementById('command_input').focus();
    } else if (on_off == "off") {
        document.getElementById('command_input_form').removeEventListener('submit', accept_entry_input);  
        document.getElementById('command_input_form').addEventListener('submit', default_return_press);
        document.getElementById("text_entry_enter_button").disabled = true;
        document.getElementById("text_entry_enter_button").style.color = 'darkgrey';
        document.getElementById("text_entry_enter_button").style.borderColor = 'darkgrey';
        
    }
}

function print_all(pars_list, bmc_list, rebuild_text){
    if (pars_list.length == 0) {
        if (bmc_list.length > 0) {
            build_multiple_choice(bmc_list);
        } else {
            toggle_entry_divs("text");
            toggle_return_listener("on");
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
    for (let text in list) {
        let par = document.createElement("p");
        if (list[text] instanceof Array) {
            if (list[text][1] == "quote") {
                par.classList.add("quote_text");
                par.innerHTML = list[text][0];
            } 
        } else {
            par.classList.add("command_input_text");
            par.innerHTML = list[text];
        }
        document.getElementById("game_text_display").appendChild(par);
    }
    game_display_div.scrollTop = game_display_div.scrollHeight;

    if (bmc_list != undefined) {
        build_multiple_choice(bmc_list);
    } else {
        toggle_entry_divs("text");
        toggle_return_listener("on");
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
            document.getElementById("game_text_display").appendChild(par);
            fade_in_quote_line(par);
        }
    } else {
        par.classList.add("command_input_text");
        document.getElementById("game_text_display").appendChild(par);
        print_letter_by_letter(text, par);
    }
}

function print_letter_by_letter(text, par_element) {
    if (text.length == 1) {
        par_element.innerHTML += text
    } else {
        par_element.innerHTML += text[0]
        setTimeout(print_letter_by_letter.bind(null, text.slice(1), par_element), rate_of_letters)
    }
    game_display_div.scrollTop = game_display_div.scrollHeight;
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
    for (let i=0; i < display_strings.length; i++) {
        let btn = document.createElement("btn");
        btn.classList.add("game_multiple_choice_buttons");
        btn.innerHTML = display_strings[i];
        btn.value = i;
        btn.onclick = accept_button_input.bind(null, display_strings[i], i);
        button_entry_div.appendChild(btn);
    }
}

function toggle_entry_divs(element_type) {
    if (element_type == "button") {
        text_entry_div.style.display = "none";
        button_entry_div.style.display = "block";
    } else if (element_type == "text") {
        button_entry_div.style.display = "none";
        text_entry_div.style.display = "block";
    }
}


function accept_button_input(display, button_index) {
    printtk(">   " + display)
    let data_values = {
        'input' : button_index,
    }
    ajax_accept_input(data_values, '/game/accept-input-data');
    
    button_entry_div.style.display = "none";
    while (button_entry_div.firstChild) {
        button_entry_div.removeChild(button_entry_div.firstChild);
    } 
}

function update_inv_visual(inv_strings) {
    for (let i=0; i < 6; i++) {
        let elem_id = "inv_slot_" + (i+1).toString();
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

function fade_to_fill_header() {
    if (parseFloat(foreground_header_image.style.opacity) == 0) {
        on_header_element = true;

    }
    if (parseFloat(foreground_header_image.style.opacity) < 1 && on_header_element) {
        foreground_header_image.style.opacity = parseFloat(foreground_header_image.style.opacity) + 1.0/60;
        setTimeout(fade_to_fill_header, rate_of_header_fadein / 60);
    } 
}

function switch_to_outline_header() {
    foreground_header_image.style.opacity = 0;
    on_header_element = false;
}

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