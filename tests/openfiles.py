import sys
sys.path.append('..')

import gooeypie as gp
import random

filetypes = set()

def start(event):
    log.clear()
    if window_type_dd.selected == 'Open folder':
        win = gp.OpenFolderWindow(app, title_inp.text)
    else:
        if window_type_dd.selected == 'Open file':
            win = gp.OpenFileWindow(app, title_inp.text)
            if multiple.checked:
                win.allow_multiple = True
        elif window_type_dd.selected == 'Save file':
            win = gp.SaveFileWindow(app, title_inp.text)

        for desc, ext in filetypes:
            win.add_file_type(desc, ext)

    if initial_folder_btn.text == 'Clear':
        location = initial_folder_dd.selected
        subfolders = paths_inp.text.split('/')
        win.set_initial_folder(location, *subfolders)
        log.append_line(f'Initial folder: {location}/{"/".join(subfolders)}')
    elif initial_path_btn.text == 'Clear':
        path = initial_path_inp.text
        win.initial_path = path
        log.append_line(f'Initial path: {path}')
    else:
        log.append_line('No initial folder set')

    if window_type_dd.selected != 'Open folder':
        if filetypes:
            log.append_line(f'File types: {filetypes}')
        else:
            log.append_line(f'No file types set')

    log.append_line(f'{win.open()}\n')


def window_type_select(event):
    title_inp.text = window_type_dd.selected


def set_preset(event):
    if event.widget == image_presets_btn:
        filetypes.add(('Images', '*.png *.gif *.jpg'))
    elif event.widget == text_preset_btn:
        filetypes.add(('Plain text', '*.txt'))
    elif event.widget == pdf_preset_btn:
        filetypes.add(('PDF', '*.pdf'))
    elif event.widget == all_preset_btn:
        filetypes.add(('All files', '*.*'))
    else:
        filetypes.clear()

    update_extensions_list()


def add_file_type(event):
    if description_inp.text and extension_inp.text:
        filetypes.add((description_inp.text, extension_inp.text))
        update_extensions_list()
        description_inp.text = ''
        extension_inp.text = ''


def update_extensions_list():
    all_extensions_list.items = []
    for desc, ext in filetypes:
        all_extensions_list.add_item(f'{desc} ({ext})')


def set_initial_folder(event):
    global start_dir
    if initial_folder_btn.text == 'Set':
        initial_folder_btn.text = 'Clear'
        initial_path_lbl.disabled = True
        initial_path_inp.disabled = True
        initial_path_btn.disabled = True
    else:
        initial_folder_btn.text = 'Set'
        initial_path_lbl.disabled = False
        initial_path_inp.disabled = False
        initial_path_btn.disabled = False


def set_initial_path(event):
    global start_dir
    if initial_path_btn.text == 'Set':
        initial_path_btn.text = 'Clear'
        initial_folder_lbl.disabled = True
        initial_folder_dd.disabled = True
        paths_inp.disabled = True
        initial_folder_btn.disabled = True
    else:
        initial_path_btn.text = 'Set'
        initial_folder_lbl.disabled = False
        initial_folder_dd.disabled = False
        paths_inp.disabled = False
        initial_folder_btn.disabled = False


app = gp.GooeyPieApp('Opening files and folders')
app.width = 600

type_cont = gp.LabelContainer(app, 'Window Type')
initial_cont = gp.LabelContainer(app, 'Initial path')
filetypes_cont = gp.LabelContainer(app, 'File types')
presets_cont = gp.Container(filetypes_cont)
log_cont = gp.LabelContainer(app, 'Log')

# Window type
window_type_dd = gp.Dropdown(type_cont, ('Open file', 'Save file', 'Open folder'))
window_type_dd.selected = random.choice(window_type_dd.items)
title_lbl = gp.Label(type_cont, 'Title')
title_inp = gp.Input(type_cont)
title_inp.text = window_type_dd.selected

