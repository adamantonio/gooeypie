import gooeypie as gp
from random import randint

app = gp.GooeyPieApp('Listbox Tests')


def display_items(event):
    """Test for items getter"""
    items = listbox.items
    print(items)
    print(len(items))
    output.prepend(f'{items}\n')


def add_items(event):
    """Testing for items setter"""
    random_numbers = [randint(1, 100) for _ in range(100)]
    listbox.items = random_numbers


def add_item(event):
    """Testing for add_item """
    listbox.add_item(add_what.text)


def add_item_to_start(event):
    """Testing for add_item """
    listbox.add_item_to_start(add_start_what.text)


def remove_item(event):
    """Testing for add_item """
    output.prepend(f'Deleted {listbox.remove_item(int(remove_where.text))}')


def set_multiple(event):
    listbox.multiple_selection = multiple.checked


def get_selected(event):
    output.prepend(f'Selected item: {listbox.selected}\n')


def get_selected_index(event):
    output.prepend(f'Selected index: {listbox.selected_index}\n')


def select_at(event):
    listbox.selected_index = int(select_where.text)


def select(event):
    if event.widget == select_all:
        listbox.select_all()
    if event.widget == select_none:
        listbox.select_none()


def remove_selected(event):
    listbox.remove_selected()


# Listbox Container
listbox_container = gp.LabelContainer(app, 'Listbox')
listbox = gp.Listbox(listbox_container)
multiple = gp.Checkbox(listbox_container, 'Allow multiple selection')
multiple.add_event_listener('change', set_multiple)
listbox.height = 10
listbox_container.set_grid(2, 1)
listbox_container.set_row_weights(1, 0)
listbox_container.add(listbox, 1, 1, fill=True, stretch=True)
listbox_container.add(multiple, 2, 1)

# Testing operations Container
test_container = gp.LabelContainer(app, 'Tests')
setter_button = gp.Button(test_container, 'Set some random values', add_items)
items_button = gp.Button(test_container, 'Get Items', display_items)
add_button = gp.Button(test_container, 'Add Item', add_item)
add_what = gp.Input(test_container)
add_start_button = gp.Button(test_container, 'Add Item to start', add_item_to_start)
add_start_what = gp.Input(test_container)
remove_button = gp.Button(test_container, 'Delete item at index', remove_item)
remove_where = gp.Input(test_container)
selected_button = gp.Button(test_container, 'Get selected value(s)', get_selected)
selected_index_button = gp.Button(test_container, 'Get selected index(es)', get_selected_index)
select_button = gp.Button(test_container, 'Select at index(es)', select_at)
select_where = gp.Input(test_container)
select_all = gp.Button(test_container, 'Select all', select)
select_none = gp.Button(test_container, 'Select none', select)
remove_selection = gp.Button(test_container, 'Remove selected', remove_selected)

test_container.set_grid(8, 2)
test_container.set_column_weights(1, 1)
test_container.add(setter_button, 1, 1, fill=True)
test_container.add(items_button, 1, 2, fill=True)
test_container.add(add_button, 2, 1, fill=True)
test_container.add(add_what, 2, 2, valign="middle", fill=True)
test_container.add(add_start_button, 3, 1, fill=True)
test_container.add(add_start_what, 3, 2, valign="middle", fill=True)
test_container.add(remove_button, 4, 1, fill=True)
test_container.add(remove_where, 4, 2, valign="middle", fill=True)
test_container.add(selected_button, 5, 1, fill=True)
test_container.add(selected_index_button, 5, 2, fill=True)
test_container.add(select_button, 6, 1, fill=True)
test_container.add(select_where, 6, 2, fill=True)
test_container.add(select_all, 7, 1, fill=True)
test_container.add(select_none, 7, 2, fill=True)
test_container.add(remove_selection, 8, 1, fill=True)

# Output container
output_container = gp.LabelContainer(app, 'Output')
output = gp.Textbox(output_container)
output.height = 10
output_container.set_grid(1, 1)
output_container.add(output, 1, 1, fill=True, stretch=True)


# Add containers to main window and run
app.set_grid(2, 2)
app.set_column_weights(0, 1)
app.set_row_weights(1, 1)
app.add(listbox_container, 1, 1, stretch=True)
app.add(test_container, 1, 2, fill=True, stretch=True)
app.add(output_container, 2, 1, column_span=2, fill=True, stretch=True)
app.run()
