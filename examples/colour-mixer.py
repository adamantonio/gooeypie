import gooeypie as gp


def change_colour(event):
    # Convert each number value from 0 to 255 to a 2-digit hex code
    rr = str(hex(red_value.value))[2:].rjust(2, '0')
    gg = str(hex(green_value.value))[2:].rjust(2, '0')
    bb = str(hex(blue_value.value))[2:].rjust(2, '0')

    # Set the background colour
    colour.background_colour = f'#{rr}{gg}{bb}'


app = gp.GooeyPieApp('Colour Mixer')

red_label = gp.Label(app, 'Red')
green_label = gp.Label(app, 'Green')
blue_label = gp.Label(app, 'Blue')

red_value = gp.Number(app, 0, 255, 5)
green_value = gp.Number(app, 0, 255, 5)
blue_value = gp.Number(app, 0, 255, 5)

# loop though the Number widgets, setting relevant options
for number in (red_value, green_value, blue_value):
    number.add_event_listener('change', change_colour)
    number.wrap = False
    number.margin_top = 0

# Empty style label to display the colour
colour = gp.StyleLabel(app, '\n\n\n\n\n')
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
