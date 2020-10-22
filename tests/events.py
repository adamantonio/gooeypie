import gooeypie as gp
import time


def log_event(event):
    now = time.strftime('%H:%M:%S', time.localtime())
    event_string = f'{now}\t{event.event_name} on {event.widget}'
    log.text = f'{event_string}\n{log.text}'


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
radios = gp.Radiogroup(app, default_options)    # ERROR!
listbox = gp.Listbox(app, default_options)
listbox.height = 4
secret = gp.Secret(app)
slider = gp.Slider(app, 1, 10)
spinbox = gp.Spinbox(app, 1, 10)
style_label = gp.StyleLabel(app, 'Style Label')
textbox = gp.Textbox(app)

widgets = (button, checkbox, dropdown, hyperlink, image,
           entry, label, radios_label, radios, listbox, secret,
           slider, spinbox, style_label, textbox)

app.set_grid(len(widgets), 2)

# Add all available events to each widget
for count, w in enumerate(widgets):
    app.add(w, count + 1, 1)
    for e in w._events:
        w.add_event_listener(e, log_event)

# Logging window
log_area = gp.LabelContainer(app, 'Log')
log = gp.Textbox(log_area, 80)
clear = gp.Button(log_area, 'Clear', clear_log)
log_area.set_grid(2, 1)
log_area.add(log, 1, 1, stretch=True)
log_area.add(clear, 2, 1)
log_area.set_row_weights(1, 0)
app.add(log_area, 1, 2, row_span=len(widgets), stretch=True)

app.run()
