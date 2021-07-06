import gooeypie as gp

app = gp.GooeyPieApp('About')
app.width = 300

logo = gp.Image(app, 'images/logo.png')
copy = gp.Label(app, 'Created with Gooey Pie\n© GooeyPie, 2020')
copy.justify = 'center'
link = gp.Hyperlink(app, 'Visit the GooeyPie website', 'www.gooeypie.dev')

app.set_grid(3, 1)
app.add(logo, 1, 1, align='center')
app.add(copy, 2, 1, align='center')
app.add(link, 3, 1, align='center')

app.run()
