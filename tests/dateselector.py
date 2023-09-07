import gooeypie as gp
import datetime


def get_date(event):
    log.prepend_line(f'Date is {date_dt.date} {type(date_dt.date)}')


def get_date_string(event):
    log.prepend_line(f'Date string is {repr(date_dt.date_str)} {type(date_dt.date_str)}')


def get_date_part(event):
    if event.widget == get_day_btn:
        log.prepend_line(f'Day is {date_dt.day}')
    if event.widget == get_month_btn:
        log.prepend_line(f'Month number is {date_dt.month}')
    if event.widget == get_month_name_btn:
        log.prepend_line(f'Month name is {date_dt.month_name}')
    if event.widget == get_year_btn:
        log.prepend_line(f'Year is {date_dt.year}')


def set_date_part(event):
    value = set_date_part_inp.text
    if event.widget == set_year_btn:
        date_dt.year = int(value)
        t = 'year'
    elif event.widget == set_month_btn:
        date_dt.month = int(value)
        t = 'month'
    elif event.widget == set_month_name_btn:
        date_dt.month_name = value
        t = 'month name'
    elif event.widget == set_day_btn:
        date_dt.day = int(value)
        t = 'day'
    log.prepend_line(f'Set {t} to {value}')


def set_date(event):
    if event.widget == set_today_btn:
        date_dt.date = datetime.date.today()

    elif event.widget == set_tomorrow_btn:
        date_dt.date = datetime.date.today() + datetime.timedelta(days=1)
    elif event.widget == set_next_week_btn:
        date_dt.date = date_dt.date + datetime.timedelta(days=7)
    elif event.widget == set_any_date_btn:
        date_dt.date = set_any_date_inp.text


def move_date(event):
    delta = int(move_date_inp.text)
    if event.widget == move_days_btn:
        date_dt.add_days(delta)
        t = 'days'
    elif event.widget == move_months_btn:
        date_dt.add_months(delta)
        t = 'months'
    elif event.widget == move_years_btn:
        date_dt.add_years(delta)
        t = 'years'
    log.prepend_line(f'Added {delta} {t}')


def clear(event):
    if event.widget == clear_btn:
        date_dt.clear()
    elif event.widget == clear_year_btn:
        date_dt.year = None
    elif event.widget == clear_month_btn:
        date_dt.month = None
    elif event.widget == clear_day_btn:
        date_dt.day = None


def toggle_state(event):
    if event.widget == date_state_btn:
        date_dt.disabled = not date_dt.disabled
        log.prepend_line(f'date widget disabled state set to {date_dt.disabled}')
    elif event.widget == year_state_btn:
        date_dt.year_disabled = not date_dt.year_disabled
        log.prepend_line(f'year select disabled state set to {date_dt.year_disabled}')
    elif event.widget == month_state_btn:
        date_dt.month_disabled = not date_dt.month_disabled
        log.prepend_line(f'month select disabled state set to {date_dt.month_disabled}')
    elif event.widget == day_state_btn:
        date_dt.day_disabled = not date_dt.day_disabled
        log.prepend_line(f'day select disabled state set to {date_dt.day_disabled}')


def date_changed(event):
    log.prepend_line(f'Date changed to {date_dt.date}')


def run_eval(event):
    # date_dt.year_range = [2000, 2020]
    cmd = eval_inp.text
    eval(cmd)


app = gp.GooeyPieApp('Date Selector Test')

# Containers
date_cont = gp.LabelContainer(app, 'Date widget')
testing_cont = gp.LabelContainer(app, 'Tests')
log_cont = gp.LabelContainer(app, 'Log')

# Sub containers
get_date_cont = gp.Container(testing_cont)
get_date_parts_cont = gp.Container(testing_cont)
set_date_parts_cont = gp.Container(testing_cont)
set_date_cont = gp.Container(testing_cont)
set_any_date_cont = gp.Container(testing_cont)
move_date_cont = gp.Container(testing_cont)
clear_cont = gp.Container(testing_cont)
state_cont = gp.Container(testing_cont)
eval_cont = gp.Container(testing_cont)

# Widgets
date_dt = gp.Date(date_cont)

# Widget customisation
date_dt.set_selector_order('MDY')
# date_dt.set_separator('/')
date_dt.set_month_display('full')
date_dt.year_range = [1950, 2023]
date_dt.disabled_year = True

get_date_btn = gp.Button(get_date_cont, 'Get date', get_date)
get_date_str_btn = gp.Button(get_date_cont, 'Get date string', get_date_string)

get_day_btn = gp.Button(get_date_parts_cont, 'Get day', get_date_part)
get_month_btn = gp.Button(get_date_parts_cont, 'Get month number', get_date_part)
get_month_name_btn = gp.Button(get_date_parts_cont, 'Get month name', get_date_part)
get_year_btn = gp.Button(get_date_parts_cont, 'Get year', get_date_part)

set_date_part_lbl = gp.Label(set_date_parts_cont, 'Set date:')
set_date_part_inp = gp.Input(set_date_parts_cont)
set_date_part_inp.width = 6
set_day_btn = gp.Button(set_date_parts_cont, 'Day', set_date_part)
set_month_btn = gp.Button(set_date_parts_cont, 'Month', set_date_part)
set_month_name_btn = gp.Button(set_date_parts_cont, 'Month name', set_date_part)
set_year_btn = gp.Button(set_date_parts_cont, 'Year', set_date_part)

