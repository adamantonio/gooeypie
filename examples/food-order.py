import gooeypie as gp

meals = ('Beef burger', 'Veggie burger', 'Sausage roll', 'Tofu bowl')
sauces = ('Tomato', 'BBQ', 'Soy', 'No Sauce')

app = gp.GooeyPieApp('Food Order')
app.width = 250

name_text = gp.Label(app, 'Name')
name = gp.Input(app)
food_text = gp.Label(app, 'Food options')
meal = gp.LabelRadiogroup(app, 'Meal', meals)
sauce = gp.LabelRadiogroup(app, 'Sauce', sauces)
order = gp.Button(app, 'Place order', None)

app.set_grid(4, 2)
app.set_column_weights(0, 1)
app.add(name_text, 1, 1, align='right')
app.add(name, 1, 2)
app.add(food_text, 2, 1, align='right')
app.add(meal, 2, 2, fill=True)
app.add(sauce, 3, 2, fill=True)
app.add(order, 4, 2)

app.run()
