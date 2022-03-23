import gooeypie as gp


def press(event):
    log.append(f'{dropdown.selected}\n')
    dropdown.deselect()


def selected(event):
    log.prepend(f'Selected item is {dropdown.selected}\n')


def selected_index(event):
    log.prepend(f'Selected index is {dropdown.selected_index}\n')


def get_items(event):
    log.prepend_line(f'Items are {dropdown.items}')


def deselect(event):
    log.prepend_line(f'Deselected')
    dropdown.deselect()


def change_items(event):
    dropdown.items = ('Red', 'Green', 'Blue')
    log.prepend_line(f'Changed items')


def set_item(event):
    log.prepend_line(f'Set selected to {set_item_input.text}')
    dropdown.selected = set_item_input.text


def set_index(event):
    log.prepend_line(f'Set selected to {set_index_input.text}')
    dropdown.selected_index = int(set_index_input.text)


app = gp.GooeyPieApp('Dropdowns')
app.width = 300

actions = gp.LabelContainer(app, 'Actions')
set_actions = gp.Container(actions)

dropdown = gp.Dropdown(app, ['First', 'Second', 'Third'])
log = gp.Textbox(app)
log.height = 10

selected_button = gp.Button(actions, 'Selected', selected)
selected_index_button = gp.Button(actions, 'Selected Index', selected_index)
get_items_button = gp.Button(actions, 'Get items', get_items)

set_item_button = gp.Button(set_actions, 'Set item', set_item)
set_item_input = gp.Input(set_actions)
set_index_button = gp.Button(set_actions, 'Set index', set_index)
set_index_input = gp.Input(set_actions)

deselect_button = gp.Button(actions, 'Deselect', deselect)
change_button = gp.Button(actions, 'Change items to colours', change_items)

set_actions.set_grid(2, 2)
set_actions.set_column_weights(1, 1)
set_actions.add(set_item_button, 1, 1, fill=True)
set_actions.add(set_item_input, 1, 2, fill=True)
set_actions.add(set_index_button, 2, 1, fill=True)
set_actions.add(set_index_input, 2, 2, fill=True)

actions.set_grid(6, 1)
actions.add(selected_button, 1, 1, fill=True)
actions.add(selected_index_button, 2, 1, fill=True)
actions.add(get_items_button, 3, 1, fill=True)
actions.add(set_actions, 4, 1, fill=True)
actions.add(deselect_button, 5, 1, fill=True)
actions.add(change_button, 6, 1, fill=True)

app.set_grid(3, 1)
app.set_row_weights(0, 0, 1)
app.add(dropdown, 1, 1, fill=True)
app.add(actions, 2, 1, fill=True)
app.add(log, 3, 1, fill=True, stretch=True)

app.run()
