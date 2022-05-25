from tkinter import *
from tkinter import messagebox
from tkinter import font
import random
import time
import json


# initializing variables

global pressedOnce
global completedGame

wordTotal = 30  # time/words default: 30 seconds
testType = 'Timed'
wordBank = 'To test your typing speed, press enter and start typing!'
pressedOnce = False
completedGame = False
timeStart = 0
timeEnd = 0


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

def generateWords(wordDict, wordTotal):
    if testType == 'Timed':
        wordTotal = wordTotal * 3
    wordBank = []*wordTotal
    for i in range(int(wordTotal)):
        wordBank.append(random.choice(wordDict['words']))
    displayWords(wordBank)


def displayWords(wordBank):
    ' '.join(wordBank)
    toType['text'] = wordBank


def startAction():
    global completedGame
    completedGame = False
    pressedOnce = False
    wordTotal = slider.get()
    entryField.delete(1.0, 'end-1c')
    generateWords(wordDict, int(wordTotal))


def typingTest():
    global completedGame
    global pressedOnce
    wordTotal = slider.get()
    wordBank = toType['text']
    if testType == 'Words':
        root.update()
        while not completedGame:
            root.update()
            if (len(entryField.get(1.0, 'end-1c')) >= len(wordBank)):
                timeEnd = time.time()
                completedGame = True
                pressedOnce = False
                input = entryField.get(1.0, 'end-1c')
                print(entryField.get(1.0, 'end-1c'))
                print(wordBank)
                scoreCalculation(timeEnd-timeStart, input)

    elif testType == 'Timed':
        root.update()
        time.sleep(0.01)
        while not completedGame:
            root.update()
            if (int(time.time() - timeStart) >= wordTotal):
                timeEnd = time.time()
                completedGame = True
                pressedOnce = False
                input = entryField.get(1.0, 'end-1c')
                scoreCalculation(wordTotal, input)


def enterPressed(event):
    pressedOnce = False
    startAction()


def scoreCalculation(timeTaken, input):
    wordsPerMin = round(calculateWpm(timeTaken, input), 2)
    wordBank = toType['text']
    accuracy = round(calculateAccuracy(wordBank, input), 2)
    scores['text'] = str(wordsPerMin) + "\n" + str(accuracy) + "%"


def calculateAccuracy(wordBank, input):
    correctKeys = 0
    print (len(input))
    for i in range(len(input)):
        if input[i] == wordBank[i]:
            correctKeys += 1
    accuracy = correctKeys / len(input) * 100
    return accuracy


def calculateWpm(time, input):
    wordsPerMin = (len(input)/5)/(time) * 60
    return wordsPerMin


def swapTestType():
    global testType
    if testType == 'Words':
        testTypeButton['text'] = 'Timed'
        testType = 'Timed'
    elif testType:
        testTypeButton['text'] = 'Words'
        testType = 'Words'


def keyPressed(event):
    global pressedOnce
    if toType['text'] == 'To test your typing speed, press enter and start typing!':
        messagebox.showwarning(
            title='Error', message='You must generate a new word bank before testing\nTo do so, press enter or click the Start Game button')
        return 0
    if not pressedOnce:
        pressedOnce = True
        startTimer()


def startTimer():
    global timeStart
    timeStart = time.time()
    typingTest()


# opening and reading word bank file
fileRead = open(r"word_bank.json")
wordDict = json.load(fileRead)
fileRead.close

# binding enter to start the game to negate the need to move the mouse while playing
root.bind('<Return>', enterPressed)
root.bind('<Key>', keyPressed)

timeCurrent = time.time()
wordsPerMin = 0.00
accuracy = 0.00

# creating widgets
title = Label(root, text='Typing Test', font=('Lucida Console',
              16), pady=10, bg='#121212', fg='White', width=30)
scoreText = Label(root, text="Words Per Minute =\nAccuracy =", font=(
    'Lucida Console', 8), bg='#121212', fg='White', justify=RIGHT, anchor=E, width=20)
scores = Label(root, text=str(wordsPerMin) + '\n' + str(accuracy) + '%', font=(
    'Lucida Console', 8), bg='#121212', fg='Red', justify=LEFT, anchor=W, width=10)

testTypeButton = Button(root, text=testType, font=(
    'Lucida Console', 8), command=swapTestType, bg='#333333', fg='White')

toType = Label(root, text=wordBank, font=('Lucida Console', 16),
               wraplength=640, height=14, bg='#121212', fg='White')  # 246
slider = Scale(orient='vertical', from_=60, to=10, variable=wordTotal,
               length=250, width=20, bg='#333333', fg='White', troughcolor='#666666')


entryField = Text(root, width=100, height=2, borderwidth=3, bg='#333333',
                  fg='White', font=('Lucida Console', 10), padx=1, pady=1)
startButton = Button(root, text='Start Game', font=(
    'Lucida Console', 8), command=startAction, bg='#333333', fg='White')

# placing widgets on the root window
# row 0
title.grid(row=0, column=0)
scoreText.grid(row=0, column=1)
scores.grid(row=0, column=2)
testTypeButton.grid(row=0, column=3)

# row 1
toType.grid(row=1, column=0, pady=30, padx=10, columnspan=3)
slider.grid(row=1, column=3)
slider.set(30)

# row 2
entryField.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
startButton.grid(row=2, column=3, padx=10)


root.mainloop()
