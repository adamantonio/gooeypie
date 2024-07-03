import gooeypie as gp
import random

lorem_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum".lower()


def add_text(event):
    text = insert_text_inp.text
    cmd = event.widget.text
    if cmd == 'Append':
        old_textbox.append(text)
        new_textbox.append(text)
    elif cmd == 'Append line':
        old_textbox.append_line(text)
        new_textbox.append_line(text)
    elif cmd == 'Prepend':
        old_textbox.prepend(text)
        new_textbox.prepend(text)
    elif cmd == 'Prepend line':
        old_textbox.prepend_line(text)
        new_textbox.prepend_line(text)
    elif cmd == 'Set contents':
        old_textbox.text = text
        new_textbox.text = text


def get_contents(event):
    # log.prepend_line(repr(old_textbox.text))
    log.prepend_line(repr(new_textbox.text))


def clear(event):
    old_textbox.clear()
    new_textbox.clear()
    log.prepend_line('Textbox cleared')


def make_lorem(event):
    start = random.randrange(len(lorem_text) // 2)
    length = random.randrange(len(lorem_text) // 2)
    insert_text_inp.text = lorem_text #[start:start + length]


def clear_lorem(event):
    insert_text_inp.clear()


def set_visibility(event):
    new_textbox.scrollbar = scrollbar_visibility_dd.selected


def events_testing(event):
    print(event)


def seek(event):
    if event.widget.text == 'To start':
        new_textbox.scroll_to_start()
    else:
        new_textbox.scroll_to_end()


def get_selected(event):
    log.prepend_line(f'Selected text is "{new_textbox.selected}"')



app = gp.GooeyPieApp('Textbox Tests')

test_cont = gp.LabelContainer(app, 'Tests')
old_textbox_cont = gp.LabelContainer(app, 'Old Textbox')
new_textbox_cont = gp.LabelContainer(app, 'NewTextbox')

# Insert text
insert_text_cont = gp.Container(test_cont)

insert_text_inp = gp.Input(insert_text_cont)
insert_text_inp.text = lorem_text
lorem_btn = gp.Button(insert_text_cont, 'Lorem', make_lorem)
clear_insert_text_btn = gp.Button(insert_text_cont, "❌", clear_lorem)

insert_text_cont.set_grid(1, 3)
insert_text_cont.set_column_weights(1, 0, 0)
insert_text_cont.add(insert_text_inp, 1, 1, fill=True)
insert_text_cont.add(lorem_btn, 1, 2)
insert_text_cont.add(clear_insert_text_btn, 1, 3)

# Insert buttons
insert_buttons_cont = gp.Container(test_cont)

append_btn = gp.Button(insert_buttons_cont, 'Append', add_text)
append_line_btn = gp.Button(insert_buttons_cont, 'Append line', add_text)
prepend_btn = gp.Button(insert_buttons_cont, 'Prepend', add_text)
prepend_line_btn = gp.Button(insert_buttons_cont, 'Prepend line', add_text)
set_btn = gp.Button(insert_buttons_cont, 'Set contents', add_text)

insert_buttons_cont.set_grid(1, 5)
insert_buttons_cont.add(append_btn, 1, 1)
insert_buttons_cont.add(append_line_btn, 1, 2)
insert_buttons_cont.add(prepend_btn, 1, 3)
insert_buttons_cont.add(prepend_line_btn, 1, 4)
insert_buttons_cont.add(set_btn, 1, 5)


# Get and clear container
misc_buttons_cont = gp.Container(test_cont)

get_btn = gp.Button(misc_buttons_cont, 'Get contents', get_contents)
get_selected_btn = gp.Button(misc_buttons_cont, 'Get selected', get_selected)
# select_all_btn = gp.Button(misc_buttons_cont, 'Select all', select_all)
clear_btn = gp.Button(misc_buttons_cont, 'Clear', clear)
scroll_start_btn = gp.Button(misc_buttons_cont, 'To start', seek)
scroll_end_btn = gp.Button(misc_buttons_cont, 'To end', seek)

misc_buttons_cont.set_grid(1, 6)
misc_buttons_cont.add(get_btn, 1, 1)
misc_buttons_cont.add(get_selected_btn, 1, 2)
# misc_buttons_cont.add(select_all_btn, 1, 3)
misc_buttons_cont.add(clear_btn, 1, 4)
misc_buttons_cont.add(scroll_start_btn, 1, 5)
misc_buttons_cont.add(scroll_end_btn, 1, 6)

# Log
log = gp.Textbox(test_cont)

# Test container
test_cont.set_grid(4, 1)
test_cont.add(insert_text_cont, 1, 1, fill=True)
test_cont.add(insert_buttons_cont, 2, 1, fill=True)
test_cont.add(misc_buttons_cont, 3, 1)
test_cont.add(log, 4, 1, fill=True)

# Old textbox
old_textbox = gp.Textbox(old_textbox_cont)
old_textbox_cont.set_grid(1, 1)
old_textbox_cont.add(old_textbox, 1, 1, fill=True, stretch=True)

# New textbox
new_textbox = gp.NewTextbox(new_textbox_cont)

standard_events = ['mouse_down', 'mouse_up', 'double_click', 'triple_click',
                   'middle_click', 'right_click', 'mouse_over', 'mouse_out',
                   'focus', 'blur', 'key_press']

for event_name in standard_events:
    new_textbox.add_event_listener(event_name, events_testing)

new_textbox.add_event_listener('change', events_testing)

scrollbar_visibility_dd = gp.Dropdown(new_textbox_cont, ['auto', 'visible', 'hidden'])
scrollbar_visibility_dd.selected_index = 0
scrollbar_visibility_dd.add_event_listener('select', set_visibility)

new_textbox_cont.set_grid(2, 1)
new_textbox_cont.set_row_weights(1, 0)
new_textbox_cont.add(new_textbox, 1,1, fill=True, stretch=True)
new_textbox_cont.add(scrollbar_visibility_dd, 2, 1, fill=True)

# Main app
app.set_grid(1, 3)
app.set_column_weights(0, 1, 1)
app.add(test_cont, 1, 1)
app.add(old_textbox_cont, 1, 2, fill=True, stretch=True)
app.add(new_textbox_cont, 1, 3, fill=True, stretch=True)

app.run()
