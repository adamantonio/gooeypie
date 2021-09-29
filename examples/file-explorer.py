import os
import sys
sys.path.append('..')

import gooeypie as gp

def list_files(event):
    folder_name = open_folder_win.open()
    if folder_name:
        folder_inp.text = folder_name
        files_lst.items = os.listdir(folder_name)

app = gp.GooeyPieApp('File explorer')

folder_lbl = gp.Label(app, 'Folder name')
folder_inp = gp.Input(app)
folder_inp.text = 'No file selected'
folder_inp.disabled = True
open_btn = gp.Button(app, 'Select folder', list_files)
files_lst = gp.Listbox(app)
files_lst.height = 20

open_folder_win = gp.OpenFolderWindow(app, "Select a folder")
open_folder_win.initial_path = '/Users/adam'

app.set_grid(2, 3)
app.width = 400
app.set_column_weights(0, 1, 0)
app.add(folder_lbl, 1, 1, valign='middle')
app.add(folder_inp, 1, 2, fill=True, valign='middle')
app.add(open_btn, 1, 3)
app.add(files_lst, 2, 1, fill=True, column_span=3)

app.run()