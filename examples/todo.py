import gooeypie as gp


def delete(event):
    todos.remove_selected()
    todos.select_none()
    new_todo.focus()


def add(event):
    todos.add_item(new_todo.text)
    new_todo.clear()
    new_todo.focus()


app = gp.GooeyPieApp('Quick todo')
app.width = 250
new_todo = gp.Input(app)
add_btn = gp.Button(app, '+', add)
add_btn.width = 3
todos = gp.Listbox(app, ['Exercise', 'Eat a piece of fruit'])
todos.height = 5
todos.add_event_listener('double_click', delete)
instructions = gp.StyleLabel(app, 'Double-click to remove a todo')
instructions.font_size = 8
instructions.margin_top = 0

app.set_grid(3, 2)
app.set_column_weights(1, 0)
app.add(new_todo, 1, 1, valign='middle', fill=True)
app.add(add_btn, 1, 2)
app.add(todos, 2, 1, column_span=2, fill=True)
app.add(instructions, 3, 1, column_span=2, align='center')

app.run()



