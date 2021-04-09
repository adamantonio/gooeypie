import gooeypie as gp
from random import choice


app = gp.GooeyPieApp('StyleLabel widget')

# Define colour list
colours = [col.strip() for col in open('colours.txt').readlines()]


def change_size(event):
    inc = 3
    if event.widget == increase_size_btn:
        style_lbl.font_size += inc
        action = 'Increased'
    else:
        style_lbl.font_size -= inc
        action = 'Decreased'

    log.prepend_line(f'{action} font size by {inc} to {style_lbl.font_size}')


def get_font_size(event):
    log.prepend_line(f'Font size is {style_lbl.font_size}')


def set_font_size(event):
    try:
        style_lbl.font_size = int(set_size_inp.text)
        log.prepend_line(f'Font size set to {style_lbl.font_size}')
    except ValueError:
        log.prepend_line(f'Invalid value for font size')


def set_font_option(event):
    if event.widget == weight_chk:
        style_lbl.font_weight = 'bold' if weight_chk.checked else 'normal'
    if event.widget == style_chk:
        style_lbl.font_style = 'italic' if style_chk.checked else 'normal'
    if event.widget == underline_chk:
        style_lbl.underline = 'underline' if underline_chk.checked else 'normal'
    if event.widget == strikethrough_chk:
        style_lbl.strikethrough = 'strikethrough' if strikethrough_chk.checked else 'normal'


def change_font_colour(event):
    if event.widget == font_colour_dd:
        style_lbl.colour = font_colour_dd.selected
        log.prepend_line(f'Set font colour to {font_colour_dd.selected}')


def change_bg_colour(event):
    if event.widget == bg_colour_dd:
        style_lbl.background_colour = bg_colour_dd.selected
        log.prepend_line(f'Set font colour to {bg_colour_dd.selected}')


def set_font(event):
    font_name = set_font_name_inp.text
    font_size = int(set_font_size_inp.text)
    options = set_font_options_inp.text
    style_lbl.set_font(font_name, font_size, options)
    log.prepend_line(f'Setting font to {font_name} {font_size} {options}')
    # Update checkboxes
    weight_chk.checked = (style_lbl.font_weight == 'bold')
    style_chk.checked = (style_lbl.font_style == 'italic')
    underline_chk.checked = (style_lbl.underline == 'underline')
    strikethrough_chk.checked = (style_lbl.strikethrough == 'strikethrough')


def get_font_colour(event):
    if event.widget == font_colour_get_btn:
        attribute = 'Font'
        value = style_lbl.colour
    else:
        attribute = 'Background'
        value = style_lbl.background_colour
    log.prepend_line(f"{attribute} colour is '{value}'")


def set_font_colour(event):
    if event.widget == font_colour_set_btn:
        attribute = 'Font'
        value = font_colour_set_inp.text
        style_lbl.colour = value
    else:
        attribute = 'Background'
        value = bg_colour_set_inp.text
        style_lbl.background_colour = value

    log.prepend_line(f"{attribute} colour set to '{value}'")


def reset(event):
    style_lbl.clear_styles()
    for check in (weight_chk, style_chk, underline_chk, strikethrough_chk):
        check.checked = False
    log.prepend_line(f'All styles cleared')


# DEFINE CONTAINERS #

# Main label containers
widget_container = gp.LabelContainer(app, 'StyleLabel widget')
widget_container.height = 200
testing_container = gp.LabelContainer(app, 'Operations')
log_container = gp.LabelContainer(app, 'Log')

# Operations containers
font_options = gp.Container(testing_container)
size_options = gp.Container(testing_container)
font_colour_options = gp.Container(testing_container)
bg_colour_options = gp.Container(testing_container)
font_set = gp.Container(testing_container)

# CREATE WIDGETS

# Test subject
text = choice(['Chocolate', 'The rain in Spain falls mainly on the ground', '1010110110'])
style_lbl = gp.StyleLabel(widget_container, text)
style_lbl.font_size = 30
style_lbl.align = 'center'

# Size options
size_lbl = gp.Label(testing_container, 'Font size')
increase_size_btn = gp.Button(size_options, '+', change_size)
increase_size_btn.width = 4
decrease_size_btn = gp.Button(size_options, '-', change_size)
decrease_size_btn.width = 4
get_size_btn = gp.Button(size_options, 'Get', get_font_size)
set_size_btn = gp.Button(size_options, 'Set', set_font_size)
set_size_inp = gp.Input(size_options)

# Font options
font_options_lbl = gp.Label(testing_container, 'Font options')
weight_chk = gp.Checkbox(font_options, 'Bold')
style_chk = gp.Checkbox(font_options, 'Italic')
underline_chk = gp.Checkbox(font_options, 'Underline')
strikethrough_chk = gp.Checkbox(font_options, 'Strikethrough')

for widget in (weight_chk, style_chk, underline_chk, strikethrough_chk):
    widget.add_event_listener('change', set_font_option)

