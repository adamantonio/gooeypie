import gooeypie as gp

def accept_terms(event):
    if accept.checked:
        continue_button.disabled = False
    else:
        continue_button.disabled = True

app = gp.GooeyPieApp('Terms and Conditions')

terms = gp.Textbox(app, 50, 10)
terms.text = open('assets/license.txt').read()
terms.width = 100

accept = gp.Checkbox(app, 'I have read and understand these conditions')
accept.add_event_listener('change', accept_terms)

continue_button = gp.Button(app, 'Continue', None)
continue_button.disabled = True

app.set_grid(3, 1)
app.add(terms, 1, 1, fill=True)
app.add(accept, 2, 1)
app.add(continue_button, 3, 1, align='right')

app.run()