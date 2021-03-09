import gooeypie as gp


def press(event):
    t.append(f'{dd.selected}\n')
    dd.deselect()

def selected(event):
    t.prepend(f'Selected is {dd.selected}\n')

def selected_index(event):
    t.prepend(f'Selected is {dd.selected_index}\n')


app = gp.GooeyPieApp('Dropdowns')
# app.set_size(300, 200)

dd = gp.Dropdown(app, ['First', 'Second', 'Third'])
b = gp.Button(app, 'Test', press)
t = gp.Textbox(app)

actions = gp.LabelContainer(app, 'Actions')
selected_button = gp.Button(actions, 'Selected', selected)
selected_index_button = gp.Button(actions, 'Selected Index', selected)

actions.set_grid(2, 2)
actions.set_column_weights(1, 1)
actions.add(selected_button, 1, 1, fill=True)
actions.add(selected_index_button, 1, 2, fill=True)


app.set_grid(3, 1)
app.add(dd, 1, 1, fill=True)
app.add(actions, 2, 1, fill=True)
app.add(t, 3, 1, fill=True)

app.run()