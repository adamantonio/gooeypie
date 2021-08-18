import gooeypie as gp


def press(event):
    t.append(f'{dd.selected}\n')
    dd.deselect()

def selected(event):
    t.prepend(f'Selected is {dd.selected}\n')
    print(f'Dimensions of container: {actions.width}x{actions.height}')

def selected_index(event):
    t.prepend(f'Selected index is {dd.selected_index}\n')


app = gp.GooeyPieApp('Dropdowns')
# app.width = 600

dd = gp.Dropdown(app, ['First', 'Second', 'Third'])
b = gp.Button(app, 'Test', press)
t = gp.Textbox(app)

actions = gp.LabelContainer(app, 'Actions')
actions.height = 100
actions.width = 50
selected_button = gp.Button(actions, 'Selected', selected)
selected_index_button = gp.Button(actions, 'Selected Index', selected_index)

actions.set_grid(2, 2)
actions.set_column_weights(1, 1)
actions.add(selected_button, 1, 1, fill=True)
actions.add(selected_index_button, 1, 2, fill=True)


app.set_grid(3, 1)
app.set_row_weights(0, 0, 1)
app.add(dd, 1, 1, fill=True)
app.add(actions, 2, 1, fill=True)
app.add(t, 3, 1, fill=True, stretch=True)

app.run()