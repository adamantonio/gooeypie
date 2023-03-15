import gooeypie as gp

def set_value(event):
    try:
        test_bar.value = set_value_num.value
    except Exception as e:
        log.prepend_line(e)

def get_value(event):
    log.prepend_line(f'Progress bar value: {test_bar.value}')
    print(test_bar.width)

def move(event):
    if event.widget == start_btn:
        test_bar.start()
    else:
        test_bar.stop()

def mode(event):
    test_bar.mode = f"{'in' * mode_dd.selected_index}determinate"

app = gp.GooeyPieApp('ProgressBar Test')

widget_cont = gp.LabelContainer(app, 'Progress Bar')
widget_cont.width = 280
testing_cont = gp.LabelContainer(app, 'Tests')
log_cont = gp.LabelContainer(app, 'Log')

test_bar = gp.Progressbar(widget_cont, 'determinate')
log = gp.Textbox(log_cont)

set_value_num = gp.Number(testing_cont, 1, 100)
set_value_btn = gp.Button(testing_cont, 'Set value', set_value)
get_value_btn = gp.Button(testing_cont, 'Get Value', get_value)

start_btn = gp.Button(testing_cont, 'Start', move)
stop_btn = gp.Button(testing_cont, 'Stop', move)

mode_lbl = gp.Label(testing_cont, 'Mode')
mode_dd = gp.Dropdown(testing_cont, ['Determinate', 'Indeterminate'])
mode_dd.selected_index = 0
mode_dd.add_event_listener('select', mode)

widget_cont.set_grid(1, 1)
widget_cont.add(test_bar, 1, 1, fill=True)

testing_cont.set_grid(3, 3)
testing_cont.set_column_weights(0, 0, 1)
testing_cont.add(set_value_num, 1, 1, valign='middle')
testing_cont.add(set_value_btn, 1, 2)
testing_cont.add(get_value_btn, 1, 3)
testing_cont.add(start_btn, 2, 2)
testing_cont.add(stop_btn, 2, 3)
testing_cont.add(mode_lbl, 3, 1)
testing_cont.add(mode_dd, 3, 2)

log_cont.set_grid(1, 1)
log_cont.add(log, 1, 1, fill=True, stretch=True)

app.set_grid(3, 1)
app.set_row_weights(0, 0, 1)
app.add(widget_cont, 1, 1, fill=True)
app.add(testing_cont, 2, 1, fill=True)
app.add(log_cont, 3, 1, fill=True)

app.run()
