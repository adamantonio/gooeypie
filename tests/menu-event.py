import gooeypie as gp
from random import randint


def menu_select(event):
    # Make a 'breadcrumb' using the menu information from the event object
    menu_path = ' > '.join(event.menu)
    status.text = menu_path


def get_all():
    print(f"Selected item in Menu 2 is {app.get_menu_radio('Menu 2', ['Radio 1', 'Radio 2', 'Radio 3'])}")
    print(f"Selected item in Menu 2 -> Submenu 2 is {app.get_submenu_radio('Menu 2', 'Submenu 2', ['Radio 1', 'Radio 2', 'Radio 3'])}")
    print(f"Menu 3 -> Check 1 is {app.get_menu_checkbox('Menu 3', 'Check 1')}")
    print(f"Menu 3 -> Check 2 is {app.get_menu_checkbox('Menu 3', 'Check 2')}")
    print(f"Menu 3 -> Submenu 3 -> Check 1 is {app.get_submenu_checkbox('Menu 3', 'Submenu 3', 'Check 1')}")
    print()


def menu_top_state(event):
    if event.widget == enable_top:
        app.enable_menu(menu_inp.text)
    else:
        app.disable_menu(menu_inp.text)


def menu_item_state(event):
    if menu_item2_inp.text == '':
        if event.widget == enable_item:
            app.enable_menu_item(menu_name_inp.text, menu_item1_inp.text)
        else:
            app.disable_menu_item(menu_name_inp.text, menu_item1_inp.text)
    else:
        if event.widget == enable_item:
            app.enable_submenu_item(menu_name_inp.text, menu_item1_inp.text, menu_item2_inp.text)
        else:
            app.disable_submenu_item(menu_name_inp.text, menu_item1_inp.text, menu_item2_inp.text)


app = gp.GooeyPieApp('GooeyPie Menus')

menu_top_cont = gp.LabelContainer(app, 'Top level menu')
menu_item_cont = gp.LabelContainer(app, 'Menu items')

app.set_size(300, 100)

app.add_menu_item('Menu 1', 'Item 1', menu_select)
app.add_menu_item('Menu 1', 'Item 2', menu_select)
app.add_submenu_item('Menu 1', 'Submenu 1', 'Submenu Item 1', menu_select)
app.add_submenu_separator('Menu 1', 'Submenu 1')
app.add_submenu_item('Menu 1', 'Submenu 1', 'Submenu Item 2', menu_select)

app.add_menu_radios('Menu 2', ['Radio 1', 'Radio 2', 'Radio 3'], menu_select)
app.add_menu_separator('Menu 2')
app.add_submenu_radios('Menu 2', 'Submenu 2', ['Radio 1', 'Radio 2', 'Radio 3'], menu_select)

app.add_menu_checkbox('Menu 3', 'Check 1', menu_select)
app.add_menu_checkbox('Menu 3', 'Check 2', menu_select)
app.add_submenu_checkbox('Menu 3', 'Submenu 3', 'Check 1', menu_select)

app.set_menu_checkbox('Menu 3', 'Check 2', True)
app.set_submenu_radio('Menu 2', 'Submenu 2', ['Radio 1', 'Radio 2', 'Radio 3'], 'Radio 2')

status = gp.Label(app, 'Select a menu')

menu_inp = gp.Input(menu_top_cont)
enable_top = gp.Button(menu_top_cont, 'Enable', menu_top_state)
disable_top = gp.Button(menu_top_cont, 'Disable', menu_top_state)

menu_name_inp = gp.Input(menu_item_cont)
menu_item1_inp = gp.Input(menu_item_cont)
menu_item2_inp = gp.Input(menu_item_cont)
enable_item = gp.Button(menu_item_cont, 'Enable', menu_item_state)
disable_item = gp.Button(menu_item_cont, 'Disable', menu_item_state)

for input_widget in [menu_inp, menu_name_inp, menu_item1_inp, menu_item2_inp]:
    input_widget.width = 12

menu_top_cont.set_grid(1, 3)
menu_top_cont.set_column_weights(0, 0, 1)
menu_top_cont.add(menu_inp, 1, 1, valign='middle')
menu_top_cont.add(enable_top, 1, 2, valign='middle')
menu_top_cont.add(disable_top, 1, 3, valign='middle')

menu_item_cont.set_grid(1, 5)
menu_item_cont.add(menu_name_inp, 1, 1, valign='middle')
menu_item_cont.add(menu_item1_inp, 1, 2, valign='middle')
menu_item_cont.add(menu_item2_inp, 1, 3, valign='middle')
menu_item_cont.add(enable_item, 1, 4, valign='middle')
menu_item_cont.add(disable_item, 1, 5, valign='middle')

app.set_grid(3, 1)
app.add(status, 1, 1, align='center', stretch=True)
app.add(menu_top_cont, 2, 1, fill=True)
app.add(menu_item_cont, 3, 1, fill=True)

# Random values
menu_inp.text = f'Menu {randint(1, 3)}'
menu_name_inp.text = f'Menu {randint(1, 3)}'
menu_item1_inp.text = f'Submenu {randint(1, 3)}'
if randint(1, 3) > 1:
    menu_item2_inp.text = 'Radio '
else:
    menu_item2_inp.text = 'Check '
menu_item2_inp.text += str(randint(1, 3))

app.run()
