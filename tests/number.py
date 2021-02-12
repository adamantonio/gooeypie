import gooeypie as gp


def get_value(event):
    out.prepend(f'Value of "1 to 10" is {standard_number.value}\n')


def set_value(event):
    if event.widget == set_std_button:
        target = int(set_std_input.text)
        out.prepend(f'Setting int to {target}\n')
        standard_number.value = target

    if event.widget == set_float_button:
        target = float(set_float_input.text)
        out.prepend(f'Setting float to {target}\n')
        float_number.value = target


# Create app and containers
app = gp.GooeyPieApp('Number tests')
numbers = gp.LabelContainer(app, 'Widgets')
tests = gp.LabelContainer(app, 'Tests')
log = gp.LabelContainer(app, 'Log')

# Number widgets
standard_label = gp.Label(numbers, 'Integer 1 to 10')
standard_number = gp.Number(numbers, 1, 10)
standard_number.disabled = True

evens_label = gp.Label(numbers, 'Evens ints <= 10')
evens_number = gp.Number(numbers, 2, 10, 2)
evens_number.read_only = True
evens_number.wrap = False

float_label = gp.Label(numbers, 'Float 0.0 to 10.0')
float_number = gp.Number(numbers, 0, 10, 0.1)

numbers.set_grid(3, 2)
numbers.add(standard_label, 1, 1)
numbers.add(standard_number, 1, 2)
numbers.add(evens_label, 2, 1)
numbers.add(evens_number, 2, 2)
numbers.add(float_label, 3, 1)
numbers.add(float_number, 3, 2)


# Tests
value_button = gp.Button(tests, 'Get value', get_value)

set_std_button = gp.Button(tests, 'Set value', set_value)
set_std_input = gp.Input(tests)

set_float_button = gp.Button(tests, 'Set value', set_value)
set_float_input = gp.Input(tests)

tests.set_grid(3, 2)
tests.add(value_button, 1, 1, column_span=2)
tests.add(set_std_button, 2, 1)
tests.add(set_std_input, 2, 2)
tests.add(set_float_button, 3, 1)
tests.add(set_float_input, 3, 2)



# Log
out = gp.Textbox(log)

log.set_grid(1, 1)
log.add(out, 1, 1, fill=True)


# Add containers to app
app.set_grid(2, 2)
app.add(numbers, 1, 1, stretch=True)
app.add(tests, 1, 2, stretch=True)
app.add(log, 2, 1, column_span=2, fill=True)


app.run()

