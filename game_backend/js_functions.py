__all__ = ['js_functions']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['print_all', 'accept_entry_input', 'ask_y_n', 'print_letter_by_letter', 'display_quote', 'master_return', 'master_helper', 'accept_button_input', 'build_multiple_choice', 'printtk', 'toggle_dynamic_input'])
@Js
def PyJsHoisted_printtk_(text, this, arguments, var=var):
    var = Scope({'text':text, 'this':this, 'arguments':arguments}, var)
    var.registers(['text', 'par'])
    var.put('par', var.get('document').callprop('createElement', Js('p')))
    var.get('par').get('classList').callprop('add', Js('command_input_text'))
    var.get('game_display_div').callprop('appendChild', var.get('par'))
    var.get('print_letter_by_letter')(var.get('text'), var.get('par'))
PyJsHoisted_printtk_.func_name = 'printtk'
var.put('printtk', PyJsHoisted_printtk_)
@Js
def PyJsHoisted_print_letter_by_letter_(text, par_element, this, arguments, var=var):
    var = Scope({'text':text, 'par_element':par_element, 'this':this, 'arguments':arguments}, var)
    var.registers(['text', 'par_element'])
    if (var.get('text').get('length')==Js(1.0)):
        var.get('par_element').put('innerHTML', var.get('text'), '+')
    else:
        var.get('par_element').put('innerHTML', var.get('text').get('0'))
        var.get('setTimeout')(var.get('print_letter_by_letter').callprop('bind', var.get(u"null"), var.get('text').callprop('slice', Js(1.0)), var.get('par_element')), Js(100.0))
    var.get('game_display_div').put('scrollTop', var.get('game_display_div').get('scrollHeight'))
PyJsHoisted_print_letter_by_letter_.func_name = 'print_letter_by_letter'
var.put('print_letter_by_letter', PyJsHoisted_print_letter_by_letter_)
@Js
def PyJsHoisted_print_all_(list, this, arguments, var=var):
    var = Scope({'list':list, 'this':this, 'arguments':arguments}, var)
    var.registers(['list'])
    var.get('printtk')(var.get('list').get('0'))
    var.get('setTimeout')(var.get('print_all').callprop('bind', var.get(u"null"), var.get('list').callprop('slice', Js(1.0))), (Js(100.0)*var.get('list').get('0').get('length')))
PyJsHoisted_print_all_.func_name = 'print_all'
var.put('print_all', PyJsHoisted_print_all_)
@Js
def PyJsHoisted_accept_entry_input_(event, this, arguments, var=var):
    var = Scope({'event':event, 'this':this, 'arguments':arguments}, var)
    var.registers(['data_values', 'event', 'input_text'])
    var.get('event').callprop('preventDefault')
    var.put('input_text', var.get('form').get('elements').get('0').get('value'))
    var.get('printtk')((Js('>   ')+var.get('input_text')))
    var.put('data_values', Js({'input':var.get('input_text'),'dest':var.get('master_return'),'helper':var.get('master_helper')}))
    @Js
    def PyJs_anonymous_0_(response, this, arguments, var=var):
        var = Scope({'response':response, 'this':this, 'arguments':arguments}, var)
        var.registers(['response'])
        var.get('console').callprop('log', var.get('response'))
    PyJs_anonymous_0_._set_name('anonymous')
    @Js
    def PyJs_anonymous_1_(error, this, arguments, var=var):
        var = Scope({'error':error, 'this':this, 'arguments':arguments}, var)
        var.registers(['error'])
        var.get('console').callprop('log', var.get('error'))
    PyJs_anonymous_1_._set_name('anonymous')
    var.get('$').callprop('ajax', Js({'url':Js('/accept-input-data'),'data':var.get('data_values'),'type':Js('POST'),'success':PyJs_anonymous_0_,'error':PyJs_anonymous_1_}))
    var.get('form').get('elements').get('0').put('value', Js(''))
PyJsHoisted_accept_entry_input_.func_name = 'accept_entry_input'
var.put('accept_entry_input', PyJsHoisted_accept_entry_input_)
@Js
def PyJsHoisted_accept_button_input_(value, display, this, arguments, var=var):
    var = Scope({'value':value, 'display':display, 'this':this, 'arguments':arguments}, var)
    var.registers(['value', 'display'])
    pass
PyJsHoisted_accept_button_input_.func_name = 'accept_button_input'
var.put('accept_button_input', PyJsHoisted_accept_button_input_)
@Js
def PyJsHoisted_build_multiple_choice_(display_strings, values, this, arguments, var=var):
    var = Scope({'display_strings':display_strings, 'values':values, 'this':this, 'arguments':arguments}, var)
    var.registers(['display_strings', 'values'])
    pass
PyJsHoisted_build_multiple_choice_.func_name = 'build_multiple_choice'
var.put('build_multiple_choice', PyJsHoisted_build_multiple_choice_)
@Js
def PyJsHoisted_ask_y_n_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.get('build_multiple_choice')(Js([Js('Yes'), Js('No')]), Js([Js('y'), Js('n')]))
PyJsHoisted_ask_y_n_.func_name = 'ask_y_n'
var.put('ask_y_n', PyJsHoisted_ask_y_n_)
@Js
def PyJsHoisted_toggle_dynamic_input_(bind_or_unbind, this, arguments, var=var):
    var = Scope({'bind_or_unbind':bind_or_unbind, 'this':this, 'arguments':arguments}, var)
    var.registers(['bind_or_unbind'])
    pass
PyJsHoisted_toggle_dynamic_input_.func_name = 'toggle_dynamic_input'
var.put('toggle_dynamic_input', PyJsHoisted_toggle_dynamic_input_)
@Js
def PyJsHoisted_display_quote_(quote, author, this, arguments, var=var):
    var = Scope({'quote':quote, 'author':author, 'this':this, 'arguments':arguments}, var)
    var.registers(['quote', 'author'])
    pass
PyJsHoisted_display_quote_.func_name = 'display_quote'
var.put('display_quote', PyJsHoisted_display_quote_)
var.put('master_return', var.get(u"null"))
var.put('master_helper', var.get(u"null"))
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass


# Add lib to the module scope
js_functions = var.to_python()