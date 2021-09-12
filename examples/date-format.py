import gooeypie as gp

date_formats = ['28/8/20', '8/28/20', '28/08/2020', '08/28/2020', '2020-08-28',
                '28-Aug-2020', 'Friday, August 28, 2020', 'Friday, 28 August, 2020',
                'August 28, 2020', '28 August, 2020']

app = gp.GooeyPieApp('Time and date')
app.width = 250

label = gp.Label(app, 'Available formats:')
date_options = gp.Listbox(app, date_formats)
date_options.height = 8
ok = gp.Button(app, 'OK', None)
ok.width = 10

app.set_grid(3, 1)
app.add(label, 1, 1)
app.add(date_options, 2, 1, fill=True)
app.add(ok, 3, 1)

app.run()
