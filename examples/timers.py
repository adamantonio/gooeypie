import gooeypie as gp

def increment_count():
    count_lbl.text = int(count_lbl.text) + 1

def control_counter(event):
    if event.widget.text == 'Pause':
        app.clear_interval()
        start_btn.text = 'Resume'
    else:
        # Increase the count every millisecond
        app.set_interval(1, increment_count)
        start_btn.text = 'Pause'

app = gp.GooeyPieApp('Fast Counter')
app.width = 240

start_btn = gp.Button(app, 'Start', control_counter)
count_lbl = gp.Label(app, '0')
count_lbl.width = 8
count_lbl.align = 'center'

app.set_grid(1, 2)
app.set_column_weights(1, 0)
app.add(start_btn, 1, 1, fill=True)
app.add(count_lbl, 1, 2, valign='middle')

app.run()