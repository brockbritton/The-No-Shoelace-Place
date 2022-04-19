
var master_return = '';
var master_helper = '';

var rate_of_letters = 20; /* fast: 5, slow: 50, normal: 20 */


function ajax_accept_input(data_values, route) {
    $.ajax({
        url: route,
        data: data_values,
        type: 'POST',
        success: function(response){
            print_all(response['print_all']);
            
            if (('update_inv_visual' in response) && (response['update_inv_visual'].length != 0)) {
                update_inv_visual(response['update_inv_visual']);
            }

            if (('build_multiple_choice' in response) && (response['build_multiple_choice'].length != 0)) {
                build_multiple_choice(response['build_multiple_choice']);
            } else if (('rebuild_text_entry' in response) && (response['rebuild_text_entry'])) {
                toggle_entry_divs("text");
            }
            
            /* toggle dynamic input to on if the basic text entry has been enabled */
        },
        error: function(error){
            print_all(["Error: " + error]);
        }
    }); 
}

function accept_entry_input(event) {
    event.preventDefault()
    var input_text = form.elements[0].value;
    printtk(">   " + input_text)
    let data_values = {
        'input' : input_text,
    }
    ajax_accept_input(data_values, '/accept-input-data');
    form.elements[0].value = "";
}

function print_all(list){
    if (list.length == 1) {
        printtk(list[0]);
        setTimeout(document.getElementById("command_input").focus(), rate_of_letters*list[0].length);
    } else {
        printtk(list[0]);
        setTimeout(print_all.bind(null, list.slice(1)), rate_of_letters*list[0].length);
    }
}

function printtk(text) {
    if (text == null) {
        text = "null_data"
    }
    var par = document.createElement("p");
    par.classList.add("command_input_text");
    /* game_display_div defined on game page script */
    game_display_div.appendChild(par);
    print_letter_by_letter(text, par);
    
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

function build_multiple_choice(display_strings) {
    text_entry_div.style.display = "none";
    button_entry_div.style.display = "block";
    for (let i=0; i < display_strings.length; i++) {
        let btn = document.createElement("btn");
        btn.classList.add("enter_button");
        btn.innerHTML = display_strings[i];
        btn.value = i
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
    ajax_accept_input(data_values, '/accept-input-data');
    
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
 

function toggle_dynamic_input(bind_or_unbind) {
    /* pass */
}

function display_quote(quote, author) {
    /* pass */
}