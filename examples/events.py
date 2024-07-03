import gooeypie as gp

app = gp.GooeyPieApp('Events demo')

def over(event):
    event_lbl.text = 'You moved over the logo!'

def click(event):
    event_lbl.text = 'Now you clicked the logo!'

def out(event):
    event_lbl.text = 'Bye bye now!'


logo_img = gp.Image(app, 'images/logo.png')
event_lbl = gp.Label(app, '')

app.set_grid(2, 1)
app.add(logo_img, 1, 1, align='center')
app.add(event_lbl, 2, 1, align='center')

logo_img.add_event_listener('mouse_over', over)
logo_img.add_event_listener('mouse_down', click)
logo_img.add_event_listener('mouse_out', out)

app.width = 250
app.run()
