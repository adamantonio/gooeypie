import gooeypie as gp


def convert(event):
    if units.selected == 'Miles':
        factor = 1.60934
        abbr = 'km'
    else:
        factor = 0.621371
        abbr = 'mi'
    converted_distance = quantity.value * factor
    conversion.text = f' = {converted_distance:.2f} {abbr}'


app = gp.GooeyPieApp('Distance converter')

quantity = gp.Number(app, 0, 1000)
units = gp.Dropdown(app, ['Miles', 'Kilometres'])
units.selected_index = 0
conversion = gp.Label(app, ' = 0 km')
conversion.width = 15

quantity.add_event_listener('change', convert)
units.add_event_listener('select', convert)

app.set_grid(1, 3)
app.add(quantity, 1, 1)
app.add(units, 1, 2)
app.add(conversion, 1, 3)

app.run()
