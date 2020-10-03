import gooeypie as gp

app = gp.GooeyPieApp('Login')

user_label = gp.Label(app, "Username")
user_input = gp.Input(app)
pass_label = gp.Label(app, "Password")
pass_input = gp.Secret(app)

app.set_grid(2, 2)
app.add(user_label, 1, 1)
app.add(user_input, 1, 2)
app.add(pass_label, 2, 1)
app.add(pass_input, 2, 2)

app.run()