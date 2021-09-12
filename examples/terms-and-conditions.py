import gooeypie as gp

def accept_terms(event):
    if accept_chk.checked:
        continue_btn.disabled = False
    else:
        continue_btn.disabled = True

app = gp.GooeyPieApp('Terms and Conditions')

terms_txt = gp.Textbox(app, 50, 10)
terms_txt.text = open('assets/license.txt').read()

accept_chk = gp.Checkbox(app, 'I have read and understand these conditions')
accept_chk.add_event_listener('change', accept_terms)

continue_btn = gp.Button(app, 'Continue', None)
continue_btn.disabled = True

app.set_grid(3, 1)
app.add(terms_txt, 1, 1)
app.add(accept_chk, 2, 1)
app.add(continue_btn, 3, 1, align='right')

app.run()