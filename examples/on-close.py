import gooeypie as gp

def check_exit():
    ok_to_exit = app.confirm_yesno('Really?', 'Are you sure you want to close?', 'question')
    return ok_to_exit

app = gp.GooeyPieApp('On close')
app.height = 100

nothing_lbl = gp.Label(app, 'I do nothing, but when you close me I will check if you mean it')
app.set_grid(1, 1)
app.add(nothing_lbl, 1, 1, align='center', valign='middle')

app.on_close(check_exit)

app.run()
