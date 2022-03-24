import gooeypie as gp
from pprint import pprint


def grid(e):
    for row in range(len(app._grid)):
        for col in range(len(app._grid[0])):
            print(str(app._grid[row][col]).ljust(40, ' '), end='|')
        print()


app = gp.GooeyPieApp('Row and column spanning')
app.width = 800
app.height = 600

buttons_container = gp.LabelContainer(app, 'Little Buttons')
labels_container = gp.Container(app)

sub_button1 = gp.Button(buttons_container, 'Little 1', None)
sub_button2 = gp.Button(buttons_container, 'Little 2', None)
sub_button3 = gp.Button(buttons_container, 'Little 3', None)

button1 = gp.Button(app, 'Button 1 - print the grid', grid)
button2 = gp.Button(app, 'Button 2', None)
big_label = gp.StyleLabel(app, 'Label')
big_label.background_colour = 'skyblue'
big_label.align = 'center'
button3 = gp.Button(app, 'Button 3', None)

label1 = gp.StyleLabel(labels_container, 'Little Label 1')
label1.background_colour = 'seagreen'
label1.colour = 'white'
label1.align = 'center'
label1.margin_bottom = 0
label2 = gp.StyleLabel(labels_container, 'Little Label 2')
label2.background_colour = 'pink'
label2.align = 'center'
label2.margin_top = 0

buttons_container.set_grid(1, 3)
buttons_container.add(sub_button1, 1, 1, valign='middle', align='center')
buttons_container.add(sub_button2, 1, 2, valign='middle', align='center')
buttons_container.add(sub_button3, 1, 3, valign='middle', align='center')

labels_container.set_grid(2, 1)
labels_container.set_row_weights(0, 1)
labels_container.add(label1, 1, 1, fill=True, stretch=True)
labels_container.add(label2, 2, 1, fill=True, stretch=True)

app.set_grid(3, 4)
app.add(buttons_container, 1, 1, column_span=2, fill=True, stretch=True)
app.add(button1, 1, 3, column_span=2, fill=True, stretch=True)
app.add(button2, 2, 1, row_span=2, fill=True, stretch=False, valign='bottom')
app.add(labels_container, 2, 4, fill=False, stretch=True, align='right')
app.add(big_label, 2, 2, row_span=2, column_span=2, fill=True, stretch=True)
app.add(button3, 3, 4, fill=True, stretch=True, column_span=1)

app.run()
