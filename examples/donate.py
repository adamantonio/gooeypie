import gooeypie as gp


def update_total(event):
    total.text = f'${donation.value + 2}'


app = gp.GooeyPieApp('Donate')

amount = gp.Label(app, 'Donation amount ($)')
donation = gp.Number(app, 5, 1000, 5)
donation.add_event_listener('change', update_total)
donation.read_only = True
processing = gp.Label(app, 'Processing fee')
fee = gp.Label(app, '$2')
total_label = gp.Label(app, 'Total')
total = gp.StyleLabel(app, '$7')
total.font_weight = 'bold'
donate = gp.Button(app, 'Donate', None)

app.set_grid(4, 2)
app.add(amount, 1, 1, align='right')
app.add(donation, 1, 2)
app.add(processing, 2, 1, align='right')
app.add(fee, 2, 2)
app.add(total_label, 3, 1, align='right')
app.add(total, 3, 2)
app.add(donate, 4, 2)

app.run()

