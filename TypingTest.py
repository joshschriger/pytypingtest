from ast import For
from asyncio.windows_events import NULL
from ctypes import sizeof
import random
import time


with open(r'C:\Users\schri\Documents\PersonalCodingProjects\Python\TypingTest\word_bank.txt') as words:
   wordLine = words.read()





wordLine = wordLine.replace(',', '')
wordArray = wordLine.split()
randomWords = []
# for x in wordArray:
#    print(x)
timeout = 30
timeoutStart = time.time()
x = 0

for i in range(10):
   randomWords[i] = wordArray[random.randrange(0, len(wordArray) - 1)]






time.sleep(1)

while time.time() < timeoutStart + timeout:
   print(randomWords)


print("time reached 30 seconds")
   
