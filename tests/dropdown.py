import gooeypie as gp


def press(event):
    t.append(f'{dd.selected}\n')
    dd.deselect()


app = gp.GooeyPieApp('Dropdowns')
app.set_size(300, 200)

dd = gp.Dropdown(app, ['First', 'Second', 'Third'])
b = gp.Button(app, 'Test', press)
t = gp.Textbox(app)

app.set_grid(3, 1)
app.add(dd, 1, 1, fill=True)
app.add(b, 2, 1, fill=True)
app.add(t, 3, 1, fill=True)

app.run()