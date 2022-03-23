import gooeypie as gp
from random import choice

app = gp.GooeyPieApp('Label widget')
align_options = ['left', 'center', 'right']
label_text = ['A short label',
              'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut ' \
              'labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco ' \
              'laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in ' \
              'voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
              '123456789 ' * 40]


def change_label(event):
    if contents_rdo.selected == 'Short':
        test_lbl.text = label_text[0]
    if contents_rdo.selected == 'Long':
        test_lbl.text = label_text[1]


def align(event):
    test_lbl.align = align_rdo.selected


def justify(event):
    test_lbl.justify = justify_rdo.selected


def add_words(event):
    test_lbl.wrap = not test_lbl.wrap


# DEFINE CONTAINERS #

# Main label containers
widget_container = gp.LabelContainer(app, 'Label widget')
testing_container = gp.LabelContainer(app, 'Operations')
log_container = gp.LabelContainer(app, 'Log')

# Operations containers
content_container = gp.Container(testing_container)
length_container = gp.Container(testing_container)
min_length_container = gp.Container(testing_container)

# CREATE WIDGETS

# Test subject
test_lbl = gp.Label(widget_container, choice(label_text))
# test_lbl.width = 180
test_lbl.wrap = True

# Label contents
contents_rdo = gp.Radiogroup(content_container, ['Short', "Long"], 'horizontal')
contents_rdo.add_event_listener('change', change_label)
other_lbl = gp.Label(content_container, 'Other')
other_inp = gp.Input(content_container)
more_words_btn = gp.Button(content_container, 'Add words', add_words)

# Length
length_lbl = gp.Label(testing_container, 'Wrap length')
length_inp = gp.Input(length_container)
length_set_btn = gp.Button(length_container, 'Set', None)
length_up_btn = gp.Button(length_container, '+', None)
length_down_btn = gp.Button(length_container, '-', None)

# Minimum length
min_length_lbl = gp.Label(testing_container, 'Minimum length')
min_length_inp = gp.Input(min_length_container)
min_length_set_btn = gp.Button(min_length_container, 'Set', None)
min_length_up_btn = gp.Button(min_length_container, '+', None)
min_length_down_btn = gp.Button(min_length_container, '-', None)

# Align
align_lbl = gp.Label(testing_container, 'Align')
align_rdo = gp.Radiogroup(testing_container, align_options, 'horizontal')
align_rdo.add_event_listener('change', align)

# Justify
justify_lbl = gp.Label(testing_container, 'Justify')
justify_rdo = gp.Radiogroup(testing_container, align_options, 'horizontal')
justify_rdo.add_event_listener('change', justify)

# Log
log = gp.Textbox(log_container)
log.height = 10


# ADD ALL WIDGETS #

# Test subject
widget_container.set_grid(1, 1)
widget_container.add(test_lbl, 1, 1, fill=True, stretch=True)

# Content options
content_container.set_grid(1, 4)
content_container.add(contents_rdo, 1, 1)
content_container.add(other_lbl, 1, 2)
content_container.add(other_inp, 1, 3)
content_container.add(more_words_btn, 1, 4)

# Wrap length
length_container.set_grid(1, 4)
length_container.add(length_inp, 1, 1)
length_container.add(length_set_btn, 1, 2)
length_container.add(length_up_btn, 1, 3)
length_container.add(length_down_btn, 1, 4)

# Minimum length
min_length_container.set_grid(1, 4)
min_length_container.add(min_length_inp, 1, 1)
min_length_container.add(min_length_set_btn, 1, 2)
min_length_container.add(min_length_up_btn, 1, 3)
min_length_container.add(min_length_down_btn, 1, 4)

# Testing container
testing_container.set_grid(5, 2)
testing_container.set_column_weights(0, 1)
testing_container.add(content_container, 1, 1, column_span=2)
testing_container.add(length_lbl, 2, 1)
testing_container.add(length_container, 2, 2)
testing_container.add(min_length_lbl, 3, 1)
testing_container.add(min_length_container, 3, 2)
testing_container.add(align_lbl, 4, 1)
testing_container.add(align_rdo, 4, 2)
testing_container.add(justify_lbl, 5, 1)
testing_container.add(justify_rdo, 5, 2)

# Log area
log_container.set_grid(1, 1)
log_container.add(log, 1, 1, fill=True)

# Add everything to main app
app.set_grid(3, 1)
app.set_row_weights(1, 0, 0)
app.add(widget_container, 1, 1, fill=True, stretch=True)
app.add(testing_container, 2, 1, fill=True)
app.add(log_container, 3, 1, fill=True)

print(f'{test_lbl.width=}')
app.run()


