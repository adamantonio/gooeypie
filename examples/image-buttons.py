import gooeypie as gp

app = gp.GooeyPieApp('Image buttons')

# Icons from iconsdb.com
audio_btn = gp.ImageButton(app, 'images/headphones-24.png', None, 'Test audio')
save_btn = gp.ImageButton(app, 'images/save-24.png', None)
save_btn.set_padding(80, 20)
logout_btn = gp.ImageButton(app, 'images/logout-24.png', None, 'Sign Out')
logout_btn.image_position = 'top'
logout_btn.set_padding(0, 10)

app.set_grid(1, 3)
app.add(audio_btn, 1, 1, valign='middle')
app.add(save_btn, 1, 2, valign='middle')
app.add(logout_btn, 1, 3, valign='middle')

app.run()
