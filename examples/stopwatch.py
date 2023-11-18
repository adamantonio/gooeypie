import gooeypie as gp

def update_time():
    mins = stopwatch.minutes
    secs = stopwatch.seconds
    ms = stopwatch.milliseconds
    formatted_time_lbl.text = f'{mins:02}:{secs:02}.{ms:03}'

def start_pause(event):
    if start_pause_btn.text == 'Start':
        stopwatch.start()
        start_pause_btn.text = 'Pause'
    else:
        stopwatch.pause()
        start_pause_btn.text = 'Start'

def stop(event):
    stopwatch.stop()
    start_pause_btn.text = 'Start'

app = gp.GooeyPieApp('Stopwatch')
stopwatch = gp.Timer()

formatted_time_lbl = gp.StyleLabel(app, '00:00.000')
formatted_time_lbl.font_size = 20
start_pause_btn = gp.Button(app, 'Start', start_pause)
stop_btn = gp.Button(app, 'Reset', stop)

app.width = 240
app.set_grid(2, 2)
app.add(formatted_time_lbl, 1, 1, column_span=2, align='center')
app.add(start_pause_btn, 2, 1, fill=True)
app.add(stop_btn, 2, 2, fill=True)

# Update the time display every 1ms (approx)
app.set_interval(1, update_time)

app.run()
