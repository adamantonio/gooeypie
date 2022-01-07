import gooeypie as gp

table_data = [{"first_name": "Yanaton", "last_name": "Turfes", "salary": 45408},
              {"first_name": "Nariko", "last_name": "Bloomfield", "salary": 498901},
              {"first_name": "Benyamin", "last_name": "Bulcroft", "salary": 476620},
              {"first_name": "Karmen", "last_name": "O'Kinneally", "salary": 298223},
              {"first_name": "Jerrie", "last_name": "Evers", "salary": 367555},
              {"first_name": "Hobie", "last_name": "Dash", "salary": 76322},
              {"first_name": "Barrett", "last_name": "Gowdy", "salary": 274401},
              {"first_name": "Tiffy", "last_name": "Essam", "salary": 227178},
              {"first_name": "Drusilla", "last_name": "Morrell", "salary": 512075},
              {"first_name": "Britt", "last_name": "Leel", "salary": 523298},
              {"first_name": "Leonora", "last_name": "MacCague", "salary": 488409},
              {"first_name": "Lilia", "last_name": "Mincini", "salary": 278163},
              {"first_name": "Grove", "last_name": "Earry", "salary": 400094},
              {"first_name": "Arley", "last_name": "Stoodley", "salary": 395060},
              {"first_name": "Karla", "last_name": "Pietersma", "salary": 85161},
              {"first_name": "Nicoline", "last_name": "Balshen", "salary": 473130},
              {"first_name": "Morgan", "last_name": "Avramovich", "salary": 212032},
              {"first_name": "Meridel", "last_name": "Byllam", "salary": 349533},
              {"first_name": "Koo", "last_name": "Hold", "salary": 595940},
              {"first_name": "Engracia", "last_name": "Langmaid", "salary": 213586}]

table_backup = table_data.copy()


def add_row(event):
    if len(table_data):
        row = list(table_data.pop().values())
        if event:
            output = f"Added {row}"
            if event.widget == add_btn:
                table.add_row(row)
            elif event.widget == add_to_top_btn:
                table.add_row_to_top(row)
                output += ' to start'
            else:
                index = int(add_at_inp.text)
                table.add_row_at(index, row)
                output += f' to index {index}'
            log.prepend_line(output)
        else:
            table.add_row(row)
    else:
        add_btn.disabled = True
        add_to_top_btn.disabled = True
        add_at_inp.disabled = True


def clear_table(event):
    table.clear()
    global table_data
    table_data = table_backup.copy()
    add_btn.disabled = False
    add_to_top_btn.disabled = False
    log.prepend_line('Cleared table')


def remove_selected(event):
    row = table.remove_selected()
    log.prepend_line(f'Removed {row}')


def select(event):
    selected = table.selected
    if selected is None:
        log.prepend_line(f'Selected {table.selected}')
    else:
        if table.multiple_selection:
            output = ''
            for row in selected:
                output = '\n    ' + str(row) + output
            log.prepend_line(f'Selected {len(selected)} item(s): {output}')
        else:
            log.prepend_line(f'Selected {table.selected}')


def double_clicked(event):
    log.prepend_line(f'Double clicked {table.selected}')


def toggle_multiple(event):
    table.multiple_selection = multiple_selection.checked
    log.prepend_line(f'Multiple selection set to {table.multiple_selection}')


def select_row(event):
    table.select_row(int(select_row_inp.text))


def select_none(event):
    table.select_none()


def select_all(event):
    table.select_all()


def remove_row(event):
    removed = table.remove_row(int(remove_row_inp.text))
    log.prepend_line(f'Removed {removed}')

def clear_log(event):
    log.clear()


def get_row(event):
    index = int(get_row_inp.text)
    row_data = table.data[index]
    log.prepend_line(f'Row {index} is {row_data}')


def print_all_data(event):
    from pprint import pprint
    data = table.data
    print(f'{len(data)} item(s)')
    pprint(data)
    log.prepend_line('Printed all data to console')


def set_data(event):
    data = [['Engracia', 'Langmaid', 213586],
        ['Koo', 'Hold', 595940],
        ['Meridel', 'Byllam', 34533],
        ['Morgan', 'Avramovich', 21202],
        ['Nicoline', 'Balshen']]

    table.data = data


def disable(event):
    table.disabled = not table.disabled
    log.prepend_line(f'Table is {"disabled" if table.disabled else "enabled"}')


app = gp.GooeyPieApp('Table testing')

widget_cont = gp.LabelContainer(app, 'Table widget')
operations_cont = gp.LabelContainer(app, 'Operations')
operations_add = gp.Container(operations_cont)
operations_remove = gp.Container(operations_cont)
operations_select = gp.Container(operations_cont)
operations_get = gp.Container(operations_cont)
log_cont = gp.LabelContainer(app, 'Log')

