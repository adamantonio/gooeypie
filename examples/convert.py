import gooeypie as gp

units = ['mi to km', 'lbs to kg', 'in to cm']

def convert(event):
    try:
        amount = float(convert_num.value)
        if convert_dd.selected == 'mi to km':
            result_lbl.text = f'{convert_num.value} mi = {amount * 1.609:.2f} km'
        elif convert_dd.selected == 'lbs to kg':
            result_lbl.text = f'{convert_num.value} lbs = {amount * 0.454:.2f} kg'
        else:
            result_lbl.text = f'{convert_num.value} in = {amount * 2.54:.2f} cm'
    except ValueError:
        result_lbl.text = 'Please enter a valid number'


app = gp.GooeyPieApp('Unit converter')
convert_lbl = gp.Label(app, 'Convert')
convert_num = gp.Number(app, 0, 100)
convert_dd = gp.Dropdown(app, units)
convert_dd.selected_index = 0
convert_dd.width = 10
convert_btn = gp.ImageButton(app, 'images/convert-icon.png', convert, 'Convert')
result_lbl = gp.Label(app, '')

app.set_grid(2, 4)
app.add(convert_lbl, 1, 1, valign='middle')
app.add(convert_num, 1, 2, valign='middle')
app.add(convert_dd, 1, 3, valign='middle')
app.add(convert_btn, 1, 4)
app.add(result_lbl, 2, 1, column_span=4, align='center')

app.run()