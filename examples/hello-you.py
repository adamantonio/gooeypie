import gooeypie as gp

def say_hello(event):
    hello_lbl.text = f'Hello {name_inp.text}!'

app = gp.GooeyPieApp('Hello!')

name_lbl = gp.Label(app, 'What is your name?')
name_inp = gp.Input(app)
name_inp.justify = 'center'
name_inp.width = 30
hello_btn = gp.Button(app, 'Say Hello', say_hello)
hello_lbl = gp.Label(app, '')

app.set_grid(4, 1)
app.add(name_lbl, 1, 1, align='center')
app.add(name_inp, 2, 1)
app.add(hello_btn, 3, 1, align='center')
app.add(hello_lbl, 4, 1, align='center')

app.run()
