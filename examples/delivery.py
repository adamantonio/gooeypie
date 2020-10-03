import gooeypie as gp

app = gp.GooeyPieApp('Delivery')

delivery_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

instructions = gp.Label(app, 'Select your preferred day for delivery')
delivery_day = gp.Dropdown(app, delivery_days)
print(delivery_day)
delivery_day.selected_index = 0   # Make Monday the default
continue_button = gp.Button(app, 'Continue', None)

app.set_grid(3, 1)
app.add(instructions, 1, 1)
app.add(delivery_day, 2, 1, fill=True)
app.add(continue_button, 3, 1, align='right')

app.run()