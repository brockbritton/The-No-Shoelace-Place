


function printtk(text) {
    var par = document.createElement("p");
    par.classList.add("command_input_text");
    par.innerHTML = text
    game_display_div.appendChild(par);
    game_display_div.scrollTop = game_display_div.scrollHeight;
}

function accept_entry_input(event) {
    /* is executing */
    event.preventDefault()
    var input_text = form.elements[0].value;
    form.elements[0].value = "";
    printtk(">   " + input_text)
  
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