set_date_lbl = gp.Label(set_date_cont, 'Set date to:')
set_today_btn = gp.Button(set_date_cont, 'Today', set_date)
set_tomorrow_btn = gp.Button(set_date_cont, 'Tomorrow', set_date)
set_next_week_btn = gp.Button(set_date_cont, 'Next week', set_date)

set_any_date_lbl = gp.Label(set_any_date_cont, 'Set date to:')
set_any_date_inp = gp.Input(set_any_date_cont)
set_any_date_inp.text = '1985-10-26'
set_any_date_btn = gp.Button(set_any_date_cont, 'Set', set_date)

move_date_lbl = gp.Label(move_date_cont, 'Move date by:')
move_date_inp = gp.Input(move_date_cont)
move_date_inp.width = 4
move_days_btn = gp.Button(move_date_cont, 'Days', move_date)
move_months_btn = gp.Button(move_date_cont, 'Months', move_date)
move_years_btn = gp.Button(move_date_cont, 'Years', move_date)

clear_btn = gp.Button(clear_cont, 'Clear', clear)
clear_year_btn = gp.Button(clear_cont, 'Year to None', clear)
clear_month_btn = gp.Button(clear_cont, 'Month to None', clear)
clear_day_btn = gp.Button(clear_cont, 'Day to None', clear)

date_state_btn = gp.Button(state_cont, 'Toggle date state', toggle_state)
year_state_btn = gp.Button(state_cont, 'Toggle year state', toggle_state)
month_state_btn = gp.Button(state_cont, 'Toggle month state', toggle_state)
day_state_btn = gp.Button(state_cont, 'Toggle day state', toggle_state)

eval_inp = gp.Input(eval_cont)
eval_inp.width = 30
eval_btn = gp.Button(eval_cont, 'eval', run_eval)

log = gp.Textbox(log_cont)
log.width = 50
log.height = 15

# Sub container grids
get_date_cont.set_grid(1, 2)
get_date_cont.add(get_date_btn, 1, 1)
get_date_cont.add(get_date_str_btn, 1, 2)

get_date_parts_cont.set_grid(1, 4)
get_date_parts_cont.add(get_day_btn, 1, 1)
get_date_parts_cont.add(get_month_btn, 1, 2)
get_date_parts_cont.add(get_month_name_btn, 1, 3)
get_date_parts_cont.add(get_year_btn, 1, 4)

set_date_parts_cont.set_grid(1, 6)
set_date_parts_cont.add(set_date_part_lbl, 1, 1)
set_date_parts_cont.add(set_date_part_inp, 1, 2)
set_date_parts_cont.add(set_day_btn, 1, 3)
set_date_parts_cont.add(set_month_btn, 1, 4)
set_date_parts_cont.add(set_month_name_btn, 1, 5)
set_date_parts_cont.add(set_year_btn, 1, 6)

set_date_cont.set_grid(1, 4)
set_date_cont.add(set_date_lbl, 1, 1)
set_date_cont.add(set_today_btn, 1, 2)
set_date_cont.add(set_tomorrow_btn, 1, 3)
set_date_cont.add(set_next_week_btn, 1, 4)

set_any_date_cont.set_grid(1, 3)
set_any_date_cont.add(set_any_date_lbl, 1, 1)
set_any_date_cont.add(set_any_date_inp, 1, 2)
set_any_date_cont.add(set_any_date_btn, 1, 3)

move_date_cont.set_grid(1, 5)
move_date_cont.add(move_date_lbl, 1, 1)
move_date_cont.add(move_date_inp, 1, 2)
move_date_cont.add(move_days_btn, 1, 3)
move_date_cont.add(move_months_btn, 1, 4)
move_date_cont.add(move_years_btn, 1, 5)

clear_cont.set_grid(1, 4)
clear_cont.add(clear_btn, 1, 1)
clear_cont.add(clear_year_btn, 1, 2)
clear_cont.add(clear_month_btn, 1, 3)
clear_cont.add(clear_day_btn, 1, 4)

state_cont.set_grid(1, 4)
state_cont.add(date_state_btn, 1, 1)
state_cont.add(year_state_btn, 1, 2)
state_cont.add(month_state_btn, 1, 3)
state_cont.add(day_state_btn, 1, 4)

eval_cont.set_grid(1, 2)
eval_cont.add(eval_inp, 1, 1)
eval_cont.add(eval_btn, 1, 2)

# Label containers
date_cont.set_grid(1, 1)
date_cont.add(date_dt, 1, 1)

testing_cont.set_grid(9, 1)
testing_cont.add(get_date_cont, 1, 1)
testing_cont.add(get_date_parts_cont, 2, 1)
testing_cont.add(set_date_parts_cont, 3, 1)
testing_cont.add(set_date_cont, 4, 1)
testing_cont.add(set_any_date_cont, 5, 1)
testing_cont.add(move_date_cont, 6, 1)
testing_cont.add(clear_cont, 7, 1)
testing_cont.add(state_cont, 8, 1)
testing_cont.add(eval_cont, 9, 1)

log_cont.set_grid(1, 1)
log_cont.add(log, 1, 1, fill=True, stretch=True)

# Main grid
app.set_grid(3, 1)
app.add(date_cont, 1, 1, fill=True)
app.add(testing_cont, 2, 1, fill=True)
app.add(log_cont, 3, 1, fill=True)

date_dt.add_event_listener('mouse_over', lambda e: print("over"))
date_dt.add_event_listener('double_click', lambda e: print("dbl click"))

# event
date_dt.add_event_listener('change', date_changed)

app.run()


