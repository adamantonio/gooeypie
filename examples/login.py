import gooeypie as gp

def login(event):
    if pass_inp.text == 'bestpassword':
        status_lbl.text = '✔ Access granted!'
    else:
        status_lbl.text = '❌ Access denied!'

app = gp.GooeyPieApp('Login')

user_lbl = gp.Label(app, "Username")
user_inp = gp.Input(app)
pass_lbl = gp.Label(app, "Password")
pass_inp = gp.Secret(app)
login_btn = gp.Button(app, 'Login', login)
status_lbl = gp.Label(app, '')

app.set_grid(4, 2)
app.add(user_lbl, 1, 1)
app.add(user_inp, 1, 2)
app.add(pass_lbl, 2, 1)
app.add(pass_inp, 2, 2)
app.add(login_btn, 3, 2)
app.add(status_lbl, 4, 2)

app.run()