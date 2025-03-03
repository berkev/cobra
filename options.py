import time
import random 
import os
import sys
from pynput import keyboard
import msvcrt as kb
from playsound3 import playsound
from threading import Thread



#Sounds
GAMEOVER = "./sound/gameover.mp3"
EAT = "./sound/eat.mp3"
MUSIC ="./sound/music.mp3"


#Cursor
RESET = '\x1B[0m'
BLINK = '\x1B[5m'
ERASE = '\x1B[0J'+'\x1B[1J'
HOME = '\x1B[H'
MARK = '\x1B[7m'
HIDECURSOR = '\x1B[?25l'
CURSOR_UP = '\x1B[1A'
CURSOR_DOWN = '\x1B[1B'
CURSOR_RIGHT = '\x1B[1C'
CURSOR_LEFT = '\x1B[1D'


class Controls:
    UP = 'w'
    DOWN = 's'
    LEFT = 'a'
    RIGHT = 'd'
    SUBMIT = 'x'

#Symbols
BORDER='#'
COFFEE='\u2615'
FOOD = "\u263a"
HEAD='\u2620'

DIRECTIONS = [CURSOR_DOWN,CURSOR_RIGHT,CURSOR_UP,CURSOR_LEFT]

moves = {CURSOR_DOWN:{'x':0,'y':1},
        CURSOR_RIGHT:{'x':1,'y':0},
        CURSOR_UP:{'x':0,'y':-1},
        CURSOR_LEFT:{'x':-1,'y':0}
        }
moveList = [moves[dir] for dir in DIRECTIONS]