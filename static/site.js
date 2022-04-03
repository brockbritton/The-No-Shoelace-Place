
var master_return = null;
var master_helper = null;

var rate_of_letters = 5;

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

function print_all(list){
    printtk(list[0])
    setTimeout(print_all.bind(null, list.slice(1)), rate_of_letters*list[0].length)
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
        url: '/accept-input-data',
        data: data_values,
        type: 'POST',
        success: function(response){
            master_return = response.dest;
            master_helper = response.helper;
            print_all(response.print);
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