
var master_return = null
var master_helper = null

function printtk(text) {
    var par = document.createElement("p");
    par.classList.add("command_input_text");
    par.innerHTML = text
    game_display_div.appendChild(par);
    game_display_div. scrollTop = game_display_div.scrollHeight;
}

function accept_entry_input(event) {
    /* is executing */
    event.preventDefault()
    var input_text = form.elements[0].value;
    printtk(">   " + input_text)
    let data_values = {
        'input' : input_text,
        'dest' : master_return,
        'helper' : master_helper
    }

    $.ajax({
        url: '/accept-input_data',
        data: data_values,
        type: 'POST',
        success: function(response){
            console.log(response);
        },
        error: function(error){
            console.log(error);
        }
    }); 
    form.elements[0].value = "";
}

function accept_button_input(value, display) {
    /* pass */
}

function build_multiple_choice(display_strings, values) {
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