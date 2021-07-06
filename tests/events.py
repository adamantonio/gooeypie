import gooeypie as gp
import time


def log_event(event):
    now = time.strftime('%H:%M:%S', time.localtime())
    if event.event_name == 'key_press':
        event_string = f'{now}\t{event.key}'
    else:
        event_string = f'{now}\t{event.event_name} on {event.widget}'
    log.prepend(f'{event_string}\n')


def remove_listeners(event):
    for w in widgets:
        for e in w._events:
            w.remove_event_listener(e)


def enable_disable(event):
    for w in widgets:
        w.disabled = not w.disabled


def clear_log(event):
    log.text = ''


app = gp.GooeyPieApp('Event tests')

# Widgets for testing
default_options = ['One', 'Two', 'Three']
button = gp.Button(app, 'Button', None)
checkbox = gp.Checkbox(app, 'Checkbox')
dropdown = gp.Dropdown(app, default_options)
hyperlink = gp.Hyperlink(app, 'Hyperlink', 'www.example.com')
image = gp.Image(app, 'logo.png')
entry = gp.Input(app)
label = gp.Label(app, 'Label')
radios_label = gp.LabelRadiogroup(app, 'LabelRadiogroup', default_options)
radios = gp.Radiogroup(app, default_options)
listbox = gp.Listbox(app, default_options)
listbox.height = 4
secret = gp.Secret(app)
slider = gp.Slider(app, 1, 10)
number = gp.Number(app, 1, 10)
style_label = gp.StyleLabel(app, 'Style Label')
textbox = gp.Textbox(app)

widgets = (button, checkbox, dropdown, hyperlink, image,
           entry, label, radios_label, radios, listbox, secret,
           slider, number, style_label, textbox)

app.set_grid(len(widgets), 2)

# Add all available events to each widget
for count, w in enumerate(widgets):
    app.add(w, count + 1, 1)
    for e in w._events:
        try:
            w.add_event_listener(e, log_event)
        except gp.GooeyPieError:
            # Hyperlinks have restricted events
            pass

# Logging window
log_area = gp.LabelContainer(app, 'Log')

button_area = gp.Container(log_area)
button_area.set_grid(1, 3)
clear = gp.Button(button_area, 'Clear', clear_log)
remove = gp.Button(button_area, 'Remove all listeners', remove_listeners)
enable = gp.Button(button_area, 'Enable/disable all', enable_disable)
button_area.add(clear, 1, 1)
button_area.add(remove, 1, 2)
button_area.add(enable, 1, 3)

log = gp.Textbox(log_area, 80)
log_area.set_grid(2, 1)
log_area.add(log, 1, 1, stretch=True)
log_area.add(button_area, 2, 1)
log_area.set_row_weights(1, 0)
app.add(log_area, 1, 2, row_span=len(widgets), stretch=True)

app.run()
