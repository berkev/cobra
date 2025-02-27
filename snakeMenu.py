from options import *
import snake



sys.stdout.write(ERASE + HOME +HIDECURSOR)
w,h = os.get_terminal_size()

ACTIONS =["Start","Exit"]
BOX = ((w - max(map(len,ACTIONS)))//2,(h-len(ACTIONS))//2)
state = 0
on = True
running = False




def setChoice(list,index):
    choice = list.copy()
    choice[index] = MARK+choice[index]+RESET+HIDECURSOR
    return choice
def draw(list):
    for i in range(0,len(list)):
        sys.stdout.write(HOME)
        sys.stdout.write(CURSOR_DOWN*(BOX[1]+i)+CURSOR_RIGHT*(BOX[0]))
        sys.stdout.write(list[i])
        sys.stdout.flush()
def drawWinningScreen(win,score):
    draw(ACTIONS)
    sys.stdout.write(HOME)
    sys.stdout.write(CURSOR_DOWN*(BOX[1]-2)+CURSOR_RIGHT*(BOX[0]))
    if win:
        sys.stdout.write("YOU WON")
    else:
        sys.stdout.write("YOU LOST")
    sys.stdout.write("Score: "+str(score))


def update(list,index):
    sys.stdout.write(ERASE+HOME)
    draw(setChoice(list,index))
    return index
def pressHandler(key):
    global state
    match str(key):
        case "'w'": 
            update(ACTIONS,0)
            state = 0
        case "'s'":
            update(ACTIONS,1)
            state = 1
        case "'x'":
            sys.stdout.write(ERASE+HOME)
            commands[state]()
        case default:
            pass

draw(ACTIONS)

def start():
    global running
    if not running:
        running = True
        game = snake.snake()
        (win,score) = game.newGame(w=80,h=20,x=w//2-40,y=h//2-10)
        running = afterGame(win,score)

def afterGame(win,score):
    draw(ACTIONS)
    drawWinningScreen(win,score)
    return False

def exit():

    global on
    on = False
    
commands = [start,exit]
# The event listener will be running in this block

with keyboard.Events() as events:
    #musicThread = playsound(MUSIC,False,daemon=True)
    for event in events:
        if isinstance(event,keyboard.Events.Press):
            if event and event.key == keyboard.Key.esc:
                sys.stdin.flush()
                break
            else:
                pressHandler(event.key)
                events = []
                if not on:
                    break