# Font colour
font_colour_lbl = gp.Label(testing_container, 'Font colour')
font_colour_get_btn = gp.Button(font_colour_options, 'Get', get_font_colour)
font_colour_set_btn = gp.Button(font_colour_options, 'Set', set_font_colour)
font_colour_set_inp = gp.Input(font_colour_options)
font_colour_dd = gp.Dropdown(font_colour_options, colours)
font_colour_dd.add_event_listener('select', change_font_colour)

# Background colour
bg_colour_lbl = gp.Label(testing_container, 'Background colour')
bg_colour_get_btn = gp.Button(bg_colour_options, 'Get', get_font_colour)
bg_colour_set_btn = gp.Button(bg_colour_options, 'Set', set_font_colour)
bg_colour_set_inp = gp.Input(bg_colour_options)
bg_colour_dd = gp.Dropdown(bg_colour_options, colours)
bg_colour_dd.add_event_listener('select', change_bg_colour)

# Set font
set_font_lbl = gp.Label(testing_container, 'Set font')
set_font_name_inp = gp.Input(font_set)
set_font_name_inp.width = 20
set_font_size_inp = gp.Input(font_set)
set_font_size_inp.width = 4
set_font_options_inp = gp.Input(font_set)
set_font_btn = gp.Button(font_set, 'Set font', set_font)

# Clear all
clear_all_lbl = gp.Label(testing_container, 'Reset')
clear_all_btn = gp.Button(testing_container, 'Clear all styles', reset)

# Log
log = gp.Textbox(log_container)
log.height = 10


# ADD ALL WIDGETS #

# StyleLabel
widget_container.set_grid(1, 1)
widget_container.add(style_lbl, 1, 1, align='center', valign='middle', fill=True, stretch=True)

# Size options
size_options.set_grid(1, 5)
size_options.add(increase_size_btn, 1, 1)
size_options.add(decrease_size_btn, 1, 2)
size_options.add(get_size_btn, 1, 3)
size_options.add(set_size_btn, 1, 4)
size_options.add(set_size_inp, 1, 5)

# Font options
font_options.set_grid(4, 1)
font_options.add(weight_chk, 1, 1, margins=('auto', 'auto', 0, 'auto'))
font_options.add(style_chk, 2, 1, margins=(0, 'auto', 0, 'auto'))
font_options.add(underline_chk, 3, 1, margins=(0, 'auto', 0, 'auto'))
font_options.add(strikethrough_chk, 4, 1, margins=(0, 'auto', 'auto', 'auto'))

# Font colour
font_colour_options.set_grid(1, 4)
font_colour_options.add(font_colour_get_btn, 1, 1)
font_colour_options.add(font_colour_set_btn, 1, 2)
font_colour_options.add(font_colour_set_inp, 1, 3)
font_colour_options.add(font_colour_dd, 1, 4)

# Background colour
bg_colour_options.set_grid(1, 4)
bg_colour_options.add(bg_colour_get_btn, 1, 1)
bg_colour_options.add(bg_colour_set_btn, 1, 2)
bg_colour_options.add(bg_colour_set_inp, 1, 3)
bg_colour_options.add(bg_colour_dd, 1, 4)

# Font set
font_set.set_grid(1, 4)
font_set.set_column_weights(0, 0, 1, 0)
font_set.add(set_font_name_inp, 1, 1)
font_set.add(set_font_size_inp, 1, 2)
font_set.add(set_font_options_inp, 1, 3, fill=True)
font_set.add(set_font_btn, 1, 4)

# Testing container
testing_container.set_grid(6, 2)
testing_container.set_column_weights(0, 1)
testing_container.add(size_lbl, 1, 1)
testing_container.add(size_options, 1, 2)
testing_container.add(font_options_lbl, 2, 1)
testing_container.add(font_options, 2, 2)
testing_container.add(font_colour_lbl, 3, 1)
testing_container.add(font_colour_options, 3, 2)
testing_container.add(bg_colour_lbl, 4, 1)
testing_container.add(bg_colour_options, 4, 2)
testing_container.add(set_font_lbl, 5, 1)
testing_container.add(font_set, 5, 2, fill=True)
testing_container.add(clear_all_lbl, 6, 1)
testing_container.add(clear_all_btn, 6, 2)


# Log area
log_container.set_grid(1, 1)
log_container.add(log, 1, 1, fill=True)

# Add everything to main app
app.set_grid(3, 1)
app.set_row_weights(1, 0, 0)
app.add(widget_container, 1, 1, fill=True, stretch=True)
app.add(testing_container, 2, 1, fill=True)
app.add(log_container, 3, 1, fill=True)

# Set some random values
font_colour_dd.selected = choice(font_colour_dd.choices)
bg_colour_dd.selected = choice(bg_colour_dd.choices)
style_lbl.colour = font_colour_dd.selected
style_lbl.background_colour = bg_colour_dd.selected

print(app.fonts())
print(app.font_available('courier'))
app.run()
