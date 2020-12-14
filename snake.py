import threading, queue, os, copy, time, random, sys, readchar

#Board's size
ColSize = 50
RowSize = 25

#queue to manage threads
inputQueue = queue.Queue()

# 
class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def plusCoordinate(self,coor):
        self.x += coor.x
        self.y += coor.y
    def setCoordinate(self,coor):
        self.x = coor.x
        self.y = coor.y

#vector up and down due to reverse of board (y-axis's direction is downward)
VectorUp = Point(0,-1)
VectorDown = Point(0,1)
VectorLeft = Point(-1,0)
VectorRight = Point(1,0)

# 
class Snake(object):
    def __init__(self,head,direct):
        self.part = [Point(head.x,head.y)]
        self.direct = direct    #in range [1,4] (clockwise)  #1:up   #2:right   #3:down   #4:left
    
    #point's coordinates of every single snake's part must be in range [0,25] to coordinate y and [0,50] to coordinate x
    # part[0] will be head of snake
    #input: self.Snake(object), vector:Point(object)
    def movement(self,vector):
        for i in range(len(self.part)-1,0,-1):   #star from last element of part[] to element 0th (stop at element 0th)
            self.part[i].setCoordinate(self.part[i-1])
        self.part[0].plusCoordinate(vector)   #set element 0th to new coordinate by plusing vector (depend on which kind of movement e.g up,down,ect)

#
def initField():
    field = [[0 for j in range(ColSize)] for i in range(RowSize)]
    return field
#
def clearScreen():
    os.system("clear")
# 
def getKey():
    while True:
        key = readchar.readkey()
        inputQueue.put(key)
        if key == "x" or key == "X":
            sys.exit()
#
def checkCollision(snake):
    if snake.part[0].x > ColSize-1 or snake.part[0].x < 0 or snake.part[0].y > RowSize-1 or snake.part[0].y < 0:
        return True
    for i in range(len(snake.part)-1):  #range [0,len(snake.part)-1]
        for j in range(i+1,len(snake.part)):  #range [i,len(snake.part)]
            if snake.part[i].x == snake.part[j].x and snake.part[i].y == snake.part[j].y:
                return True
    return False
#
def mergeToField(field,snake,point):
    #merge random point to field
    field[point.y][point.x] = 1
    #merge snake to field
    for i in range(len(snake.part)):
        if snake.part[i].x <= ColSize-1 and snake.part[i].x >= 0 and snake.part[i].y <= RowSize-1 and snake.part[i].y >= 0:
            field[snake.part[i].y][snake.part[i].x] = 1
#
def display(field,score):
    clearScreen()
    print("\rScore: ",score)
    for i in range(len(field[0])):
        if i == 0:
            print("\r  ",end = "")
        print("_ ",end = "")
        if i == len(field[0]) - 1:
            print("")   #for enter to new line
    for i in range(len(field)):
        print("\r||",end = "")
        if i != len(field) - 1:
            for j in range(len(field[0])):
                if field[i][j] != 0:
                    print("\033[0;37;47m[]\033[m",end = "")
                else:
                    print("  ",end = "")
        else:
            for j in range(len(field[0])):
                if field[i][j] == 0:
                    print("_ ",end = "")
                else:
                    print("\033[0;37;47m[]\033[m",end = "")
        print("||")
    print("\rPress:\n\rW - Go up, S - Go down, A - Go left, D - Go right")
    print("\rX with Ctrl + Z to exit the game")
#
def sleep(t):
    time.sleep(t)
# 
def randomPoint():
    x = random.randint(0,49)
    y = random.randint(0,24)
    return Point(x,y)

#input: snake:Snake(object), key:string
#output: Snake(object), int
def doMovement(snake,directvector,vectorup,vectordown,vectorleft,vectorright,inputQueue):
    if not inputQueue.empty():
        key = inputQueue.get()
        if (key == "w" or key == "W") and snake.direct != 3:   #go up
            snake.direct = 1
            directvector.setCoordinate(vectorup)
        elif (key == "d" or key == "D") and snake.direct != 4:  #go right
            snake.direct = 2
            directvector.setCoordinate(vectorright)
        elif (key == "s" or key == "S") and snake.direct != 1:    #go down
            snake.direct = 3
            directvector.setCoordinate(vectordown)
        elif (key == "a" or key == "A") and snake.direct != 2:  #go left
            snake.direct = 4
            directvector.setCoordinate(vectorleft)
    return snake, directvector, inputQueue

#
def SnakeGame(vectorup,vectordown,vectorleft,vectorright,inputQueue):
    #initialize field
    newField = initField()
    field = copy.deepcopy(newField)
    #initialize snake
    snake = Snake(Point(5,5),2)
    snake.part.append(Point(snake.part[0].x-1,snake.part[0].y))
    snake.part.append(Point(snake.part[0].x-2,snake.part[0].y))
    #
    point = randomPoint()
    directvector = Point(vectorright.x,vectorright.y)    #able to modify then
    preSec = int(round(time.time()*1000))
    score = 0
    flag = False
    tempPoint = Point(0,0)
    #begin the game
    mergeToField(field,snake,point)
    display(field,score)
    #
    while True:
        flag = False
        if int(round(time.time()*1000)) - preSec >= 200:
            if not inputQueue.empty():
                snake, directvector, inputQueue = doMovement(snake,directvector,vectorup,vectordown,vectorleft,vectorright,inputQueue)
                inputQueue.queue.clear()
            if point.x == snake.part[0].x and point.y == snake.part[0].y:
                score += 20
                tempPoint.setCoordinate(snake.part[len(snake.part)-1])
                flag = True
                del point
                point = randomPoint()
            snake.movement(directvector)
            field = copy.deepcopy(newField)
            mergeToField(field,snake,point)
            display(field,score)
            if flag == True:
                snake.part.append(Point(tempPoint.x,tempPoint.y))
            preSec = int(round(time.time()*1000))
        if checkCollision(snake):
            print("\r\033[1;31mGAME OVER\033[m")
            sys.exit()
        sleep(0.01)

#initialize threads
drive1 = threading.Thread(target=SnakeGame,args=(VectorUp,VectorDown,VectorLeft,VectorRight,inputQueue))
drive2 = threading.Thread(target=getKey)

#start threads
drive1.start()
drive2.start()