import gooeypie as gp


def update_time():
    time_lbl.text = stopwatch.time

    hrs = stopwatch.hours
    mins = stopwatch.minutes
    secs = stopwatch.seconds
    ms = stopwatch.milliseconds
    formatted_time_lbl.text = f'{hrs}:{mins:02}:{secs:02}.{ms:03}'

    stopped_lbl.text = f'Stopped = {stopwatch.stopped}'
    paused_lbl.text = f'Paused = {stopwatch.paused}'


def start(event):
    if stopwatch.time == 0:
        app.set_interval(1, update_time)
    stopwatch.start()


def stop(event):
    stopwatch.stop()


def pause(event):
    stopwatch.pause()


def restart(event):
    stopwatch.restart()


app = gp.GooeyPieApp('Stopwatch')
stopwatch = gp.Timer()

time_lbl = gp.Label(app, '0')
time_lbl.margin_bottom = 0
formatted_time_lbl = gp.StyleLabel(app, '0:00:00.000')
formatted_time_lbl.margin_top = 0
formatted_time_lbl.font_size = 16

start_btn = gp.Button(app, 'Start', start)
stop_btn = gp.Button(app, 'Stop', stop)
pause_btn = gp.Button(app, 'Pause', pause)
restart_btn = gp.Button(app, 'Restart', restart)

stopped_lbl = gp.Label(app, '')
paused_lbl = gp.Label(app, '')

app.set_grid(4, 4)
app.add(time_lbl, 1, 1, column_span=4, align='center')
app.add(formatted_time_lbl, 2, 1, column_span=4, align='center')

app.add(start_btn, 3, 1)
app.add(stop_btn, 3, 2)
app.add(pause_btn, 3, 3)
app.add(restart_btn, 3, 4)

app.add(stopped_lbl, 4, 1, column_span=2, align='center')
app.add(paused_lbl, 4, 3, column_span=2, align='center')

update_time()

app.run()
