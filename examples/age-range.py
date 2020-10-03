import gooeypie as gp

age_ranges = ('Under 18', '18 - 29', '30 - 49', '50 to 64', '65 and over')

app = gp.GooeyPieApp('Age')
app.width = 200

instructions = gp.Label(app, 'Select your age')
age = gp.Radiogroup(app, age_ranges)
confirm = gp.Button(app, 'Confirm', None)

app.set_grid(3, 1)
app.add(instructions, 1, 1)
app.add(age, 2, 1)
app.add(confirm, 3, 1)

app.run()
