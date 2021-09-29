import sys
sys.path.append('..')

import gooeypie as gp


def open_file(event):
    filename = open_file_win.open()
    if filename:
        contents_txt.text = open(filename).read()
        filename_inp.text = filename


def save_file(event):
    filename = save_file_win.open()
    if filename:
        open(filename, 'w').write(contents_txt.text)
        filename_inp.text = filename


app = gp.GooeyPieApp('Simple Text Editor')

filename_lbl = gp.Label(app, 'Filename')
filename_inp = gp.Input(app)
filename_inp.text = 'No file selected'
filename_inp.disabled = True
open_btn = gp.Button(app, 'Open file', open_file)
contents_txt = gp.Textbox(app)
contents_txt.height = 10
save_btn = gp.Button(app, 'Save a copy', save_file)

open_file_win = gp.OpenFileWindow(app, 'Open file')
open_file_win.add_file_type('Plain text', '*.txt')
open_file_win.set_initial_folder('desktop')

save_file_win = gp.SaveFileWindow(app, 'Save as')
save_file_win.add_file_type('Plain text', '*.txt')
save_file_win.set_initial_folder('desktop')

app.set_grid(3, 3)
app.width = 600
app.set_column_weights(0, 1, 0)
app.add(filename_lbl, 1, 1, valign='middle')
app.add(filename_inp, 1, 2, fill=True, valign='middle')
app.add(open_btn, 1, 3)
app.add(contents_txt, 2, 1, fill=True, column_span=3)
app.add(save_btn, 3, 1, column_span=3)

app.run()
