import gooeypie as gp
import datetime

def calculate_age(event):
    today = datetime.date.today()
    dob = dob_dt.date
    difference = today - dob
    answer_lbl.text = f'You are {difference.days} days old!'

app = gp.GooeyPieApp('How old are you?')
app.width = 300

dob_lbl = gp.Label(app, 'When were you born?')
dob_dt = gp.Date(app)
how_many_btn = gp.Button(app, 'How many days old are you?', calculate_age)
answer_lbl = gp.Label(app, '')

current_year = datetime.date.today().year
dob_dt.year_range = [current_year - 100, current_year]
dob_dt.set_selector_order('MDY')

app.set_grid(4, 1)
app.add(dob_lbl, 1, 1, align='center')
app.add(dob_dt, 2, 1, align='center')
app.add(how_many_btn, 3, 1, align='center')
app.add(answer_lbl, 4, 1, align='center')

app.run()
