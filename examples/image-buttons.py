import gooeypie as gp

app = gp.GooeyPieApp('Image buttons')
app.set_grid(1, 3)

def test_popup(event):
    app.error_dialog('Cannot generate password, wow this is a long title will you see it', 'you need to do better.\n\nPlease try')

def test_exit(event):
    app.exit()

# Icons from iconsdb.com
audio_button = gp.ImageButton(app, 'images/headphones-24.png', test_popup, 'Test audio')
save_button = gp.ImageButton(app, 'images/save-24.png', test_exit)
logout_button = gp.ImageButton(app, 'images/logout-24.gif', None, 'Sign Out')
logout_button.image_position = 'top'

app.add(audio_button, 1, 1, valign='middle')
app.add(save_button, 1, 2, valign='middle')
app.add(logout_button, 1, 3)

app.run()
