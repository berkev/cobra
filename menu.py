from options import *
import snake


class Map:
    def __init__(self,w,h,x,y):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

class menu:
    # Implements a traversable menu.
    # Keybinding: 'w': Move up 's': move down, 
    #             'x': choose option
    def __init__(self,width,height):
        self.w = width
        self.h = height
        self.actions = {"Start":self.start,"Music":self.toggleMusic,"Sound":self.toggleSoundeffect,"Exit":self.exit}
        self.position = 0
        self.actionNames = [k for (k,v) in self.actions.items()]
        self.on = True
        self.running = False
        self.music = False
        self.soundeffect = False
        self.map= Map(w=80,h=20,x=self.w//2-40,y=self.h//2-10)
        self.size = ((self.w - max(map(len,self.actionNames)))//2,(self.h-len(self.actions))//2)
        self.updateDisplay()

    def pressHandler(self,key):
        match str(key).replace("'",""):
            case Controls.DOWN:
                self.position += 1
                self.position %= len(self.actionNames)
                self.updateDisplay()  
            case Controls.UP:
                self.position += len(self.actionNames)-1
                self.position %= len(self.actionNames)
                self.updateDisplay()  
            case Controls.SUBMIT:   
                self.actions[self.actionNames[self.position]]()
            case default:
                pass
        self.updateDisplay()
          
    
    def markActiveAction(self):
        
        a = list(map(lambda x: x+" on" if x=="Music" and self.music or x=="Sound" and self.soundeffect else (x+" off" if x=="Music" or x=="Sound" else x),self.actionNames))
        a[self.position] = BLINK+MARK+a[self.position]+RESET+HIDECURSOR
        return a
        


    def draw(self):
        markedNames = self.markActiveAction()
        for i in range(0,len(markedNames)):
            sys.stdout.write(HOME)
            sys.stdout.write(CURSOR_DOWN*(self.size[1]+i)+CURSOR_RIGHT*(self.size[0]))
            sys.stdout.write(markedNames[i])
            sys.stdout.flush()

    def updateDisplay(self):
        sys.stdout.write(ERASE+HOME)
        self.draw()
    
    def cleanup(self):
        sys.stdout.write(ERASE+HOME)


    def afterGame(self,win,score):
        self.updateDisplay()
        return False


    def start(self):
        if not self.running:
            self.running = True
            game = snake.snake()
            (win,score) = game.newGame(w=80,h=20,x=w//2-40,y=h//2-10)
            self.running = self.afterGame(win,score)

    def exit(self):
        self.on = False  
        
    
    def toggleMusic(self):
        self.music = not self.music

    def toggleSoundeffect(self):
        self.soundeffect= not self.soundeffect


    
    def main(self):

        
        
        with keyboard.Events() as events:
        #musicThread = playsound(MUSIC,False,daemon=True)
            for event in events:
                    if isinstance(event,keyboard.Events.Press):
                        if event and event.key == keyboard.Key.esc:
                            self.cleanup()
                            sys.stdin.flush()
                            break
                    else:
                        self.pressHandler(event.key)
                        events = []
                        if not self.on:
                            break

        self.cleanup()
        sys.stdin.flush()

       
    
if __name__=="__main__":
    sys.stdout.write(ERASE + HOME +HIDECURSOR)
    w,h = os.get_terminal_size()
    snakeMenu = menu(w,h)
    snakeMenu.main()
