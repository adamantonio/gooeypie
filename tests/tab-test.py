import gooeypie as gp
from random import choice

app = gp.GooeyPieApp('Tab tests')


def toggle_lock(e):
    if not checker_tab.disabled:
        checker_tab.disabled = False
        checker_tab.select()
        checker_tab.icon = 'unlocked-green.png'
    else:
        checker_tab.disabled = True
    print(testing_tab_container.width)
    print(testing_tab_container.height)


def tab_container_state(event):
    if event.widget.text == 'Enable':
        testing_tab_container.disabled = False
    elif event.widget.text == 'Disable':
        testing_tab_container.disabled = True
    elif event.widget.text == 'Get state':
        log.prepend_line(f'Tab container state: {testing_tab_container.disabled=}')


def get_tabs(event):
    log.prepend_line(testing_tab_container.tabs())


def selected_tab(event):
    log.prepend_line(f'Selected tab is {repr(testing_tab_container.selected)}')


def select_tab(event):
    select_tab_name = all_tabs_dd.selected
    tabs[select_tab_name].select()
    log.prepend_line(f'{select_tab_name} tab selected')


def visibility(event):
    select_tab_name = all_tabs_dd.selected
    if event.widget.text.lower() == 'show':
        tabs[select_tab_name].show()
        status = 'unhidden'
    else:
        tabs[select_tab_name].hide()
        status = 'hidden'

    log.prepend_line(f'{select_tab_name} tab {status}')


def tab_state(event):
    select_tab_name = all_tabs_dd.selected
    if event.widget.text.lower() == 'get state':
        if tabs[select_tab_name].disabled:
            state = 'disabled'
        else:
            state = 'enabled'
        log.prepend_line(f'{select_tab_name} is {state}')

    elif event.widget.text.lower() == 'disable':
        tabs[select_tab_name].disabled = True
        log.prepend_line(f'Disabled {select_tab_name}')

    elif event.widget.text.lower() == 'enable':
        tabs[select_tab_name].disabled = False
        log.prepend_line(f'Enabled {select_tab_name}')

    elif event.widget.text.lower() == 'toggle':
        tabs[select_tab_name].disabled = not tabs[select_tab_name].disabled
        log.prepend_line(f'Toggled state of {select_tab_name}')

    elif event.widget.text.lower() == 'disable contents':
        tabs[select_tab_name].disable_contents()
        log.prepend_line(f'Disabled contents of {select_tab_name} tab')

    elif event.widget.text.lower() == 'enable contents':
        tabs[select_tab_name].enable_contents()
        log.prepend_line(f'Enabled contents of {select_tab_name} tab')


def tab_icon(event):
    select_tab_name = all_tabs_dd.selected
    if event.widget.text.lower() == 'get icon':
        log.prepend_line(f'Icon for {select_tab_name} tab is {tabs[select_tab_name].icon}')

    elif event.widget.text.lower() == 'remove icon':
        tabs[select_tab_name].icon = None
        log.prepend_line(f'Removed icon for {select_tab_name}')

    elif event.widget.text.lower() == 'random icon':
        icon = choice(['locked-red.png', 'key-orange.png', 'unlocked-green.png'])
        tabs[select_tab_name].icon = icon
        log.prepend_line(f'Changed icon for {select_tab_name} to {icon}')


# Create containers
testing_tab_container = gp.TabContainer(app)
tab_container_tests_cont = gp.LabelContainer(app, 'Container tests')
tab_tests_cont = gp.LabelContainer(app, 'Tab tests')
log_cont = gp.LabelContainer(app, 'Log')

# Login tab
login_tab = gp.Tab(testing_tab_container, 'Login', 'locked-red.png')
username_lbl = gp.Label(login_tab, 'Username')
username_inp = gp.Input(login_tab)
password_lbl = gp.Label(login_tab, 'Password')
password_inp = gp.Input(login_tab)
login_btn = gp.Button(login_tab, 'Log in', None)

login_tab.set_grid(3, 2)
login_tab.add(username_lbl, 1, 1)
login_tab.add(username_inp, 1, 2)
login_tab.add(password_lbl, 2, 1)
login_tab.add(password_inp, 2, 2)
login_tab.add(login_btn, 3, 2)

# Set up password generator tab
generator_tab = gp.Tab(testing_tab_container, 'Generator', 'key-orange.png')
generator_instructions_lbl = gp.Label(generator_tab, 'Set your desired password length using the slider')
length_slider = gp.Slider(generator_tab, 4, 30)
generated_password_inp = gp.Input(generator_tab)
generated_password_inp.justify = 'center'
copy_password_btn = gp.Button(generator_tab, 'Copy to clipboard', None)

generator_tab.set_grid(4, 1)
generator_tab.set_row_weights(0, 0, 0, 1)
generator_tab.add(generator_instructions_lbl, 1, 1)
generator_tab.add(length_slider, 2, 1, fill=True)
generator_tab.add(generated_password_inp, 3, 1, fill=True)
generator_tab.add(copy_password_btn, 4, 1, align='center')

# Set up Password checker tab
checker_tab = gp.Tab(testing_tab_container, 'Checker', 'locked-red.png')
check_password_instructions_lbl = gp.Label(checker_tab, 'Enter your password to check')
check_password_inp = gp.Input(checker_tab)
check_password_btn = gp.Button(checker_tab, 'Check', None)
check_password_report_lbl = gp.Label(checker_tab, '\n\n\n')

