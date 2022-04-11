import gooeypie as gp

sizes = ['Small', 'Medium', 'Large']
colours = ['Red', 'Blue', 'Green', 'Pink', 'Goldenrod', 'Purple', 'Crimson']
chrises = ['Pratt', 'Hemsworth', 'Pine', 'Evans']
dogs = ['Poodle', 'Cavalier', 'Beagle', 'Rottweiler', 'Jack Russell']


def selected(event):
    radios = eval(f'{target_dd.selected}_rdo')
    log.prepend_line(f'Selected {target_dd.selected[:-1]} is "{radios.selected}" at index {radios.selected_index}')


def set_selected(event):
    radios = eval(f'{target_dd.selected}_rdo')
    try:
        if event.widget == selected_item_btn:
            radios.selected = selected_inp.text
            log.prepend_line(f'Set selected item to {selected_inp.text}')
        else:
            radios.selected_index = int(selected_inp.text)
            log.prepend_line(f'Set selected index to {selected_inp.text}')
    except ValueError as err:
        log.prepend_line(f'Error: {err}')


def deselect(event):
    radios = eval(f'{target_dd.selected}_rdo')
    radios.deselect()


def enable_disable(event):
    radios = eval(f'{target_dd.selected}_rdo')
    if event.widget == disable_btn:
        radios.disabled = True
        log.prepend_line(f'Disabled {target_dd.selected}')
    else:
        radios.disabled = False
        log.prepend_line(f'Enabled {target_dd.selected}')


def item_state(event):
    radios = eval(f'{target_dd.selected}_rdo')
    try:
        if event.widget.text == 'Disable item':
            radios.disable_item(state_inp.text)
            log.prepend_line(f"Disabled item '{state_inp.text}' in {target_dd.selected}")
        else:
            radios.enable_item(state_inp.text)
            log.prepend_line(f"Enabled item '{state_inp.text}' in {target_dd.selected}")
    except ValueError as err:
        log.prepend_line(f'Error: {err}')


def index_state(event):
    radios = eval(f'{target_dd.selected}_rdo')
    try:
        if event.widget.text == 'Disable index':
            radios.disable_index(int(state_inp.text))
            log.prepend_line(f"Disabled index {state_inp.text} in {target_dd.selected}")
        else:
            radios.enable_index(int(state_inp.text))
            log.prepend_line(f"Enabled index {state_inp.text} in {target_dd.selected}")
    except ValueError as err:
        log.prepend_line(f'Error: {err}')


app = gp.GooeyPieApp('Radio testing')
widget_cont = gp.LabelContainer(app, 'Radiogroup testing widgets')
tests_cont = gp.LabelContainer(app, 'Tests')

list_cont = gp.Container(tests_cont)
selected_cont = gp.Container(tests_cont)
state_cont = gp.Container(tests_cont)

log_cont = gp.LabelContainer(app, 'Log')

sizes_rdo = gp.LabelRadiogroup(widget_cont, 'Sizes', sizes)
colours_rdo = gp.Radiogroup(widget_cont, colours)
chriss_rdo = gp.LabelRadiogroup(widget_cont, 'Chrises', chrises, 'horizontal')
dogs_rdo = gp.Radiogroup(widget_cont, dogs, 'horizontal')

target_dd = gp.Dropdown(list_cont, ['sizes', 'colours', 'chriss', 'dogs'])
target_dd.selected_index = 0
selected_btn = gp.Button(list_cont, 'Get selected', selected)
disable_btn = gp.Button(list_cont, 'Disable', enable_disable)
enable_btn = gp.Button(list_cont, 'Enable', enable_disable)

selected_inp = gp.Input(selected_cont)
selected_item_btn = gp.Button(selected_cont, 'Set selected item', set_selected)
selected_index_btn = gp.Button(selected_cont, 'Set selected index', set_selected)
deselect_btn = gp.Button(selected_cont, 'Deselect', deselect)

state_inp = gp.Input(state_cont)
item_disable_btn = gp.Button(state_cont, 'Disable item', item_state)
item_enable_btn = gp.Button(state_cont, 'Enable item', item_state)
index_disable_btn = gp.Button(state_cont, 'Disable index', index_state)
index_enable_btn = gp.Button(state_cont, 'Enable index', index_state)

log = gp.Textbox(log_cont)
log.height = 20

widget_cont.set_grid(3, 2)
widget_cont.add(sizes_rdo, 1, 1, fill=True)
widget_cont.add(colours_rdo, 1, 2, fill=True)
widget_cont.add(chriss_rdo, 2, 1, column_span=2)
widget_cont.add(dogs_rdo, 3, 1, column_span=2)

selected_cont.set_grid(1, 4)
selected_cont.add(selected_inp, 1, 1)
selected_cont.add(selected_item_btn, 1, 2)
selected_cont.add(selected_index_btn, 1, 3)
selected_cont.add(deselect_btn, 1, 4)

list_cont.set_grid(1, 4)
list_cont.add(target_dd, 1, 1)
list_cont.add(selected_btn, 1, 2)
list_cont.add(disable_btn, 1, 3)
list_cont.add(enable_btn, 1, 4)

state_cont.set_grid(1, 5)
state_cont.add(state_inp, 1, 1)
state_cont.add(item_disable_btn, 1, 2)
state_cont.add(item_enable_btn, 1, 3)
state_cont.add(index_disable_btn, 1, 4)
state_cont.add(index_enable_btn, 1, 5)

tests_cont.set_grid(3, 1)
tests_cont.add(list_cont, 1, 1)
tests_cont.add(selected_cont, 2, 1)
tests_cont.add(state_cont, 3, 1)

log_cont.set_grid(1, 1)
log_cont.add(log, 1, 1, fill=True, stretch=True)

app.set_grid(3, 1)
app.set_row_weights(0, 0, 1)
app.add(widget_cont, 1, 1, fill=True)
app.add(tests_cont, 2, 1, fill=True)
app.add(log_cont, 3, 1, fill=True)

app.run()
