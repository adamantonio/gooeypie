import gooeypie as gp

def say_hello(event):
    hello_label.text = 'Hello Gooey Pie!'

app = gp.GooeyPieApp('Hello!')
app.set_size(250, 80)
app.set_grid(2, 1)
#
hello_button = gp.Button(app, 'Say Hello', None)
hello_label = gp.Label(app, '')
#
app.add(hello_button, 1, 1, align='center')
app.add(hello_label, 2, 1, align='center')

app.run()
