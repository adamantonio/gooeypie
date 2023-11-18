import gooeypie as gp
from random import randint

label_changes = 0


def set_random_number():
    """Change to the label to a random number from 1 and 99"""

    # Increment the label_changes variable and clear the interval if 25 changes have been made
    global label_changes
    label_changes += 1
    if label_changes == 25:
        label_changes = 0
        app.clear_interval()

    # Set the label to a new random number
    number_lbl.text = randint(1, 99)


def start(event):
    """Sets up the interval to change the label 25 times every 10ms before stopping"""
    app.set_interval(10, set_random_number)


app = gp.GooeyPieApp('Random!')
app.width = 250

number_lbl = gp.StyleLabel(app, '?')
number_lbl.font_size = 30
number_lbl.font_weight = 'bold'

generate_btn = gp.Button(app, 'Gimme a random number!', start)

app.set_grid(2, 1)
app.add(number_lbl, 1, 1, align='center')
app.add(generate_btn, 2, 1, align='center')

app.run()
