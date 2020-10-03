import gooeypie as gp

def what_is_selected(event):
    print(genders.selected)
    print(genders.options)

app = gp.GooeyPieApp('Testing Radios')

genders = gp.Radiogroup(app, ('Female', 'Male', 'Other'))
button = gp.Button(app, 'What is selected', what_is_selected)

app.set_grid(2, 1)
app.add(genders, 1, 1)
app.add(button, 2, 1)
app.run()
