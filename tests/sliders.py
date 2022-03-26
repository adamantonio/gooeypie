import gooeypie as gp


def slider_change(event):
    print(event.widget.value)
    if event.widget == slider_h_int:
        h_int_lbl.text = slider_h_int.value
    if event.widget == slider_h_float:
        h_float_lbl.text = f'{slider_h_float.value:.2f}'
    if event.widget == slider_v_int:
        v_int_lbl.text = slider_v_int.value
    if event.widget == slider_v_float:
        v_float_lbl.text = f'{slider_v_float.value:.2f}'


def listen(event):
    for slider in (slider_h_int, slider_h_float, slider_v_int, slider_v_float):
        if events_chk.checked:
            slider.add_event_listener('change', slider_change)
        else:
            slider.remove_event_listener('change')


def toggle_state(event):
    for slider in (slider_h_int, slider_h_float, slider_v_int, slider_v_float):
        slider.disabled = disable_chk.checked


app = gp.GooeyPieApp('Sliders')

horizontal_cont = gp.LabelContainer(app, 'Horizontal sliders')
vertical_cont = gp.LabelContainer(app,  'Vertical sliders')

slider_h_int = gp.Slider(horizontal_cont, 1, 10)
slider_h_int.add_event_listener('change', slider_change)
slider_h_int.length = 200
h_int_lbl = gp.Label(horizontal_cont, '')
h_int_lbl.width = 4
h_int_lbl.align = 'center'
slider_h_float = gp.Slider(horizontal_cont, 0.0, 1.0)
slider_h_float.add_event_listener('change', slider_change)
h_float_lbl = gp.Label(horizontal_cont, '')
h_float_lbl.width = 4
h_float_lbl.align = 'center'

slider_v_int = gp.Slider(vertical_cont, 1, 10, orientation='vertical')
slider_v_int.add_event_listener('change', slider_change)
slider_v_int.length = 200
slider_v_float = gp.Slider(vertical_cont, 0.0, 1.0, orientation='vertical')
slider_v_float.add_event_listener('change', slider_change)
v_int_lbl = gp.Label(vertical_cont, '')
v_int_lbl.width = 4
v_int_lbl.align = 'center'
v_float_lbl = gp.Label(vertical_cont, '')
v_float_lbl.width = 4
v_float_lbl.align = 'center'

horizontal_cont.set_grid(2, 2)
horizontal_cont.set_column_weights(1, 0)
horizontal_cont.add(slider_h_int, 1, 1, fill=True)
horizontal_cont.add(h_int_lbl, 1, 2)
horizontal_cont.add(slider_h_float, 2, 1, fill=True)
horizontal_cont.add(h_float_lbl, 2, 2)

vertical_cont.set_grid(2, 2)
vertical_cont.set_row_weights(1, 0)
vertical_cont.add(slider_v_int, 1, 1, align='center', stretch=True)
vertical_cont.add(slider_v_float, 1, 2, align='center', stretch=True)
vertical_cont.add(v_int_lbl, 2, 1, align='center')
vertical_cont.add(v_float_lbl, 2, 2, align='center')

disable_chk = gp.Checkbox(app, 'Enable/disable all')
disable_chk.add_event_listener('change', toggle_state)

events_chk = gp.Checkbox(app, 'Listen for changes')
events_chk.add_event_listener('change', listen)
events_chk.checked = True

app.set_grid(4, 1)
app.add(horizontal_cont, 1, 1, fill=True)
app.add(vertical_cont, 2, 1, fill=True)
app.add(disable_chk, 3, 1)
app.add(events_chk, 4, 1)

app.run()
