import gooeypie as gp

app = gp.GooeyPieApp('Space')

left_btn = gp.Button(app, 'Left', None)
middle_btn = gp.Button(app, 'Middle', None)
right_btn = gp.Button(app, 'Right', None)

app.set_grid(1, 3)
app.set_column_weights(1, 2, 1)
app.add(left_btn, 1, 1)
app.add(middle_btn, 1, 2)
app.add(right_btn, 1, 3)

app.run()
