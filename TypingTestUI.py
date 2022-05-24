from tkinter import *
from tkinter import messagebox
import pyglet
import random
import time
import json


# initializing variables

global pressedOnce
global completedGame

wordTotal = 30  # time/words default: 30 seconds
testType = 'Timed'
wordBank = 'Text that needs to be typed will be here'
wordInput = ''
pressedOnce = False
completedGame = False
timeStart = 0
timeEnd = 0

# creating the GUI
root = Tk()
root.geometry('725x400')
root.resizable(width=False, height=True)
root.minsize(width=725, height=400)
root.title("Typing Test")
root.iconbitmap('JS kbd Logo.ico')


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
    entryField.delete(0, END)
   #  if valWordTotal():
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
            if (len(entryField.get()) >= len(wordBank)):
                timeEnd = time.time()
                completedGame = True
                pressedOnce = False
                input = entryField.get()
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
                input = entryField.get()
                scoreCalculation(wordTotal, input)


def enterPressed(event):
    startAction()


def scoreCalculation(timeTaken, input):
    wordsPerMin = round(calculateWpm(timeTaken, input), 2)
    messagebox.showinfo("Scores", "Words Per Minute: " + str(wordsPerMin))
    prevWpmText['text'] = "Previous WPM = " + str(wordsPerMin)


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


def errorPopup(message):
    messagebox.showerror("Error", message)


def keyPressed(event):
    global pressedOnce
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
wordsPerMin = 0

# creating widgets
prevWpmText = Label(root, text="Previous WPM = " + str(wordsPerMin), width=20)
title = Label(root, text='Typing Test', pady=10, font=('Arial', 16))
testTypeButton = Button(root, text=testType, command=swapTestType)

toType = Label(root, text=wordBank, wraplength=512,
               font=('Arial', 16), height=10)  # 246
slider = Scale(orient='vertical', from_=60, to=10, variable=wordTotal, length = 250, width = 20)


entryField = Entry(root, width=100, borderwidth=3)
startButton = Button(root, text='Start Game',
                     command=startAction, fg='white', bg='gray')

# placing widgets on the root window
# row 0
prevWpmText.grid(row=0, column=0)
title.grid(row=0, column=1)
testTypeButton.grid(row=0, column=2)

# row 1
toType.grid(row=1, column=0, pady=30, padx=10, columnspan=2)
slider.grid(row=1, column=2)
slider.set(30)

# row 2
entryField.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
startButton.grid(row=2, column=2, padx=10)


root.mainloop()
