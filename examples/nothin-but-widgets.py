import gooeypie as gp

app = gp.GooeyPieApp('Widget Gallery')
app.set_grid(16, 1)
app.width = 200

app.add(gp.Input(app), 1, 1, fill=True)
app.add(gp.Checkbox(app, 'Checkbox'), 2, 1)
app.add(gp.Label(app, 'Label'), 3, 1)
app.add(gp.Slider(app, 1, 10), 4, 1, fill=True)

style_label = gp.StyleLabel(app, 'StyleLabel')
style_label.font_name = 'Courier'
style_label.font_size = 16
style_label.font_weight = 'bold'
style_label.colour = '#FF6702'
style_label.background_colour = 'black'
app.add(style_label, 5, 1, align='center')

app.add(gp.Hyperlink(app, 'Hyperlink', '.'), 6, 1)
app.add(gp.Secret(app), 7, 1, fill=True)
app.add(gp.SimpleListbox(app, [f'Listbox item {n}' for n in range(1, 7)]), 8, 1, fill=True)
app.add(gp.Textbox(app), 9, 1, fill=True)
app.add(gp.ImageButton(app, 'images/favicon.ico', None, '   ImageButton'), 10, 1, fill=True)
app.add(gp.Radiogroup(app, [f'Radio item {n}' for n in range(1, 4)]), 11, 1, fill=True)
app.add(gp.LabelRadiogroup(app, 'Radio Group', [f'Radio item {n}' for n in range(1, 4)]), 12, 1, fill=True)
app.add(gp.Spinbox(app, 1, 10), 13, 1)
app.add(gp.Button(app, 'Button', None), 14, 1, fill=True)
app.add(gp.Dropdown(app, [f'Dropdown item {n}' for n in range(1, 9)]), 15, 1, fill=True)
app.add(gp.Image(app, 'images/logo.png'), 16, 1, align='center')

app.run()
