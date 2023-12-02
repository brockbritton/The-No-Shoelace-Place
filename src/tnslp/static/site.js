

const rate_of_letters = 20; /* fast: 5, normal: 20, slow: 50 */
const rate_of_header_fadein = 500;
const quote_fadein_rate = 2000;
let on_header_element = false;

function accept_entry_input() {
    const input_element = document.getElementById("player-text-input");
    const input_text = input_element.value
    printtk(">   " + input_text)
    let data_values = {
        'input' : input_text,
    }
    fetchPostEndpoint(data_values, '/game/accept-data');
    input_element.value = "";
}

function accept_button_input(display, button_index) {
    printtk(">   " + display)
    let data_values = {
        'input' : button_index,
    }
    fetchPostEndpoint(data_values, '/game/accept-data');
    const button_entry_div = document.getElementById("button-entry-div");
    button_entry_div.style.display = "none";
    while (button_entry_div.firstChild) {
        button_entry_div.removeChild(button_entry_div.firstChild);
    } 
}

async function fetchPostEndpoint(data, route) {
    //disable play button
    document.getElementById("text-entry-enter-button").disabled = true;
    try {
        const request_options = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        const response = await fetch(route, request_options)
        const response_data = await response.json()

        if (response_data != null) {
            if ('print_all' in response_data) {
                print_all.apply(null, [response_data['print_all'], response_data['build_multiple_choice'], response_data['rebuild_text_entry']])
                
            } else if (('load_prints' in response_data)) {
                load_prints(response_data['load_prints'], response_data['build_multiple_choice']);
            }

            update_frontend_player_data()
        }
    } catch (error) {
        //console.log(error)
        if (route == "/game/loading-game") {
            //await fetchPostEndpoint(data, "/game/loading-game")
        } else {
            printtk(`Post Error ${error.status}: see terminal for more information.`);
        }
    }
}

function print_all(pars_list, bmc_list, rebuild_text){
    if (pars_list.length == 0) {
        if (bmc_list.length > 0) {
            build_multiple_choice(bmc_list);
        } else {
            document.getElementById("text-entry-enter-button").disabled = false;
            toggle_entry_divs("text");
        }
    
    } else {
        printtk(pars_list[0]);
        if (pars_list[0] instanceof Array) {
            if (pars_list[0][1] == "quote") {
                setTimeout(print_all.bind(null, pars_list.slice(1), bmc_list, rebuild_text), quote_fadein_rate);
            } else if (pars_list[0][1] == "riddle") {
                setTimeout(print_all.bind(null, pars_list.slice(1), bmc_list, rebuild_text), quote_fadein_rate);
            }
        } else {
            //this timeout isnt perfect. the next paragraph starts printing before this is done.
            //need to add some more time?
            //+ (rate_of_letters*(pars_list[0].length/2.5)) ish
            setTimeout(print_all.bind(null, pars_list.slice(1), bmc_list, rebuild_text), rate_of_letters*pars_list[0].length); //
        }
    }
}

function load_prints(list, bmc_list) {
    const game_text_display = document.getElementById("game-text-display")
    for (let text in list) {
        let par = document.createElement("p");
        if (list[text] instanceof Array) {
            par.classList.add(`${list[text][1]}-text`);
            par.innerHTML = list[text][0];
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
        document.getElementById("text-entry-enter-button").disabled = false;
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
            par.classList.add("quote-text");
            par.innerHTML = text[0];
            par.style.opacity = 0;
            document.getElementById("game-text-display").appendChild(par);
            fade_in_quote_line(par);
        } else if (text[1] == "riddle") {
            par.classList.add("riddle-text");
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
    const game_text_display = document.getElementById("game-text-display")
    if (par_element.style.opacity != 1) {
        if (parseFloat(par_element.style.opacity) + quote_opacity_rate >= 1) {
            par_element.style.opacity = 1;
        } else {
            par_element.style.opacity = parseFloat(par_element.style.opacity) + quote_opacity_rate;
        }
        setTimeout(fade_in_quote_line.bind(null, par_element), quote_fadein_rate * quote_opacity_rate);
    } 
    game_text_display.scrollTop = game_text_display.scrollHeight;
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
        document.getElementById("player-text-input").focus()
    }  
}

function build_inv_labels(html_element, text_string) {
    
}

async function update_frontend_player_data() {
    $.ajax({
        url: '/game/request-player-data',
        type: 'GET',
        success: function(response) {

            // Updating Section "Player Info"
            const stats_html_elements = document.getElementsByClassName("ps-values")
            for (let i = 0; i < response["stats"].length; i++) {
                if (response["stats"][i] != null) {
                    stats_html_elements[i].innerHTML = String(response["stats"][i]);
                } else {
                    stats_html_elements[i].innerHTML = "Unknown"; 
                }
            }
            
            //Updating Section "Inventory"
            for (let i = 0; i < 6; i++) {
                const inv_label = document.getElementById(`inv-slot-${(i+1).toString()}`)
                if (inv_label.innerHTML != response["inventory"][i]) {
                    inv_label.innerHTML = ""
                    if (response["inventory"][i].length != 0) {
                        //let curr_step = -1;
                        const label_array = response["inventory"][i].split("") 
                        for (let j = 0; j < label_array.length; j++) {
                            
                            inv_label.innerHTML += label_array[j] 
                            /*
                            setTimeout(function() { 
                                inv_label.innerHTML += label_array[j] 
                                console.log(j, inv_label.innerHTML)
                                
                            }, i*1000 + 200);
                            */
                        }    
                    }
                } 
            }
            

            //Updating Section "Skills"
            const skills_html_elements = document.getElementsByClassName("player-skills-lvl")
            
            for (let i = 0; i < response["skills"].length; i++) {
                skills_html_elements[i].innerHTML = String(response["skills"][i]);
                
                if (response["skills"][i] > 0) {
                    //add class that takes away blur from name
                    const skills_string = document.getElementById(`${skills_html_elements[i].id.slice(0, -4)}-string`)
                    skills_string.classList.add("learned")
                }
                
            }
        },
        error: function(request, response, errors) {
            console.log(`Player Data Request: ${errors}`)
        }
    });
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