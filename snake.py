from options import *





w,h = os.get_terminal_size()



RIGHT_BOUND = w-3
LEFT_BOUND = 2
UPPER_BOUND = 2
LOWER_BOUND = h-3
BOUNDS = [LOWER_BOUND,RIGHT_BOUND,UPPER_BOUND,LEFT_BOUND]
STARTLEN= 5

headSymbol = HEAD
bodySegments = ["o","+"]




#velocity = positions/seconds
VELOCITY = 3
#fps = renders/second
FPS = 30




mv = moveList[0]


class snake:

    def __init__(self,audio=True,music=False):
        self.speed = VELOCITY/FPS
        self.score=0
        self.audio = audio
        self.music = music
        self.mv = mv
        self.running = True
        self.keystrokeThread = Thread(target=self.keylistenerMain,daemon=True)
        # self.listener = keyboard.Listener(on_press=self.pressHandler, on_release=None)
        # self.listener.start()

        if audio:
            self.sound = self.soundEffect
        else:
            self.sound = lambda x: x

        
    def keylistenerMain(self):
        while self.running:
            while kb.kbhit(): 
                hit = kb.getch()
                self.pressHandler(hit.decode(errors="ignore"))
                if not self.running:
                    break
            time.sleep(0.01)

    def pressHandler(self,key):
        match str(key).replace("'",""):
            case Controls.UP: 
                self.mv = moves[CURSOR_UP]
            case Controls.DOWN:
                self.mv = moves[CURSOR_DOWN]
            case Controls.LEFT:
                self.mv = moves[CURSOR_LEFT]
            case Controls.RIGHT:
                self.mv = moves[CURSOR_RIGHT]
            case Controls.SUBMIT:
                self.running = False
            case default:
                pass
    
    

    def drawBorders(self,symbol=BORDER,x=LEFT_BOUND,y=UPPER_BOUND,width=RIGHT_BOUND-LEFT_BOUND+1,height=LOWER_BOUND-UPPER_BOUND+1):
        sys.stdout.write(HOME)
        sys.stdout.write(CURSOR_RIGHT*x)
        sys.stdout.write(CURSOR_DOWN*y)
        sys.stdout.write(symbol*(width+1))
        for i in range(1,height-1):
            sys.stdout.write(HOME)
            sys.stdout.write(CURSOR_RIGHT*x)
            sys.stdout.write(CURSOR_DOWN*(y+i))
            sys.stdout.write(symbol)
            sys.stdout.write(CURSOR_RIGHT*(width-1))
            sys.stdout.write(symbol)  
        sys.stdout.write(HOME)
        sys.stdout.write(CURSOR_RIGHT*x)
        sys.stdout.write(CURSOR_DOWN*(y+height-1))
        sys.stdout.write(symbol*(width+1))

    def generateOrbs(self,count,xmin,xmax,ymin,ymax):
        Orbs = []
        while len(Orbs)<count:
            new = (random.randrange(xmin+1,xmax-2),
                    random.randrange(ymin+1,ymax-2))
            if new not in Orbs:
                Orbs.append(new)
        return Orbs

    def drawAt(self,positions,symbol=FOOD):
        for (X,Y) in positions:
            sys.stdout.write(HOME)
            sys.stdout.flush()
            sys.stdout.write(CURSOR_RIGHT*X)
            sys.stdout.write(CURSOR_DOWN*Y)
            sys.stdout.write(symbol)
            sys.stdout.flush()
        sys.stdout.write(HOME)

    def spawnOrbs(self,count,xmin,xmax,ymin,ymax):
        sys.stdout.write(HOME)
        Orbs = []
        for i in range(0,count):
            sys.stdout.write(HOME)
            sys.stdout.flush()
            new = (random.randrange(xmin+1,xmax-2),
                    random.randrange(ymin+1,ymax-2))
            if new not in Orbs:
                Orbs.append(new)
                sys.stdout.write(CURSOR_RIGHT*Orbs[i][0])
                sys.stdout.write(CURSOR_DOWN*Orbs[i][1])
                sys.stdout.write(FOOD+HOME)
            sys.stdout.flush()
        
        return Orbs

    def soundEffect(self,path):
        if path:
            playsound(path,block=False)

    def moveHead(self,size,path):
        if size>len(path):
            sys.stdout.write(BLINK)
        sys.stdout.write(HOME)
        sys.stdout.flush()
        erasePosition = path[0]
        sys.stdout.write(CURSOR_RIGHT*erasePosition['x'])
        sys.stdout.write(CURSOR_DOWN*erasePosition['y'])
        sys.stdout.write(" ")
        sys.stdout.flush()
        sys.stdout.write(HOME)
        sys.stdout.flush()
        for i in range(1,len(path)-1):
            sys.stdout.write(HOME)
            sys.stdout.write(CURSOR_RIGHT*path[i]['x'])
            sys.stdout.write(CURSOR_DOWN*path[i]['y'])
            sys.stdout.write(bodySegments[(i+len(path))%len(bodySegments)])
            
        sys.stdout.write(HOME)
        sys.stdout.flush()
        newHead=path[-1]
        sys.stdout.write(CURSOR_RIGHT*newHead['x'])
        sys.stdout.write(CURSOR_DOWN*newHead['y'])
        sys.stdout.write(headSymbol)
        sys.stdout.write(RESET)
        sys.stdout.flush()

        
    def drawScore(self,score,x,y):
        sys.stdout.write(HOME)
        sys.stdout.write(CURSOR_RIGHT*(x))
        sys.stdout.write(CURSOR_DOWN*(y-1))
        sys.stdout.write("Punktzahl: "+str(score))
        sys.stdout.write(HOME)

        
    sys.stdout.write(ERASE + HOME)

    def newGame(self,w=RIGHT_BOUND-LEFT_BOUND,h=LOWER_BOUND-UPPER_BOUND,x=LEFT_BOUND,y=UPPER_BOUND):
        sys.stdout.write(ERASE)
        self.drawBorders(x=x,y=y,width=w,height=h)
        sys.stdout.write(HOME)
        Orbs = self.generateOrbs(10,x,x+w,y,y+h)
        self.drawAt(Orbs,FOOD)

        self.keystrokeThread.start()
        positionX = (w//2+x)
        positionY = (h//2+y)
        position = {'x':positionX,'y': positionY}
        cursorPath = [position]

        size = STARTLEN
        sys.stdout.write(HOME)
        sys.stdout.write(CURSOR_RIGHT*positionX)
        sys.stdout.write(CURSOR_DOWN*positionY)
        
        while size<w*h and self.running:
         
            self.drawScore(self.score,x,y)
            position = {'x':position['x']+self.mv['x'],'y':position['y']+self.mv['y']}
            posX = position['x']
            posY = position['y']
            if posX < x+1 or posX > x+w-1 or posY < y+1 or posY > y+h -2:
                self.running = False
                self.sound(GAMEOVER)
                break
            if (posX,posY) in [(pos['x'],pos['y']) for pos in cursorPath ]:
                self.running = False
                self.sound(GAMEOVER)
                break
            cursorPath += [position]
            self.drawAt(Orbs)
            if (posX,posY) in Orbs:
               
                self.sound(EAT)
                size+=4
                Orbs.remove((posX,posY)) 
                self.score += 1
                self.speed *= 0.98
          

            if  len(Orbs)<2:
                Orbs+=self.generateOrbs(10,x,x+w,y,y+h)
                self.drawAt(Orbs)
                


            self.moveHead(size,cursorPath)
            time.sleep(self.speed)
            if size < len(cursorPath):
                cursorPath = cursorPath[1:]
            sys.stdout.write(HOME)
            sys.stdout.write(CURSOR_RIGHT*(x)+CURSOR_DOWN*(y+h+2))
            sys.stdout.write('\x1B[K')
            sys.stdout.write(HOME)
        sys.stdout.write(ERASE + HOME)
        win = self.running
        self.running = False
        self.keystrokeThread.join()
        return (win,self.score)


        












if __name__=="__main__":
    import snakeMenu
        

