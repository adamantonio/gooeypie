import gooeypie as gp
from random import choice


app = gp.GooeyPieApp('Input widget')


# EVENT FUNCTIONS #

def get_text(event):
    log.prepend_line(f'Text is {repr(main_inp.text)}')


def set_text(event):
    value = set_text_inp.text
    main_inp.text = value
    log.prepend_line(f'Set text to {repr(value)}')


def select(event):
    main_inp.select()
    log.prepend_line(f'Selected text')


def focus(event):
    main_inp.set_focus()
    log.prepend_line(f'Set focus')


def justify_text(event):
    setting = justify_radios.selected.lower()
    main_inp.justify = setting
    log.prepend_line(f'Setting justify property to {setting}')


def change_width(event):
    inc = 1
    if event.widget == increase_width_btn:
        main_inp.width += inc
        action = 'Increased'
    else:
        main_inp.width -= inc
        action = 'Decreased'

    log.prepend_line(f'{action} width by {inc} to {main_inp.width}')


def get_width(event):
    log.prepend_line(f'Width is {main_inp.width}')


def set_width(event):
    try:
        main_inp.width = int(set_width_inp.text)
        log.prepend_line(f'Set width to {repr(set_width_inp.text)}')
    except ValueError:
        log.prepend_line(f'Invalid value set for width')


def change_state(event):
    if event.widget == state_btn:
        main_inp.disabled = not main_inp.disabled
    else:
        main_inp.secret = not main_inp.secret


def input_changed(event):
    if event_chk.checked:
        log.prepend_line(f'Input changed to {main_inp.text}')


# DEFINE CONTAINERS #

# Main label containers
widget_container = gp.LabelContainer(app, 'Input widget')
testing_container = gp.LabelContainer(app, 'Operations')
log_container = gp.LabelContainer(app, 'Log')

# Operations containers
text_actions = gp.Container(testing_container)
width_actions = gp.Container(testing_container)
state_actions = gp.Container(testing_container)


# CREATE WIDGETS #

# The test subject
main_inp = gp.Input(widget_container)
main_inp.add_event_listener('change', input_changed)

# Text actions
text_action_lbl = gp.Label(testing_container, 'Text')
get_text_btn = gp.Button(text_actions, 'Get', get_text)
set_text_btn = gp.Button(text_actions, 'Set', set_text)
set_text_inp = gp.Input(text_actions)
select_text_btn = gp.Button(text_actions, 'Select', select)
focus_text_btn = gp.Button(text_actions, 'Focus', focus)

# Justify
justify_lbl = gp.Label(testing_container, 'Justify')
justify_radios = gp.Radiogroup(testing_container, ['Left', 'Center', 'Right'], 'horizontal')
justify_radios.add_event_listener('change', justify_text)

# Width
width_lbl = gp.Label(testing_container, 'Width')
increase_width_btn = gp.Button(width_actions, '+', change_width)
increase_width_btn.width = 4
decrease_width_btn = gp.Button(width_actions, '-', change_width)
decrease_width_btn.width = 4
get_width_btn = gp.Button(width_actions, 'Get', get_width)
set_width_btn = gp.Button(width_actions, 'Set', set_width)
set_width_inp = gp.Input(width_actions)

# State
state_lbl = gp.Label(testing_container, 'State')
state_btn = gp.Button(state_actions, 'Enable/disable', change_state)
secret_btn = gp.Button(state_actions, 'Toggle secret', change_state)

# Input supports the change event
event_lbl = gp.Label(testing_container, 'Events')
event_chk = gp.Checkbox(testing_container, 'Enable change event logging')

# Log
log = gp.Textbox(log_container)
log.height = 10


# ADD ALL WIDGETS #

# Input container
widget_container.set_grid(1, 1)
widget_container.add(main_inp, 1, 1)

# Text buttons
text_actions.set_grid(1, 5)
text_actions.add(get_text_btn, 1, 1)
text_actions.add(set_text_btn, 1, 2)
text_actions.add(set_text_inp, 1, 3)
text_actions.add(select_text_btn, 1, 4)
text_actions.add(focus_text_btn, 1, 5)

# Width buttons
width_actions.set_grid(1, 5)
width_actions.add(increase_width_btn, 1, 1)
width_actions.add(decrease_width_btn, 1, 2)
width_actions.add(get_width_btn, 1, 3)
width_actions.add(set_width_btn, 1, 4)
width_actions.add(set_width_inp, 1, 5)

# State buttons
state_actions.set_grid(1, 2)
state_actions.add(state_btn, 1, 1)
state_actions.add(secret_btn, 1, 2)

# Testing container
testing_container.set_grid(5, 2)
testing_container.add(text_action_lbl, 1, 1)
testing_container.add(text_actions, 1, 2)
testing_container.add(justify_lbl, 2, 1)
testing_container.add(justify_radios, 2, 2)
testing_container.add(width_lbl, 3, 1)
testing_container.add(width_actions, 3, 2)
testing_container.add(state_lbl, 4, 1)
testing_container.add(state_actions, 4, 2)
testing_container.add(event_lbl, 5, 1)
testing_container.add(event_chk, 5, 2)

# Log area
log_container.set_grid(1, 1)
log_container.add(log, 1, 1, fill=True)

# Add everything to main app
app.set_grid(3, 1)
app.add(widget_container, 1, 1, fill=True)
app.add(testing_container, 2, 1, fill=True)
app.add(log_container, 3, 1, fill=True)

# Give the input a random value
main_inp.text = choice(['Chocolate', 'The rain in Spain falls mainly on the ground', '😀'])


app.run()
