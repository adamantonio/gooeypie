import gooeypie as gp

def say_hello(event):
    hello_label.text = f'Hello {name.text}!'

app = gp.GooeyPieApp('Hello!')

question = gp.Label(app, 'What is your name?')
name = gp.Input(app)
name.justify = 'center'
name.width = 30
hello_button = gp.Button(app, 'Say Hello', say_hello)
hello_label = gp.Label(app, '')

app.set_grid(4, 1)
app.add(question, 1, 1, align='center')
app.add(name, 2, 1)
app.add(hello_button, 3, 1, align='center')
app.add(hello_label, 4, 1, align='center')

app.run()
