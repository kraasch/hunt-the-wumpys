#!/usr/bin/python3

import sys
import random
import readchar

# TODO: distribute random arrow 'a', increase arrow count on collision.

#visibleMode = True
visibleMode = False

arrows=0
grid = []

grid.append(['_', '_', '_', '_', '_'])
grid.append(['_', '_', '_', '_', '_'])
grid.append(['_', '_', '_', '_', '_'])
grid.append(['_', '_', '_', '_', '_'])
grid.append(['_', '_', '_', '_', '_'])

y=(int)(random.random()*5)
x=(int)(random.random()*5)
grid[y][x] = 'x'

def findSpotX():
    global x,y
    char='x'
    xx=0
    yy=0
    while True:
        xx=(int)(random.random()*5) 
        yy=(int)(random.random()*5) 
        now = grid[yy][xx]
        if (now == '_' or now == '-'):
            break
    grid[yy][xx] = char
    x=xx
    y=yy

def findSpot(char):
    xx=0
    yy=0
    while True:
        xx=(int)(random.random()*5) 
        yy=(int)(random.random()*5) 
        now = grid[yy][xx]
        if (now == '_'):
            break
    grid[yy][xx] = char

findSpot('w')
findSpot('h')
findSpot('b')
findSpot('a')

messages=[]

def printCell(i, j):
    content = grid[i][j]
    if visibleMode:
        # print all
        print(content, end='')
    else:
        # don't show wumpus, bats, hole, arrows.
        if content == 'w' or content == 'b' or content == 'h' or content == 'a':
            print('_', end='')
        else:
            print(content, end='')

def printGrid():
    for i in range(0, 5):
        print('|', end='')
        for j in range(0, 5):
            printCell(i, j)
        print('|', end='')
        print()

def addMessage(x, y):
    if grid[y][x]=='w':
        messages.append('You smell wumpus.')
    elif grid[y][x]=='b':
        messages.append('You hear flapping.')
    elif grid[y][x]=='h':
        messages.append('You feel a draft.')

def printMessages():
    global messages
    for i in range(-1, 2):
        for j in range(-1, 2):
            xx=x+i
            yy=y+j
            if canStep(x, y, i, j) and (i!=0 or j!=0):
                addMessage(xx, yy)
    for msg in messages:
        print(' ' + msg)

def canStep(x, y, xdir, ydir):
    newX = x+xdir
    newY = y+ydir
    return newX>=0 and newY>=0 and newX<=4 and newY<=4 

def doStep(xx, yy, xdir, ydir):
    global x,y,arrows,messages
    grid[yy][xx]='-'
    x=xx+xdir
    y=yy+ydir
    if grid[y][x]=='w':
        print('Wumpus eats you.')
        sys.exit()
    elif grid[y][x]=='b':
        print('Bats carry you away.')
        findSpotX()
    elif grid[y][x]=='h':
        print('You fall into a hole.')
        sys.exit()
    elif grid[y][x]=='a':
        messages.append('You found an arrow.')
        arrows=arrows+1
        grid[y][x]='x'
    else:
        grid[y][x]='x'

def doShoot(xx, yy, xdir, ydir):
    global x,y,arrows
    if not (arrows >= 1):
        print('You have no arrows.')
    else:
        arrows=arrows-1
        if grid[yy+ydir][xx+xdir]=='w':
            print('You shoot the wumpus.')
            sys.exit()
        else:
            print('You miss.')

def shoot(xdir, ydir):
    global x,y
    if (canStep(x, y, xdir, ydir)):
        doShoot(x, y, xdir, ydir)

def step(xdir, ydir):
    global x,y
    if (canStep(x, y, xdir, ydir)):
        doStep(x, y, xdir, ydir)

def readInput():
    key = readchar.readkey()
    return key

def evaluateInput(k):

    if k == 'q' or k == 'Q':
        sys.exit()

    elif k=='\x1b[A' or k=='k':
        step(0, -1)
    elif k=='\x1b[B' or k=='j':
        step(0, 1)
    elif k=='\x1b[C' or k=='l':
        step(1, 0)
    elif k=='\x1b[D' or k=='h':
        step(-1, 0)

    elif k=='w' or k=='K':
        shoot(0, -1)
    elif k=='s' or k=='J':
        shoot(0, 1)
    elif k=='d' or k=='L':
        shoot(1, 0)
    elif k=='a' or k=='H':
        shoot(-1, 0)

def flushAndPrint():
    print(chr(27) + "[2J")
    print('\n' * 20)
    printMessages()
    print('+-----+')
    printGrid()
    print('+-----+')
    print( "q           - quit.")
    print( "arrow keys  - walk.")
    print( "wasd        - shoot.")
    print(f"arrows left : {arrows}")

flushAndPrint()
while True:
    messages=[]
    data = readInput()
    evaluateInput(data)
    flushAndPrint()