checker_tab.set_grid(3, 2)
checker_tab.set_column_weights(1, 0)
checker_tab.set_row_weights(0, 0, 1)
checker_tab.add(check_password_instructions_lbl, 1, 1, column_span=2)
checker_tab.add(check_password_inp, 2, 1, fill=True, stretch=True)
checker_tab.add(check_password_btn, 2, 2)
checker_tab.add(check_password_report_lbl, 3, 1, column_span=2)

# About tab
about_tab = gp.Tab(testing_tab_container, 'About')
logo_img = gp.Image(about_tab, 'logo.png')
about_lbl = gp.Label(about_tab, '© GooeyPie')

about_tab.set_grid(2, 1)
about_tab.set_row_weights(1, 1)
about_tab.add(logo_img, 1, 1, align='center', valign='bottom')
about_tab.add(about_lbl, 2, 1, align='center', valign='top')

# Add tabs to tab container
testing_tab_container.add(login_tab)
testing_tab_container.add(generator_tab)
testing_tab_container.add(checker_tab)
testing_tab_container.add(about_tab)


# Tab container tests

# State
state_cont = gp.Container(tab_container_tests_cont)
enable_tab_container_btn = gp.Button(state_cont, 'Enable', tab_container_state)
disable_tab_container_btn = gp.Button(state_cont, 'Disable', tab_container_state)
state_tab_container_btn = gp.Button(state_cont, 'Get state', tab_container_state)
get_selected_btn = gp.Button(state_cont, 'Selected', selected_tab)
get_tabs_btn = gp.Button(state_cont, 'Get tabs', get_tabs)

state_cont.set_grid(1, 5)
state_cont.add(enable_tab_container_btn, 1, 1)
state_cont.add(disable_tab_container_btn, 1, 2)
state_cont.add(state_tab_container_btn, 1, 3)
state_cont.add(get_selected_btn, 1, 4)
state_cont.add(get_tabs_btn, 1, 5)

tab_container_tests_cont.set_grid(1, 1)
tab_container_tests_cont.add(state_cont, 1, 1)

# Tab tests
tabs = {
    'Login': login_tab,
    'Password generator': generator_tab,
    'Password checker': checker_tab,
    'About': about_tab
}

selected_tab_cont = gp.Container(tab_tests_cont)
all_tabs_dd = gp.Dropdown(selected_tab_cont, list(tabs.keys()))
all_tabs_dd.selected_index = 0
select_tab_btn = gp.Button(selected_tab_cont, 'Select', select_tab)
hide_tab_btn = gp.Button(selected_tab_cont, 'Hide', visibility)
show_tab_btn = gp.Button(selected_tab_cont, 'Show', visibility)
get_state_btn = gp.Button(selected_tab_cont, 'Get state', tab_state)
disable_tab_btn = gp.Button(selected_tab_cont, 'Disable', tab_state)
enable_tab_btn = gp.Button(selected_tab_cont, 'Enable', tab_state)
toggle_state_tab_btn = gp.Button(selected_tab_cont, 'Toggle', tab_state)
disable_tab_contents_btn = gp.Button(selected_tab_cont, 'Disable contents', tab_state)
enable_tab_contents_btn = gp.Button(selected_tab_cont, 'Enable contents', tab_state)
get_icon_btn = gp.Button(selected_tab_cont, 'Get icon', tab_icon)
remove_icon_btn = gp.Button(selected_tab_cont, 'Remove icon', tab_icon)
random_icon_btn = gp.Button(selected_tab_cont, 'Random icon', tab_icon)


selected_tab_cont.set_grid(4,6)
selected_tab_cont.add(all_tabs_dd, 1, 1, column_span=3)
selected_tab_cont.add(select_tab_btn, 2, 1)
selected_tab_cont.add(hide_tab_btn, 2, 2)
selected_tab_cont.add(show_tab_btn, 2, 3)
selected_tab_cont.add(get_state_btn, 3, 1)
selected_tab_cont.add(disable_tab_btn, 3, 2)
selected_tab_cont.add(enable_tab_btn, 3, 3)
selected_tab_cont.add(toggle_state_tab_btn, 3, 4)
selected_tab_cont.add(disable_tab_contents_btn, 3, 5)
selected_tab_cont.add(enable_tab_contents_btn, 3, 6)
selected_tab_cont.add(get_icon_btn, 4, 1)
selected_tab_cont.add(remove_icon_btn, 4, 2)
selected_tab_cont.add(random_icon_btn, 4, 3)

tab_tests_cont.set_grid(1, 1)
tab_tests_cont.add(selected_tab_cont, 1, 1)

# Log
log = gp.Textbox(log_cont)

log_cont.set_grid(1, 1)
log_cont.add(log, 1, 1, fill=True, stretch=True)

app.set_grid(4, 1)
app.add(testing_tab_container, 1, 1, fill=True, stretch=True)
app.add(tab_container_tests_cont, 2, 1, fill=True)
app.add(tab_tests_cont, 3, 1, fill=True)
app.add(log_cont, 4, 1, fill=True)

app.run()

