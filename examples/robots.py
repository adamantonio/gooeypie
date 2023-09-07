import gooeypie as gp

def select_robot(event):
    # Robot images from robohash.org - images are named robot1.png, robot2.png etc.
    avatar.image = f'images/robot{select_sld.value}.png'

app = gp.GooeyPieApp('Customise your avatar')
app.width = 350

select_sld = gp.Slider(app, 1, 5, 'vertical')
select_sld.value = 1
select_sld.add_event_listener('change', select_robot)

avatar = gp.Image(app, 'images/robot1.png')

app.set_grid(1, 2)
app.add(select_sld, 1, 1, stretch=True)
app.add(avatar, 1, 2)

app.run()