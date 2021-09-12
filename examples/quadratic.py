import gooeypie as gp

def solve(event):
    """Solves a quadratic equation using the quadratic formula"""
    a, b, c = a_num.value, b_num.value, c_num.value
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        answer_lbl.text = 'No solution! 😔'
    else:
        solution1 = (-b - discriminant**0.5) / (2 * a)
        solution2 = (-b + discriminant**0.5) / (2 * a)
        if solution1 == solution2:
            answer_lbl.text = f'x = {solution1}'  # 1 solution only
        else:
            answer_lbl.text = f'x = {solution1}, {solution2}'  # 2 solutions

app = gp.GooeyPieApp('Solve it')
equation_lbl = gp.StyleLabel(app, 'ax² + bx + c = 0')
equation_lbl.font_name = 'times'
equation_lbl.font_size = 16
equation_lbl.font_style = 'italic'

a_lbl = gp.Label(app, 'a =')
a_num = gp.Number(app, -10, 10)
a_num.value = 1
b_lbl = gp.Label(app, 'b =')
b_num = gp.Number(app, -10, 10)
b_num.value = 7
c_lbl = gp.Label(app, 'c =')
c_num = gp.Number(app, -10, 10)
c_num.value = 12

# Image from https://www.iconsdb.com/royal-blue-icons/math-icon.html
solve_btn = gp.ImageButton(app, 'images/maths.png', solve, 'Solve')
solve_btn.image_position = 'top'
answer_lbl = gp.Label(app, '')

app.set_grid(5, 3)
app.add(equation_lbl, 1, 1, column_span=3, align='center')
app.add(a_lbl, 2, 1)
app.add(a_num, 2, 2)
app.add(b_lbl, 3, 1)
app.add(b_num, 3, 2)
app.add(c_lbl, 4, 1)
app.add(c_num, 4, 2)
app.add(solve_btn, 2, 3, row_span=3, stretch=True)
app.add(answer_lbl, 5, 1, column_span=3, align='center')

app.run()