# Initial path
initial_folder_lbl = gp.Label(initial_cont, 'Initial folder')
initial_folder_dd = gp.Dropdown(initial_cont, ('home', 'documents', 'desktop', 'app'))
initial_folder_dd.selected = random.choice(initial_folder_dd.items)
paths_inp = gp.Input(initial_cont)
initial_folder_btn = gp.Button(initial_cont, 'Set', set_initial_folder)
initial_path_lbl = gp.Label(initial_cont, 'Initial path')
initial_path_inp = gp.Input(initial_cont)
initial_path_btn = gp.Button(initial_cont, 'Set', set_initial_path)

# File types
description_lbl = gp.Label(filetypes_cont, 'Description')
description_inp = gp.Input(filetypes_cont)
extension_lbl = gp.Label(filetypes_cont, 'Extension')
extension_inp = gp.Input(filetypes_cont)
add_type_btn = gp.Button(filetypes_cont, 'Add file type', add_file_type)
all_extensions_list = gp.Listbox(filetypes_cont)
all_extensions_list.height = 5
multiple = gp.Checkbox(filetypes_cont, 'Allow multiple selection for open files')

# Presets
preset_lbl = gp.Label(presets_cont, 'Presets')
image_presets_btn = gp.Button(presets_cont, 'Images', set_preset)
text_preset_btn = gp.Button(presets_cont, 'Text', set_preset)
pdf_preset_btn = gp.Button(presets_cont, 'PDF', set_preset)
all_preset_btn = gp.Button(presets_cont, 'All files', set_preset)
clear_preset_btn = gp.Button(presets_cont, 'Clear all', set_preset)

# Log widgets
open_btn = gp.Button(log_cont, 'Open', start)
log = gp.Textbox(log_cont)
log.height = 4

# Window type
type_cont.set_grid(1, 3)
type_cont.set_column_weights(0, 0, 1)
type_cont.add(window_type_dd, 1, 1)
type_cont.add(title_lbl, 1, 2)
type_cont.add(title_inp, 1, 3, fill=True)

# Initial path
initial_cont.set_grid(2, 4)
initial_cont.set_column_weights(0, 0, 1, 0)
initial_cont.add(initial_folder_lbl, 1, 1)
initial_cont.add(initial_folder_dd, 1, 2)
initial_cont.add(paths_inp, 1, 3, fill=True)
initial_cont.add(initial_folder_btn, 1, 4)
initial_cont.add(initial_path_lbl, 2, 1)
initial_cont.add(initial_path_inp, 2, 2, column_span=2, fill=True)
initial_cont.add(initial_path_btn, 2, 4)

# Preset containers
presets_cont.set_grid(1, 6)
presets_cont.set_column_weights(0, 0, 0, 0, 0, 1)
presets_cont.add(preset_lbl, 1, 1)
presets_cont.add(image_presets_btn, 1, 2)
presets_cont.add(text_preset_btn, 1, 3)
presets_cont.add(pdf_preset_btn, 1, 4)
presets_cont.add(all_preset_btn, 1, 5)
presets_cont.add(clear_preset_btn, 1, 6, align='right')
presets_cont.margin_top = 20

# File types
filetypes_cont.set_grid(5, 3)
filetypes_cont.set_column_weights(0, 0, 1)
filetypes_cont.add(description_lbl, 1, 1)
filetypes_cont.add(description_inp, 1, 2)
filetypes_cont.add(all_extensions_list, 1, 3, row_span=3, fill=True, stretch=True)
filetypes_cont.add(extension_lbl, 2, 1)
filetypes_cont.add(extension_inp, 2, 2)
filetypes_cont.add(add_type_btn, 3, 2, fill=True)
filetypes_cont.add(presets_cont, 4, 1, column_span=3, fill=True)
filetypes_cont.add(multiple, 5, 1, column_span=3)

# Log
log_cont.set_grid(1, 2)
log_cont.set_column_weights(0, 1)
log_cont.add(open_btn, 1, 1)
log_cont.add(log, 1, 2, fill=True)

# All containers
app.set_grid(4, 1)
app.add(type_cont, 1, 1, fill=True)
app.add(initial_cont, 2, 1, fill=True)
app.add(filetypes_cont, 3, 1, fill=True)
app.add(log_cont, 4, 1, fill=True)

# Events
window_type_dd.add_event_listener('select', window_type_select)

app.run()
