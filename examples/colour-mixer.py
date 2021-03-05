import gooeypie as gp


def change_colour(event):
    # Convert each numbers from 0 to 255 to a 2-digit hex code
    print(type(red_value.value))
    rr = str(hex(int(red_value.value)))[2:].rjust(2, '0')
    gg = str(hex(int(green_value.value)))[2:].rjust(2, '0')
    bb = str(hex(int(blue_value.value)))[2:].rjust(2, '0')
    # Set the background colour
    colour.background_colour = f'#{rr}{gg}{bb}'
    # print(f'#{rr}{gg}{bb}')
    # colour.text = 'boooooooooooooo'


app = gp.GooeyPieApp('Colour Mixer')

red_label = gp.Label(app, 'Red')
green_label = gp.Label(app, 'Green')
blue_label = gp.Label(app, 'Blue')

red_value = gp.Number(app, 0, 255, 5)
green_value = gp.Number(app, 0, 255, 5)
blue_value = gp.Number(app, 0, 255, 5)

# loop though the Number widgets,
for number in (red_value, green_value, blue_value):
    number.add_event_listener('change', change_colour)
    number.wrap = False
    number.margin_top = 0

lines = '\n\n\n\n\n'

colour = gp.StyleLabel(app, lines)
colour.background_colour = 'black'

app.set_grid(3, 3)
app.add(red_label, 1, 1)
app.add(green_label, 1, 2)
app.add(blue_label, 1, 3)
app.add(red_value, 2, 1)
app.add(green_value, 2, 2)
app.add(blue_value, 2, 3)
app.add(colour, 3, 1, column_span=3, fill=True)

app.run()