table = gp.Table(widget_cont, ['First name', 'Last name', 'Salary'])
table.set_column_widths(150, 150, 100)
table.height = 5
table.set_column_alignment(2, 'center')

for _ in range(5):
    add_row(None)
multiple_selection = gp.Checkbox(widget_cont, 'Multiple selection')
multiple_selection.add_event_listener('change', toggle_multiple)
disable_chk = gp.Checkbox(widget_cont, 'Disable table')
disable_chk.add_event_listener('change', disable)

# Add operations
set_all_btn = gp.Button(operations_add, 'Set data', set_data)
add_btn = gp.Button(operations_add, 'Add row', add_row)
add_to_top_btn = gp.Button(operations_add, 'Add row to top', add_row)
add_row_at_btn = gp.Button(operations_add, 'Add row at', add_row)
add_at_inp = gp.Input(operations_add)
add_at_inp.text = 2
add_at_inp.width = 4

operations_add.set_grid(1, 5)
operations_add.add(set_all_btn, 1, 1)
operations_add.add(add_btn, 1, 2)
operations_add.add(add_to_top_btn, 1, 3)
operations_add.add(add_row_at_btn, 1, 4)
operations_add.add(add_at_inp, 1, 5, valign='middle')

# Remove operations
remove_all_btn = gp.Button(operations_remove, 'Clear table', clear_table)
remove_selected_btn = gp.Button(operations_remove, 'Remove selected', remove_selected)
remove_row_btn = gp.Button(operations_remove, 'Remove row:', remove_row)
remove_row_inp = gp.Input(operations_remove)
remove_row_inp.text = 1
remove_row_inp.width = 5

operations_remove.set_grid(1, 4)
operations_remove.add(remove_all_btn, 1, 1)
operations_remove.add(remove_selected_btn, 1, 2)
operations_remove.add(remove_row_btn, 1, 3)
operations_remove.add(remove_row_inp, 1, 4, valign='middle')

# Select operations
select_all_btn = gp.Button(operations_select, 'Select all', select_all)
select_none_btn = gp.Button(operations_select, 'Select none', select_none)
select_row_btn = gp.Button(operations_select, 'Select row:', select_row)
select_row_inp = gp.Input(operations_select)
select_row_inp.text = 1
select_row_inp.width = 5

operations_select.set_grid(1, 4)
operations_select.add(select_all_btn, 1, 1)
operations_select.add(select_none_btn, 1, 2)
operations_select.add(select_row_btn, 1, 3)
operations_select.add(select_row_inp, 1, 4, valign='middle')

# Get operations
get_selected_btn = gp.Button(operations_get, 'Get selected', select)
get_row_btn = gp.Button(operations_get, 'Get row:', get_row)
get_row_inp = gp.Input(operations_get)
get_all_btn = gp.Button(operations_get, 'Print all', print_all_data)
get_row_inp.text = 1
get_row_inp.width = 5

operations_get.set_grid(1, 4)
operations_get.add(get_selected_btn, 1, 1)
operations_get.add(get_row_btn, 1, 2)
operations_get.add(get_row_inp, 1, 3, valign='middle')
operations_get.add(get_all_btn, 1, 4)


# Add all operations
operations_cont.set_grid(4, 1)
operations_cont.add(operations_add, 1, 1)
operations_cont.add(operations_remove, 2, 1)
operations_cont.add(operations_select, 3, 1)
operations_cont.add(operations_get, 4, 1)


# Log container
log = gp.Textbox(log_cont)
log.height = 10
clear_log_btn = gp.Button(log_cont, 'Clear', clear_log)

log_cont.set_grid(2, 1)
log_cont.set_row_weights(1, 0)
log_cont.add(log, 1, 1, fill=True, stretch=True)
log_cont.add(clear_log_btn, 2, 1)


# Table container
widget_cont.set_grid(2, 2)
widget_cont.set_column_weights(0, 1)
widget_cont.add(table, 1, 1, fill=True, stretch=True, column_span=2)
widget_cont.add(multiple_selection, 2, 1)
widget_cont.add(disable_chk, 2, 2)

# Add all to main app
app.set_grid(3, 1)
app.set_row_weights(0, 0, 1)
app.add(widget_cont, 1, 1, stretch=True, fill=True)
app.add(operations_cont, 2, 1, fill=True)
app.add(log_cont, 3, 1, fill=True, stretch=True)


table.add_event_listener('select', select)
table.add_event_listener('double_click', double_clicked)

app.run()
