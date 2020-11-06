import gooeypie as gp

app = gp.GooeyPieApp('Tests: Label')

left = gp.Label(app, 'Left\njustified\nLabel')
center = gp.Label(app, 'Center\njustified\nlabel')
center.justify = 'center'
right = gp.Label(app, 'Right\njustified\nlabel')
right.justify = 'right'

app.set_grid(4, 1)
app.add(left, 1, 1)
app.add(center, 2, 1)
app.add(right, 3, 1)

app.run()
