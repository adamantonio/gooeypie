import gooeypie as gp


def start(event):
    file_name = open_images_win.open()
    if file_name:
        print(open(file_name).read())


app = gp.GooeyPieApp('Opening files')
app.set_size(400, 200)
open_images_win = gp.OpenFileWindow(app, 'Open stuff')
open_images_win.initial_path = "c:\\"
open_images_win.add_file_type("Text files", "*.txt *.log")
# open_images_win.add_file_type("Log files", "*.log")


test_btn = gp.Button(app, 'Test', start)

app.set_grid(1, 1)
app.add(test_btn, 1, 1, align='center', valign='middle')

app.run()
