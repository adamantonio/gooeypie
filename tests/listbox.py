import gooeypie as gp
from random import randint

NUM_RANDOM_ITEMS = 15

app = gp.GooeyPieApp('New Listbox Tests')


def display_items(event):
    """Test for items getter"""
    items = listbox.items
    output.prepend(f'{len(items)} items: {items}\n')


def add_items(event):
    """Testing for items setter"""
    random_numbers = [randint(1, 100) for _ in range(NUM_RANDOM_ITEMS)]
    random_numbers = [n + 1 for n in range(NUM_RANDOM_ITEMS)]
    listbox.items = random_numbers
    output.prepend(f'Set listbox to {NUM_RANDOM_ITEMS} random numbers\n')


def add_item(event):
    """Testing for add_item """
    listbox.add_item(add_what.text)
    output.prepend(f'Added {add_what.text} to end\n')


def add_item_to_start(event):
    """Testing for add_item """
    listbox.add_item_to_start(add_start_what.text)
    output.prepend(f'Added {add_start_what.text} to start\n')


def add_item_to_index(event):
    """Testing for add_item_at"""
    item = str(randint(50, 100))
    listbox.add_item_at(int(add_where_index.text), item)
    output.prepend(f'Added {item} to index {int(add_where_index.text)}\n')


def remove_item(event):
    """Testing for remove_item"""
    output.prepend(f'Removed {listbox.remove_item(int(remove_where.text))}\n')


def set_multiple(event):
    """Change the listbox to allow multiple selection"""
    listbox.multiple_selection = multiple.checked
    output.prepend(f'Set multiple selection to {multiple.checked}\n')


def get_selected(event):
    output.prepend(f'Selected item(s): {listbox.selected}\n')


def get_selected_index(event):
    output.prepend(f'Selected index: {listbox.selected_index}\n')


def remove_selected(event):
    output.prepend(f'Removed item(s): {listbox.remove_selected()}\n')


def select_at(event):
    if ',' in select_where.text:
        # Multiple indexes specified
        indexes = [int(index.strip()) for index in select_where.text.split(',')]
        for index in indexes:
            listbox.selected_index = index
    else:
        # Single index specified
        listbox.selected_index = int(select_where.text)

    output.prepend(f'Selected item at index(es) {select_where.text}\n')


def select(event):
    if event.widget == select_all:
        listbox.select_all()
    if event.widget == select_none:
        listbox.select_none()


def set_scrollbar(event):
    """Changes the visibility setting of the scrollbar"""
    listbox.scrollbar = scrollbar_option.selected
    output.prepend(f'Changed scrollbar to {scrollbar_option.selected}\n')


def select_event(event):
    output.prepend(f"'{listbox.selected}' selected on listbox\n")


def enable_disable_listboxes(event):
    listbox.disabled = not listbox.disabled
    state = 'Disabled' if listbox.disabled else 'Enabled'
    output.prepend(f'{state} listbox\n')


def set_selected(event):
    listbox.selected = randint(100, 200)


def clear(event):
    listbox.clear()


def event_test(event):
    output.prepend_line(f'Select event triggered item(s): {listbox.selected}')


# Listbox Container
listbox_container = gp.LabelContainer(app, 'New Listbox')
listbox = gp.Listbox(listbox_container)
listbox.width = 200
multiple = gp.Checkbox(listbox_container, 'Allow multiple selection')
multiple.add_event_listener('change', set_multiple)
scrollbar_option = gp.Dropdown(listbox_container, ['auto', 'visible', 'hidden'])
scrollbar_option.add_event_listener('select', set_scrollbar)

listbox_container.set_grid(3, 1)
listbox_container.set_row_weights(1, 0, 0)
listbox_container.add(listbox, 1, 1, fill=True, stretch=True)
listbox_container.add(multiple, 2, 1)
listbox_container.add(scrollbar_option, 3, 1)

listbox.add_event_listener('select', event_test)

# Testing operations Container
test_container = gp.LabelContainer(app, 'Tests')
setter_button = gp.Button(test_container, 'Set some random values', add_items)
items_button = gp.Button(test_container, 'Get Items', display_items)
add_button = gp.Button(test_container, 'Add Item', add_item)
add_what = gp.Input(test_container)
add_start_button = gp.Button(test_container, 'Add Item to start', add_item_to_start)
add_start_what = gp.Input(test_container)
add_where_button = gp.Button(test_container, 'Add random item to index', add_item_to_index)
add_where_index = gp.Input(test_container)
remove_button = gp.Button(test_container, 'Delete item at index', remove_item)
remove_where = gp.Input(test_container)
selected_button = gp.Button(test_container, 'Get selected value(s)', get_selected)
selected_index_button = gp.Button(test_container, 'Get selected index(es)', get_selected_index)
select_button = gp.Button(test_container, 'Select at index(es)', select_at)
select_where = gp.Input(test_container)
select_all = gp.Button(test_container, 'Select all', select)
select_none = gp.Button(test_container, 'Select none', select)
remove_selection = gp.Button(test_container, 'Remove selected', remove_selected)
disable = gp.Button(test_container, 'Enable/disable listboxes', enable_disable_listboxes)
set_select = gp.Button(test_container, 'Set selected to random', set_selected)
clear = gp.Button(test_container, 'Clear all', clear)

test_container.set_grid(10, 2)
test_container.set_column_weights(1, 1)
test_container.add(setter_button, 1, 1, fill=True)
test_container.add(items_button, 1, 2, fill=True)
test_container.add(add_button, 2, 1, fill=True)
test_container.add(add_what, 2, 2, valign="middle", fill=True)
test_container.add(add_start_button, 3, 1, fill=True)
test_container.add(add_start_what, 3, 2, valign="middle", fill=True)
test_container.add(add_where_button, 4, 1, fill=True)
test_container.add(add_where_index, 4, 2, valign="middle", fill=True)
test_container.add(remove_button, 5, 1, fill=True)
test_container.add(remove_where, 5, 2, valign="middle", fill=True)
test_container.add(selected_button, 6, 1, fill=True)
test_container.add(selected_index_button, 6, 2, fill=True)
test_container.add(select_button, 7, 1, fill=True)
test_container.add(select_where, 7, 2, fill=True)
test_container.add(select_all, 8, 1, fill=True)
test_container.add(select_none, 8, 2, fill=True)
test_container.add(remove_selection, 9, 1, fill=True)
test_container.add(disable, 9, 2, fill=True)
test_container.add(set_select, 10, 1, fill=True)
test_container.add(clear, 10, 2, fill=True)

# Output container
output_container = gp.LabelContainer(app, 'Output')
output = gp.Textbox(output_container)
output.height = 10
output_container.set_grid(1, 1)
output_container.add(output, 1, 1, fill=True, stretch=True)

# Add containers to main window and run
app.set_grid(2, 2)
app.set_column_weights(1, 0)
app.set_row_weights(1, 0)
app.add(listbox_container, 1, 1, stretch=True, fill=True)
app.add(test_container, 1, 2, fill=True)
app.add(output_container, 2, 1, column_span=2, fill=True, stretch=True)
app.run()
