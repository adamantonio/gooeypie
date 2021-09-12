import gooeypie as gp

def hello(event):
    if event.widget == de_img:
        greeting_lbl.text = 'Hallo!'
    elif event.widget == fr_img:
        greeting_lbl.text = 'Bonjour!'
    else:
        greeting_lbl.text = 'Hello!'

app = gp.GooeyPieApp('Greetings')

en_img = gp.Image(app, 'images/en.png')
de_img = gp.Image(app, 'images/de.png')
fr_img = gp.Image(app, 'images/fr.png')

en_img.add_event_listener('mouse_down', hello)
de_img.add_event_listener('mouse_down', hello)
fr_img.add_event_listener('mouse_down', hello)

greeting_lbl = gp.StyleLabel(app, '')
greeting_lbl.font_size = 40
greeting_lbl.align = 'center'

app.set_grid(2, 3)
app.add(en_img, 1, 1)
app.add(de_img, 1, 2)
app.add(fr_img, 1, 3)
app.add(greeting_lbl, 2, 1, column_span=3, fill=True)

app.run()
