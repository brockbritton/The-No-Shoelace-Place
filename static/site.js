
var master_return = '';
var master_helper = '';

var rate_of_letters = 5;

function accept_input_ajax(data_values, route) {
    $.ajax({
        url: route,
        data: data_values,
        type: 'POST',
        success: function(response){
            master_return = response.dest;
            master_helper = response.helper;
            print_all(response.actions['print_all']);
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
        'dest' : master_return,
        'helper' : master_helper
    }
    accept_input_ajax(data_values, '/accept-input-data');
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
    var par = document.createElement("p");
    par.classList.add("command_input_text");
    game_display_div.appendChild(par);
    print_letter_by_letter(text, par)

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



function build_multiple_choice(display_strings, values) {
    let buttons_div = domument.getElementById("button_entry_div");
    for (let i=0; i < display_strings.length; i++) {
        let btn = document.createElement("btn");
        btn.classList.add("enter_button");
        btn.innerHTML = display_strings[i];
        btn.value = values[i];
        buttons_div.appendChild(btn);
    }
    document.getElementById("text_entry_div").style.display = "none";
    document.getElementById("button_entry_div").style.display = "block";

}

function accept_button_input(value, display) {
    /* pass */
}

function ask_y_n() {
    
    build_multiple_choice(["Yes", "No"], ["y", "n"])
}

function toggle_dynamic_input(bind_or_unbind) {
    /* pass */
}

function display_quote(quote, author) {
    /* pass */
}