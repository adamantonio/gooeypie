import gooeypie as gp

app = gp.GooeyPieApp('Pay Calculator')

def add_hours(event):
    summary_tbl.add_row(date_inp.text, hours_inp.text)

def calculate_total_pay(event):
    hours = 0
    for row in summary_tbl.data:
        hours += float(row[1])
    total_pay = hours * float(rate_inp.text)
    total_lbl.text = f'Total pay: ${total_pay:.2f}'

date_lbl = gp.Label(app, 'Date')
date_inp = gp.Input(app)
date_inp.text = '2021-12-25'
hours_lbl = gp.Label(app, 'Hours worked')
hours_inp = gp.Input(app)
add_btn = gp.Button(app, 'Add', add_hours)
summary_tbl = gp.Table(app, ['Date', 'Hours'])
summary_tbl.set_column_widths(120, 50)
summary_tbl.height = 6
summary_tbl.set_column_alignments('center', 'center')
rate_lbl = gp.Label(app, 'Hourly rate')
rate_inp = gp.Input(app)
calculate_btn = gp.Button(app, 'Calculate', calculate_total_pay)
total_lbl = gp.StyleLabel(app, '')
total_lbl.font_size = 14

app.set_grid(7, 2)
app.add(date_lbl, 1, 1, align='right')
app.add(date_inp, 1, 2)
app.add(hours_lbl, 2, 1, align='right')
app.add(hours_inp, 2, 2)
app.add(add_btn, 3, 2)
app.add(summary_tbl, 4, 1, column_span=2, fill=True)
app.add(rate_lbl, 5, 1, align='right')
app.add(rate_inp, 5, 2)
app.add(calculate_btn, 6, 2)
app.add(total_lbl, 7, 1, column_span=2, align='center')

app.run()
