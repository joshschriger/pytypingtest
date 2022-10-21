# import tkinter as tk
from tkinter import *
import tkinter
import random
import time
import json
from tkinter import messagebox


# initializing variables

global pressed_once
global completed_game





#font = Font(family = 'roboto', weight = 'mono')

# creating the GUI
root = Tk()
root.geometry('936x464')
root.resizable(width=True, height=True)
root.minsize(width=725, height=400)
root.title("Typing Test")
root.iconbitmap('JS kbd Logo.ico')
root['background'] = '#121212'


# functions

def generate_words(word_dict, word_total):
    """
    Generate the word bank from the word dict
    """
    if test_type == 'Timed':
        word_total = word_total * 3
    word_bank = []*word_total
    for i in range(word_total):
        word_bank.append(random.choice(word_dict['words']))
    display_words(word_bank)


def display_words(word_bank):
    """
    Shows the word bank on the typing GUI
    """
    ' '.join(word_bank)
    to_type['text'] = word_bank


def start_action():
    """
    Starts the game and timer
    """
    completed_game = False
    pressed_once = False
    word_total = slider.get()
    entry_field.delete(1.0, 'end-1c')
    generate_words(word_dict, int(word_total))


def typing_test():
    """
    MAIN FUNCTION OF THE GAME
    """
    word_total = 30  # time/words default: 30 seconds
    # test_type = 'Timed'
    word_bank = 'To test your typing speed, press enter and start typing!'
    pressed_once = False
    completed_game = False
    word_total = slider.get()
    word_bank = to_type['text']
    time_start = time.time()
    if test_type == 'Words':
        root.update()
        while not completed_game:
            root.update()
            if (len(entry_field.get(1.0, 'end-1c')) >= len(word_bank)):
                time_end = time.time()
                completed_game = True
                pressed_once = False
                input = entry_field.get(1.0, 'end-1c')
                print(entry_field.get(1.0, 'end-1c'))
                print(word_bank)
                score_calculation(time_end-time_start, input)

    elif test_type == 'Timed':
        root.update()
        time.sleep(0.01)
        while not completed_game:
            root.update()
            if (int(time.time() - time_start) >= word_total):
                time_end = time.time()
                completed_game = True
                pressed_once = False
                input = entry_field.get(1.0, 'end-1c')
                score_calculation(word_total, input)


def enter_pressed(event):
    """
    When enter is pressed the word bank is reset
    """
    pressed_once = False
    start_action()


def score_calculation(timeTaken, input):
    """
    Calculates the score of the game
    """
    words_per_min = round(calculate_wpm(timeTaken, input), 2)
    word_bank = to_type['text']
    accuracy = round(calculate_accuracy(word_bank, input), 2)
    scores['text'] = str(words_per_min) + "\n" + str(accuracy) + "%"


def calculate_accuracy(word_bank, input):
    """
    Calculate the accuracy of the game
    """
    correct_keys = 0
    print (input)

    for i in range(input):
        print ("input:\t" + input[i])
        print ("word_bank:\t" + word_bank[i])
        # TODO fix this
    # for typed, word in input, word_bank:
    #     for letter in range(typed):
    #         if typed[letter] == word[z]:
    #             correct_keys += 1
    accuracy = correct_keys / len(input) * 100
    return accuracy


def calculate_wpm(time, input):
    """
    Calculate the words per minute of the game
    """
    words_per_min = (len(input)/5)/(time) * 60
    return words_per_min


def swaptest_type():
    """
    Swaps the test type between 'Timed' and 'Words'
    """
    global test_type
    if test_type == 'Words':
        test_typeButton['text'] = 'Timed'
        test_type = 'Timed'
    elif test_type:
        test_typeButton['text'] = 'Words'
        test_type = 'Words'


def key_pressed(event):
    """
    When a key is pressed the game starts
    """
    global pressed_once
    if to_type['text'] == 'To test your typing speed, press enter and start typing!':
        messagebox.showwarning(
            title='Error', message='You must generate a new word bank before testing\nTo do so, press enter or click the Start Game button')
        return 0
    if not pressed_once:
        pressed_once = True
        start_timer()


def start_timer():
    """
    Starts game's timer
    """
    time_start = time.time()
    typing_test()


# opening and reading word bank file
file_read = open(r"word_bank.json", encoding="utf8")
word_dict = json.load(file_read)
file_read.close()

# binding enter to start the game to negate the need to move the mouse while playing
root.bind('<Return>', enter_pressed)
root.bind('<Key>', key_pressed)

time_current = time.time()
words_per_min = 0.00
accuracy = 0.00

# creating widgets
title = Label(root, text='Typing Test', font=('Lucida Console',
              16), pady=10, bg='#121212', fg='White', width=30)
scoreText = Label(root, text="Words Per Minute =\nAccuracy =", font=(
    'Lucida Console', 8), bg='#121212', fg='White', justify=RIGHT, anchor=E, width=20)
scores = Label(root, text=str(words_per_min) + '\n' + str(accuracy) + '%', font=(
    'Lucida Console', 8), bg='#121212', fg='Red', justify=LEFT, anchor=W, width=10)

test_typeButton = Button(root, text=test_type, font=(
    'Lucida Console', 8), command=swaptest_type, bg='#333333', fg='White')

to_type = Label(root, text=word_bank, font=('Lucida Console', 16),
               wraplength=640, height=14, bg='#121212', fg='White')  # 246
slider = Scale(orient='vertical', from_=60, to=10, variable=word_total,
               length=250, width=20, bg='#333333', fg='White', troughcolor='#666666')


entry_field = Text(root, width=100, height=2, borderwidth=3, bg='#333333',
                  fg='White', font=('Lucida Console', 10), padx=1, pady=1)
startButton = Button(root, text='Start Game', font=(
    'Lucida Console', 8), command=start_action, bg='#333333', fg='White')

# placing widgets on the root window
# row 0
title.grid(row=0, column=0)
scoreText.grid(row=0, column=1)
scores.grid(row=0, column=2)
test_typeButton.grid(row=0, column=3)

# row 1
to_type.grid(row=1, column=0, pady=30, padx=10, columnspan=3)
slider.grid(row=1, column=3)
slider.set(30)

# row 2
entry_field.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
startButton.grid(row=2, column=3, padx=10)


root.mainloop()
