import gooeypie as gp


def get_value(event):
    if event.widget == default_get:
        target = default_number
    elif event.widget == inc_get:
        target = inc_number
    elif event.widget == float_get:
        target = float_number
    else:
        print('Something went wrong')

    log.prepend_line(f'Value of {target} is {target.value}')


def set_value(event):
    if event.widget == default_set:
        target = default_number
        value = default_set_value
    elif event.widget == inc_set:
        target = inc_number
        value = inc_set_value
    elif event.widget == float_set:
        target = float_number
        value = float_set_value
    else:
        print('Something went wrong')

    target.value = value.text
    log.prepend_line(f'Value of {target} set to {value.text}')


def enable(event):
    if event.widget == default_enable:
        target = default_number
    elif event.widget == inc_enable:
        target = inc_number
    elif event.widget == float_enable:
        target = float_number
    else:
        print('Something went wrong')

    target.disabled = not target.disabled
    log.prepend_line(f'Disabled state of {target} set to {target.disabled}')


def read_only(event):
    if event.widget == default_read_only:
        target = default_number
    elif event.widget == inc_read_only:
        target = inc_number
    elif event.widget == float_read_only:
        target = float_number
    else:
        print('Something went wrong')

    target.read_only = not target.read_only
    log.prepend_line(f'Readonly state of {target} set to {target.read_only}')


def wrap(event):
    if event.widget == default_wrap:
        target = default_number
    elif event.widget == inc_wrap:
        target = inc_number
    elif event.widget == float_wrap:
        target = float_number
    else:
        print('Something went wrong')

    target.wrap = not target.wrap
    log.prepend_line(f'Wrap state of {target} set to {target.wrap}')


def toggle_change_events(event):
    if change.checked:
        default_number.add_event_listener('change', value_changed)
        inc_number.add_event_listener('change', value_changed)
        float_number.add_event_listener('change', value_changed)
    else:
        default_number.remove_event_listener('change')
        inc_number.remove_event_listener('change')
        float_number.remove_event_listener('change')


def value_changed(event):
    log.prepend_line(f'Value of {event.widget} changed to {event.widget.value}')


app = gp.GooeyPieApp('Number widget tests')

# Widgets container
widgets = gp.LabelContainer(app, 'Widgets and tests')

# Labels
default_label = gp.Label(widgets, 'Integers 1 to 10 (default increment)')
inc_label = gp.Label(widgets, 'Integers 0 to 255 (increment 5)')
float_label = gp.Label(widgets, 'Floats 0 to 1.0 (increment 0.1)')

# Number widgets
default_number = gp.Number(widgets, 1, 10)
inc_number = gp.Number(widgets, 0, 255, 5)
float_number = gp.Number(widgets, 0, 1, 0.1)

default_get = gp.Button(widgets, 'Get value', get_value)
inc_get = gp.Button(widgets, 'Get value', get_value)
float_get = gp.Button(widgets, 'Get value', get_value)

default_set = gp.Button(widgets, 'Set value to', set_value)
inc_set = gp.Button(widgets, 'Set value to', set_value)
float_set = gp.Button(widgets, 'Set value to', set_value)

default_set_value = gp.Input(widgets)
default_set_value.width = 8
default_set_value.margin_left = 0
inc_set_value = gp.Input(widgets)
inc_set_value.width = 8
inc_set_value.margin_left = 0
float_set_value = gp.Input(widgets)
float_set_value.width = 8
float_set_value.margin_left = 0

default_enable = gp.Button(widgets, 'Enable/disable', enable)
inc_enable = gp.Button(widgets, 'Enable/disable', enable)
float_enable = gp.Button(widgets, 'Enable/disable', enable)

default_read_only = gp.Button(widgets, 'Toggle readonly', read_only)
inc_read_only = gp.Button(widgets, 'Toggle readonly', read_only)
float_read_only = gp.Button(widgets, 'Toggle readonly', read_only)

default_wrap = gp.Button(widgets, 'Toggle wrap', wrap)
inc_wrap = gp.Button(widgets, 'Toggle wrap', wrap)
float_wrap = gp.Button(widgets, 'Toggle wrap', wrap)


# Add all testing widgets and tests to widget container
widgets.set_grid(3, 8)

widgets.add(default_label, 1, 1, valign='middle')
widgets.add(default_number, 1, 2, fill=True, valign='middle')
widgets.add(default_get, 1, 3)
widgets.add(default_set, 1, 4)
widgets.add(default_set_value, 1, 5, valign='middle')
widgets.add(default_enable, 1, 6)
widgets.add(default_read_only, 1, 7)
widgets.add(default_wrap, 1, 8)

widgets.add(inc_label, 2, 1, valign='middle')
widgets.add(inc_number, 2, 2, fill=True, valign='middle')
widgets.add(inc_get, 2, 3)
widgets.add(inc_set, 2, 4)
widgets.add(inc_set_value, 2, 5, valign='middle')
widgets.add(inc_enable, 2, 6)
widgets.add(inc_read_only, 2, 7)
widgets.add(inc_wrap, 2, 8)

widgets.add(float_label, 3, 1, valign='middle')
widgets.add(float_number, 3, 2, fill=True, valign='middle')
widgets.add(float_get, 3, 3)
widgets.add(float_set, 3, 4)
widgets.add(float_set_value, 3, 5, valign='middle')
widgets.add(float_enable, 3, 6)
widgets.add(float_read_only, 3, 7)
widgets.add(float_wrap, 3, 8)

# Log container
log_container = gp.LabelContainer(app, 'Log')
log = gp.Textbox(log_container)
log.height = 20
log_container.set_grid(1, 1)
log_container.add(log, 1, 1, fill=True)

# Events
change = gp.Checkbox(app, 'Enable change event on Number widgets')
change.add_event_listener('change', toggle_change_events)

app.set_grid(3, 1)
app.add(widgets, 1, 1)
app.add(change, 2, 1)
app.add(log_container, 3, 1, fill=True)

log.append_line(f'Added {default_number}')
log.append_line(f'Added {inc_number}')
log.append_line(f'Added {float_number}')

app.run()
