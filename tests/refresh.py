"""Test file for refresh"""

import gooeypie as gp


def longer(event):
    if event.widget == longer_btn:
        test_lbl.text = 'This is a much longer label and it will be interesting to see if it can work to refresh the window'
    else:
        test_lbl.text = 'This text\nhas many different\nlines which also\nmakes a big difference'

    app.refresh()


def update_image(event):
    if test_img.image == 'logo.png':
        test_img.image = 'chart-icon.png'
    else:
        test_img.image = 'logo.png'

    app.refresh()


app = gp.GooeyPieApp('Refresh test')

# Tests to see if resizable makes a difference to programmatically change the window size
# app.set_resizable(False)
# app.resizable_horizontal = False

test_lbl = gp.Label(app, 'Short label')
test_img = gp.Image(app, 'chart-icon.png')

longer_btn = gp.Button(app, 'Longer label', longer)
newlines_btn = gp.Button(app, 'Label with newlines', longer)
image_btn = gp.Button(app, 'Change image', update_image)

app.set_grid(5, 1)
app.add(test_lbl, 1, 1)
app.add(test_img, 2, 1)
app.add(longer_btn, 3, 1)
app.add(newlines_btn, 4, 1)
app.add(image_btn, 5, 1)

app.run()
