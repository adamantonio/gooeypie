import gooeypie as gp

app = gp.GooeyPieApp('Test')

# License container
license_container = gp.Container(app)

license_box_1 = gp.Input(license_container)
license_box_2 = gp.Input(license_container)
license_box_3 = gp.Input(license_container)
license_box_4 = gp.Input(license_container)
license_box_1.width = 5
license_box_2.width = 5
license_box_3.width = 5
license_box_4.width = 5

license_container.set_grid(1, 4)
license_container.add(license_box_1, 1, 1)
license_container.add(license_box_2, 1, 2)
license_container.add(license_box_3, 1, 3)
license_container.add(license_box_4, 1, 4)

# Buttons container
buttons_container = gp.Container(app)
register = gp.Button(buttons_container, 'Register', None)
cancel = gp.Button(buttons_container, 'Cancel', None)
buttons_container.set_grid(1, 2)
buttons_container.add(register, 1, 1)
buttons_container.add(cancel, 1, 2)

# Main window
app.set_grid(4, 3)

logo = gp.Image(app, './images/leaf.gif')
name_label = gp.Label(app, 'Name')
name = gp.Input(app)

company_label = gp.Label(app, 'Company name')
company = gp.Input(app)

license_label = gp.Label(app, 'License key')

app.add(logo, 1, 1, row_span=4)
app.add(name_label, 1, 2)
app.add(company_label, 2, 2)
app.add(license_label, 3, 2)
app.add(name, 1, 3, fill=True)
app.add(company, 2, 3, fill=True)
app.add(license_container, 3, 3)
app.add(buttons_container, 4, 3, valign='top')

app.set_row_weights(0, 0, 0, 1)

app.run()
