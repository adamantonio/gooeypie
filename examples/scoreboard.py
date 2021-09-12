import gooeypie as gp

# Dictionary to hold the score
score = {'HOME': 0, 'AWAY': 0}

def update_score(event):
    team = event.widget.text  # The label text is also the score dict key
    score[team] += 1
    score_lbl.text = f' {score["HOME"]} - {score["AWAY"]} '

app = gp.GooeyPieApp('Scoreboard')

score_lbl = gp.StyleLabel(app, ' 0 - 0 ')
score_lbl.font_name = 'Courier'
score_lbl.font_weight = 'bold'
score_lbl.background_color = 'black'
score_lbl.font_size = 60
score_lbl.colour = 'red'

home_lbl = gp.Label(app, 'HOME')
away_lbl = gp.Label(app, 'AWAY')
home_lbl.add_event_listener('mouse_down', update_score)
away_lbl.add_event_listener('mouse_down', update_score)

app.set_grid(2, 2)
app.add(score_lbl, 1, 1, column_span=2)
app.add(home_lbl, 2, 1, align='center')
app.add(away_lbl, 2, 2, align='center')

app.run()
