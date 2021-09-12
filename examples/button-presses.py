import gooeypie as gp

presses = 0

def button_counter(event):
    global presses
    presses += 1
    if presses <= 5:
        counter.text = f'You have pressed me {presses} times'
    else:
        counter.text = 'You have pressed me enough'
        counter.disabled = True

app = gp.GooeyPieApp('Buttons')
counter = gp.Button(app, 'You have not pressed me yet', button_counter)

app.set_grid(1, 1)
app.add(counter, 1, 1)

app.run()