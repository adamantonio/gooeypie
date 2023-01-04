import gooeypie as gp

def open_on_top_window(event):
    on_top_window.show_on_top()

def open_other_window(event):
    other_window.show()

# Create main window
app = gp.GooeyPieApp('Other windows')
app.width = 250
on_top_btn = gp.Button(app, 'Open on top', open_on_top_window)
open_other_btn = gp.Button(app, 'Open other window', open_other_window)
app.set_grid(1, 2)
app.add(on_top_btn, 1, 1)
app.add(open_other_btn, 1, 2)

# Create other windows
on_top_window = gp.Window(app, 'On top window')
on_top_window.width = 300
on_top_message = gp.Label(on_top_window, 'This window is on top')
on_top_window.set_grid(1, 1)
on_top_window.add(on_top_message, 1, 1)

other_window = gp.Window(app, 'Other window')
other_window.width = 300
other_message = gp.Label(other_window, 'This is another window')
other_window.set_grid(1, 1)
other_window.add(other_message, 1, 1)

app.run()
