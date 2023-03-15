# Questions for video:
#     Will it rain tomorrow?
#     Will my team win this weekend?
#     ?
#

import gooeypie as gp
from random import choice
import time

responses = ['It is certain.', 'It is decidedly so.', 'Without a doubt.',
             'As I see it, yes.', 'Most likely.', 'Outlook good.',
             'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
             'Don\'t count on it.', 'My reply is no.', 'My sources say no.'
             ]

def ask(event):
    thinking_pb.value = 0
    answer_lbl.text = ''
    for steps in range(20):
        thinking_pb.value += 5
        app.refresh()
        time.sleep(0.02)
    answer_lbl.text = choice(responses)
    question_inp.focus()


app = gp.GooeyPieApp('Magic 8 Ball')

question_inp = gp.Input(app)
question_inp.width = 50
ask_btn = gp.Button(app, 'Ask', ask)
thinking_pb = gp.Progressbar(app)
answer_lbl = gp.StyleLabel(app, '')
answer_lbl.font_size = 20
answer_lbl.align = 'center'

app.set_grid(3, 2)
app.set_column_weights(1, 0)
app.add(question_inp, 1, 1, valign='middle')
app.add(ask_btn, 1, 2, valign='middle')
app.add(thinking_pb, 2, 1, column_span=2, fill=True)
app.add(answer_lbl, 3, 1, column_span=2, fill=True)

app.run()
