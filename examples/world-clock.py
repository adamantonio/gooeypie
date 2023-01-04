import gooeypie as gp
from datetime import datetime
import pytz

def update_times():
    """Update all time labels"""
    time_local = datetime.now()
    time_local_lbl.text = f'Local time\n{time_local.strftime("%H:%M:%S")}'
    time_london = datetime.now(pytz.timezone('Europe/London'))
    time_london_lbl.text = f'London\n{time_london.strftime("%H:%M:%S")}'
    time_ny = datetime.now(pytz.timezone('America/New_York'))
    time_newyork_lbl.text = f'New York\n{time_ny.strftime("%H:%M:%S")}'

app = gp.GooeyPieApp('World Clock')

time_local_lbl = gp.StyleLabel(app, 'Local time')
time_local_lbl.font_size = 20
time_london_lbl = gp.Label(app, 'London')
time_newyork_lbl = gp.Label(app, 'New York')
sep_v = gp.Separator(app, 'vertical')
sep_h = gp.Separator(app, 'horizontal')

app.set_grid(3, 3)
app.add(time_local_lbl, 1, 1, align='center', valign='middle', row_span=3)
app.add(sep_v, 1, 2, row_span=3)
app.add(time_london_lbl, 1, 3)
app.add(sep_h, 2, 3)
app.add(time_newyork_lbl, 3, 3)

update_times()
app.set_interval(500, update_times)

app.run()
