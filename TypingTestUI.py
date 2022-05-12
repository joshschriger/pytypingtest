from tkinter import *

root = Tk()


def startClick():
   startLabel = Label(root, text='Button Clicked!')
   startLabel.pack()

#creating label widget
#myLabel1 = Label(root, text = 'Hello World')
#myLabel2 = Label(root, text = 'My name is Josh Schriger')
myButton = Button(root, text = 'Start Game', command=startClick, fg='white', bg='gray')

#shoving it onto the screen
#myLabel1.grid(row = 0, column = 0)
#myLabel2.grid(row = 1, column = 1)
myButton.pack()

root.mainloop()
