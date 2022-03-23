"""Notes

Required library updates before making this a public thing:
    + Padding
    + Get widget

Other thing to think about:
    + All of those early returns from guess()... bad? Maybe need to split those out

"""
import gooeypie as gp
import random

# Constants to represent the status of a guess
NOT_IN_WORD, IN_WORD, CORRECT = 0, 1, 2

current_guess = 1
target_word = ''
words = []

colours = {
    NOT_IN_WORD: 'Gray',
    IN_WORD: 'DarkGoldenRod',
    CORRECT: 'ForestGreen'
}


def wordle(target, guess_word):
    """Returns an array of 5 colours to indicate success or failure of guess"""
    target_list = list(target)
    guess_list = list(guess_word)
    answer_list = [NOT_IN_WORD] * 5

    # check for correct positions first
    for index in range(5):
        if guess_list[index] == target_list[index]:
            answer_list[index] = CORRECT
            target_list[index] = ''  # to avoid double letters
            guess_list[index] = ''

    # check for letters that are in the word
    for index in range(5):
        if guess_list[index] and guess_list[index] in target_list:
            answer_list[index] = IN_WORD
            target_list[target_list.index(guess_list[index])] = ''

    return answer_list


def load_words():
    """Word list from https://github.com/charlesreid1/five-letter-words/blob/master/sgb-words.txt"""
    for line in open('words.txt').readlines():
        words.append(line.strip().upper())


def set_target_word():
    """Loads the words"""
    global target_word
    target_word = random.choice(words)


def reset_game(event):
    global current_guess
    set_target_word()
    for row in range(6):
        for col in range(5):
            progress_cont._grid[row][col].text = '?'
            progress_cont._grid[row][col].colour = 'LightGray'
            progress_cont._grid[row][col].background_color = 'default'

    status_lbl.text = 'Good luck!'
    guess_btn.text = 'Guess'
    guess_inp.disabled = False
    guess_inp.text = ''
    guess_inp.focus()
    current_guess = 1


def guess(event):
    global current_guess

    if event.widget == guess_btn and guess_btn.text == 'Play again':
        reset_game(event)
        return

    if len(guess_inp.text) != 5:
        app.alert('Invalid guess', 'Your guess must have 5 letters', 'error')
        return

    guess_inp.text = guess_inp.text.upper()
    if guess_inp.text not in words:
        app.alert('Invalid guess', f'"{guess_inp.text}" not found in word list', 'error')
        guess_inp.select()
        return

    guess_result = wordle(target_word, guess_inp.text)
    for index in range(5):
        progress_cont._grid[current_guess - 1][index].text = guess_inp.text[index]
        progress_cont._grid[current_guess - 1][index].colour = 'white'
        progress_cont._grid[current_guess - 1][index].background_colour = colours[guess_result[index]]

    if guess_result == [CORRECT] * 5:
        status_lbl.text = 'You got it!'
        guess_inp.disabled = True
        guess_btn.text = 'Play again'
    elif current_guess == 6:
        status_lbl.text = f'Unlucky! The word was {target_word}'
        guess_inp.disabled = True
        guess_btn.text = 'Play again'
    else:
        current_guess += 1

    guess_inp.select()


def check_for_guess(event):
    if event.key['name'] == 'Return':
        guess(event)


app = gp.GooeyPieApp('WordlePy')
app.width = 250

app.add_menu_item('Game', 'Start over', reset_game)

progress_cont = gp.LabelContainer(app, 'Progress')

status_lbl = gp.Label(app, 'Good luck!')
progress_cont.set_grid(6, 5)

for row in range(6):
    for col in range(5):
        temp_lbl = gp.StyleLabel(progress_cont, '?')
        temp_lbl.font_name = 'Arial Black'
        temp_lbl.font_size = 14
        temp_lbl.width = 2
        temp_lbl.align = 'center'
        temp_lbl.colour = 'LightGray'
        temp_lbl.margins = [4, 4, 4, 4]
        progress_cont.add(temp_lbl, row + 1, col + 1)

guess_inp = gp.Input(app)
guess_inp.justify = 'center'
guess_inp.add_event_listener('key_press', check_for_guess)
guess_btn = gp.Button(app, 'Guess', guess)

app.set_grid(4, 1)
app.add(status_lbl, 1, 1, align='center')
app.add(progress_cont, 2, 1, align='center')
app.add(guess_inp, 3, 1, fill=True)
app.add(guess_btn, 4, 1, fill=True)

load_words()
set_target_word()

guess_inp.focus()

app.run()


# Good tests: HELLO, LEVEL
