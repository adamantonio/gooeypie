import gooeypie as gp


def increment_count():
    current_count = int(count.text)
    count.text = current_count + 1


def control_counter(event):
    if event.widget.text == 'Pause':
        app.clear_interval()
        start.text = 'Resume'
    else:
        # Increase the count every 100 milliseconds
        app.set_interval(100, increment_count)
        start.text = 'Pause'


app = gp.GooeyPieApp('Fast Counter')
app.width = 240

start = gp.Button(app, 'Start', control_counter)
count = gp.Label(app, '0')
count.width = 4
count.align = 'center'

app.set_grid(1, 2)
app.set_column_weights(1, 0)
app.add(start, 1, 1, fill=True)
app.add(count, 1, 2, valign='middle')

app.run()
