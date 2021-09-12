import gooeypie as gp
from random import choice

colours = ['CornflowerBlue', 'LimeGreen', 'Orchid', 'DarkSlateGray']
fonts = ['times new roman', 'comic sans ms', 'verdana', 'chiller']
styles = ['italic', 'normal']

def change_style(event):
    styled_label.colour = choice(colours)
    styled_label.background_colour = choice(colours)
    styled_label.font_style = choice(styles)
    styled_label.font_name = choice(fonts)

app = gp.GooeyPieApp('style')
app.set_size(300, 150)

styled_label = gp.StyleLabel(app, 'style...?')
styled_label.font_size = 40
styled_label.align = 'center'
styled_label.add_event_listener('mouse_over', change_style)

app.set_grid(1, 1)
app.add(styled_label, 1, 1, fill=True, stretch=True)
app.run()
