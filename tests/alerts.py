import gooeypie as gp
import random


icons = ['info', 'warning', 'error', 'question']
buttons = ['OK/Cancel', 'Yes/No', 'Retry/Cancel', 'Yes/No/Cancel']
titles = ['Short sensible title', 'Quite a long title that is probably too long to actually have as a title']
messages = ['A short message here', 'A longer message that will\ncontain some newlines.\n\nIt contains several']


def open_dialog(event):
    title = title_inp.text
    message = message_txt.text
    icon = icon_dd.selected
    if type_rdo.selected == 'Alert':
        log.prepend_line(f'Alert with icon {icon_dd.selected}')
        app.alert(title, message, icon)
    else:
        if buttons_dd.selected == 'OK/Cancel':
            result = app.confirm_okcancel(title, message, icon)
        if buttons_dd.selected == 'Yes/No':
            result = app.confirm_yesno(title, message, icon)
        if buttons_dd.selected == 'Retry/Cancel':
            result = app.confirm_retrycancel(title, message, icon)
        if buttons_dd.selected == 'Yes/No/Cancel':
            result = app.confirm_yesnocancel(title, message, icon)

        log.prepend_line(f'Confirmed {result} with icon {icon_dd.selected} and buttons {buttons_dd.selected}')


def type_change(event):
    """Removes or adds the question option for alerts"""
    if type_rdo.selected == 'Alert':
        buttons_lbl.disabled = True
        buttons_dd.disabled = True
    else:
        buttons_lbl.disabled = False
        buttons_dd.disabled = False


def set_randoms():
    """Just some random values that can run the test"""
    type_rdo.selected = random.choice(type_rdo.options)
    title_inp.text = random.choice(titles)
    message_txt.text = random.choice(messages)
    icon_dd.selected = random.choice(icons)
    buttons_dd.selected = random.choice(buttons_dd.items)


app = gp.GooeyPieApp('Dialog tests')
app.width = 500

options = gp.LabelContainer(app, 'Options')
log_cont = gp.LabelContainer(app, 'Log')

type_lbl = gp.Label(options, 'Dialog type')
type_rdo = gp.Radiogroup(options, ('Alert', 'Confirm'), 'horizontal')
title_lbl = gp.Label(options, 'Window title')
title_inp = gp.Input(options)
message_lbl = gp.Label(options, 'Message')
message_txt = gp.Textbox(options)
icon_lbl = gp.Label(options, 'Icon')
icon_dd = gp.Dropdown(options, icons)
buttons_lbl = gp.Label(options, 'Buttons')
buttons_dd = gp.Dropdown(options, buttons)
open_btn = gp.Button(options, 'Open dialog', open_dialog)

options.set_grid(6, 2)
options.set_column_weights(0, 1)
options.add(type_lbl, 1, 1)
options.add(type_rdo, 1, 2)
options.add(title_lbl, 2, 1)
options.add(title_inp, 2, 2, fill=True)
options.add(message_lbl, 3, 1)
options.add(message_txt, 3, 2, fill=True)
options.add(icon_lbl, 4, 1)
options.add(icon_dd, 4, 2, fill=True)
options.add(buttons_lbl, 5, 1)
options.add(buttons_dd, 5, 2, fill=True)
options.add(open_btn, 6, 2)

log = gp.Textbox(log_cont)
log_cont.set_grid(1, 1)
log_cont.add(log, 1, 1, fill=True)

app.set_grid(2, 1)
app.add(options, 1, 1, fill=True)
app.add(log_cont, 2, 1, fill=True)

type_rdo.add_event_listener('change', type_change)
set_randoms()
type_change(None)

app.run()
