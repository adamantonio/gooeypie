import gooeypie as gp
from random import randint

NUM_RANDOM_ITEMS = 15

app = gp.GooeyPieApp('Listbox Tests')


def display_items(event):
    """Test for items getter"""
    items = listbox.items
    output.prepend(f'Regular: {len(items)} items: {items}\n')
    items = scroll_listbox.items
    output.prepend(f'Scrolled: {len(items)} items: {items}\n')


def add_items(event):
    """Testing for items setter"""
    random_numbers = [randint(1, 100) for _ in range(NUM_RANDOM_ITEMS)]
    random_numbers = [n + 1 for n in range(NUM_RANDOM_ITEMS)]
    listbox.items = random_numbers
    scroll_listbox.items = random_numbers
    output.prepend(f'Set listbox to {NUM_RANDOM_ITEMS} random numbers\n')


def add_item(event):
    """Testing for add_item """
    listbox.add_item(add_what.text)
    scroll_listbox.add_item(add_what.text)
    output.prepend(f'Added {add_what.text} to end\n')


def add_item_to_start(event):
    """Testing for add_item """
    listbox.add_item_to_start(add_start_what.text)
    scroll_listbox.add_item_to_start(add_start_what.text)
    output.prepend(f'Added {add_start_what.text} to start\n')


def remove_item(event):
    """Testing for remove_item"""
    output.prepend(f'Removed {scroll_listbox.remove_item(int(remove_where.text))} and {listbox.remove_item(int(remove_where.text))}\n')


def set_multiple(event):
    """Change the listbox to allow multiple selection"""
    listbox.multiple_selection = multiple.checked
    scroll_listbox.multiple_selection = multiple.checked
    output.prepend(f'Set multiple selection to {multiple.checked}\n')


def get_selected(event):
    output.prepend(f'Selected item(s): {scroll_listbox.selected} and {listbox.selected}\n')


def get_selected_index(event):
    output.prepend(f'Selected index: {scroll_listbox.selected_index} and {listbox.selected_index}\n')


def remove_selected(event):
    output.prepend(f'Removed item(s): {scroll_listbox.remove_selected()} and {listbox.remove_selected()}\n')


def select_at(event):
    listbox.selected_index = int(select_where.text)
    scroll_listbox.selected_index = int(select_where.text)
    output.prepend(f'Selected item at {select_where.text}\n')


def select(event):
    if event.widget == select_all:
        listbox.select_all()
        scroll_listbox.select_all()
    if event.widget == select_none:
        listbox.select_none()
        scroll_listbox.select_none()


def set_scrollbar(event):
    """Changes the visibility setting of the scrollbar"""
    scroll_listbox.scrollbar = scrollbar_option.selected
    output.prepend(f'Changed scrollbar to {scrollbar_option.selected}\n')


def select_event(event):
    output.prepend(f'{scroll_listbox.selected} selected on scroll listbox, {listbox.selected} selected on listbox\n')


def enable_disable_listboxes(event):
    listbox.disabled = not listbox.disabled
    scroll_listbox.disabled = not scroll_listbox.disabled
    state = 'Disabling' if listbox.disabled else 'Enabling'
    output.prepend(f'{state} listboxes\n')

def clear(event):
    listbox.clear()
    scroll_listbox.clear()


# Listbox Container
listbox_container = gp.LabelContainer(app, 'Simple Listbox')
listbox = gp.SimpleListbox(listbox_container)
listbox.width = 30
multiple = gp.Checkbox(listbox_container, 'Allow multiple selection')
multiple.add_event_listener('change', set_multiple)
listbox_container.set_grid(2, 1)
listbox_container.set_row_weights(1, 0)
listbox_container.add(listbox, 1, 1, fill=True, stretch=True)
listbox_container.add(multiple, 2, 1)

# Scrolled listbox container
scrolled_listbox_container = gp.LabelContainer(app, 'Scrolling')
scroll_listbox = gp.Listbox(scrolled_listbox_container)
scroll_listbox.add_event_listener('select', select_event)
scroll_listbox.width = 30
scrollbar_option = gp.Dropdown(scrolled_listbox_container, ['auto', 'visible', 'hidden'])
scrollbar_option.selected_index = 0
scrollbar_option.add_event_listener('select', set_scrollbar)
scrolled_listbox_container.set_grid(2, 1)
scrolled_listbox_container.set_row_weights(1, 0)
scrolled_listbox_container.add(scroll_listbox, 1, 1, fill=True, stretch=True)
scrolled_listbox_container.add(scrollbar_option, 2, 1)

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
disable = gp.Button(test_container, 'Enable/disable listboxes', enable_disable_listboxes)
clear = gp.Button(test_container, 'Clear all', clear)

test_container.set_grid(9, 2)
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
test_container.add(disable, 8, 2, fill=True)
test_container.add(clear, 9, 1, fill=True)

# Output container
output_container = gp.LabelContainer(app, 'Output')
output = gp.Textbox(output_container)
output.height = 10
output_container.set_grid(1, 1)
output_container.add(output, 1, 1, fill=True, stretch=True)

# Add containers to main window and run
app.set_grid(2, 3)
app.set_column_weights(1, 1, 1)
app.set_row_weights(1, 0)
app.add(scrolled_listbox_container, 1, 1, stretch=True, fill=True)
app.add(listbox_container, 1, 2, stretch=True, fill=True)
app.add(test_container, 1, 3, fill=True)
app.add(output_container, 2, 1, column_span=3, fill=True, stretch=True)
app.run()
