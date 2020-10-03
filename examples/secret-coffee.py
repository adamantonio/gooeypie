import gooeypie as gp

def toggle_mask(event):
    secret.toggle()

app = gp.GooeyPieApp('Secret')

question = gp.Label(app, "What's your secret?")

secret = gp.Secret(app)
secret.width = 50

check = gp.Checkbox(app, 'Show secret')
check.add_event_listener('change', toggle_mask)

app.set_grid(3, 1)
app.add(question, 1, 1)
app.add(secret, 2, 1)
app.add(check, 3, 1)

app.run()