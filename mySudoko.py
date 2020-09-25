
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((450, 650))

run = True

hintImg = pygame.image.load("hint.png")
solutionImg = pygame.image.load("solution.png")
newImg = pygame.image.load("new-game.png")

class Grid(object):

    tN = []
    for i in range(9):
        tN.append([])
        for j in range(9):
            tN[i].append(0)


    def __init__(self, table, pos, width, height):
        self.width = width
        self.height = height
        self.pos = pos
        self.table = table
        self.sudoko_solved = False
        self.selected = None
        self.cellWidth = (int)(width / 9)
        self.cellHeight = (int)(height / 9)
        self.makeTemp()
        self.solve_puzzle(0, 0, 0)
        self.wrongAttempts = 0

    def makeTemp(self):
        self.tempTable = []
        for i in range(9):
            self.tempTable.append([])
            for j in range(9):
                self.tempTable[i].append(self.table[i][j])

    def drawGrid(self):
        pygame.draw.rect(screen, (23, 66, 88), (self.pos[0], self.pos[1], self.width, self.height))
        for i in range(10):
            if i%3 == 0:
                thick = 3
            else:
                thick = 1
            pygame.draw.line(screen, (0,0,0), (self.pos[0], self.pos[1]+i*self.cellHeight), (self.pos[0]+self.width, self.pos[1]+i*self.cellHeight), thick)
            pygame.draw.line(screen, (0,0,0), (self.pos[0]+i*self.cellWidth, self.pos[1]), (self.pos[0]+i*self.cellWidth, self.pos[1]+self.height), thick)
        pass
    def drawNumbers(self):
        font = pygame.font.Font('freesansbold.ttf', 28)
        for i in range(9):
            for j in range(9):
                if self.table[i][j] > 0:
                    num = font.render(f"{self.table[i][j]}", True, (0, 255, 255))
                    screen.blit(num, (self.pos[0]+j*self.cellWidth+18, self.pos[1]+i*self.cellHeight+14))

    def drawSelected(self):
        if self.selected != None:
            #self.selected = (row, col)
            row = self.selected[0]
            col = self.selected[1]
            X = col * self.cellWidth + self.pos[0]
            Y = row * self.cellHeight + self.pos[1]
            pygame.draw.rect(screen, (255, 0, 0), (X, Y, self.cellWidth, self.cellHeight), 3)

    def drawTempNumbers(self):
        font = pygame.font.Font('freesansbold.ttf', 24)
        for i in range(9):
            for j in range(9):
                if self.tN[i][j] != 0:
                    num = font.render(f"{self.tN[i][j]}", True, (0, 255, 0))
                    screen.blit(num, (self.pos[0]+j*self.cellWidth, self.pos[1]+i*self.cellHeight))

    def checkMouse(self, pos):
        col = (pos[0]-self.pos[0]) // self.cellWidth
        row = (pos[1]-self.pos[1]) // self.cellHeight
        if col <= 8 and col >=0 and row <= 8 and row >= 0:
            self.selected = (row, col)
        elif pos[0] >= self.width - 74 and pos[0] <= self.width - 10 and pos[1] >= 26 and pos[1] <= 90:
            self.Hint()
        elif pos[0] >= 10 and pos[0] <= 74 and pos[1] >= 26 and pos[1] <= 90:
            self.solveShow()
        elif pos[0] >= 193 and pos[0] <= 193+64 and pos[1] >= 26 and pos[1] <= 90:
            self.newGame()
        return row, col

    def newGame(self):

        pass
    def solveShow(self):
        self.sudoko_solved = False
        for i in range(9):
            for j in range(9):
                self.tN[i][j] = 0
                self.tempTable[i][j] = self.table[i][j]
        self.solve_puzzle(0, 0, 1)


    def drawWrong(self):
        font = pygame.font.Font('freesansbold.ttf', 28)
        wNum = font.render(f"Wrong Attemps = {self.wrongAttempts}", True, (0, 255, 0))
        screen.blit(wNum, (15, 560))



    def find_next_empty(self, i, j):
        while i!=-1 and self.tempTable[i][j]!=0:
            i, j = self.find_next(i, j)
        return i, j

    def solve_puzzle(self, i, j, show):
        if show:
            print(self.table, "LOL", self.tempTable)
            print(i, j)
        i, j = self.find_next_empty(i, j)
        if show:
            print(i, j, show)

        if i==-1:
            self.sudoko_solved = True
            return True
        if show:
            Erfan.selected = i, j
            self.drawSelected()
        for k in range(1, 10):
            if self.is_possible(i, j, k):
                self.tempTable[i][j] = k
                if show:
                    self.table[i][j] = k
                    self.drawNumbers()
                self.solve_puzzle(i, j, show)
                if self.sudoko_solved:
                    return True
                if show:
                    self.table[i][j] = 0
                    self.drawNumbers()
                self.tempTable[i][j] = 0
        return False


    def find_next(self, i, j):
        if i==8 and j==8:
            return -1, -1
        if j==8:
            return i+1, 0
        return i, j+1

    def is_possible(self, i, j, k):
        for l in range(9):
            if self.tempTable[i][l] == k:
                return False
            if self.tempTable[l][j] == k:
                return False
        for x in range(3):
            for y in range(3):
                if self.tempTable[(i//3)*3+x][(j//3)*3+y] == k:
                    return False
        return True

    def Hint(self):
        list = []
        for i in range(9):
            for j in range(9):
                if self.table[i][j] == 0:
                    list.append((i, j))
        if len(list) != 0:
            n = random.randint(0, len(list)-1)
            x, y = list[n]
            self.table[x][y] = self.tempTable[x][y]
            self.tN[x][y] = 0
            self.selected = (x, y)
    def drawHint(self):
        screen.blit(hintImg, (self.width - 74, self.pos[1]-74))

    def drawSolution(self):
        screen.blit(solutionImg, (10,  26))

    def drawNew(self):
        screen.blit(newImg, (193, 26))




Table = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
         [6, 8, 0, 0, 7, 0, 0, 9, 0],
         [1, 9, 0, 0, 0, 4, 5, 0, 0],
         [8, 2, 0, 1, 0, 0, 0, 4, 0],
         [0, 0, 4, 6, 0, 2, 9, 0, 0],
         [0, 5, 0, 0, 0, 3, 0, 2, 8],
         [0, 0, 9, 3, 0, 0, 0, 7, 4],
         [0, 4, 0, 0, 5, 0, 0, 3, 6],
         [7, 0, 3, 0, 1, 8, 0 ,0, 0]]

Erfan = Grid(Table, (0, 100), 450, 450)

def format_time(time):
    sec = (int)(time/1000)
    min = sec // 60
    hour = min // 60
    sec = sec % 60
    return hour, min, sec

def drawTime():
    time = pygame.time.get_ticks()
    h, m, s = format_time(time)
    font = pygame.font.Font('freesansbold.ttf', 24)
    showTime = font.render(f"Timer : {m}:{s}", True, (0, 255, 0))
    screen.blit(showTime, (300, 560))


while run:
    screen.fill((0,0,0))
    Erfan.drawGrid()
   # print(Erfan.tempTable)
    #print(Erfan.table)
    Erfan.drawNumbers()
    Erfan.drawSelected()
#    Erfan.tN[1][1] = 2
    Erfan.drawTempNumbers()
    Erfan.drawWrong()
    Erfan.drawHint()
    Erfan.drawSolution()
    Erfan.drawNew()

    key = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            r, c = Erfan.checkMouse(pos)
            print(r, c)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                key = 1
            if event.key == pygame.K_2:
                key = 2
            if event.key == pygame.K_3:
                key = 3
            if event.key == pygame.K_4:
                key = 4
            if event.key == pygame.K_5:
                key = 5
            if event.key == pygame.K_6:
                key = 6
            if event.key == pygame.K_7:
                key = 7
            if event.key == pygame.K_8:
                key = 8
            if event.key == pygame.K_9:
                key = 9
            if event.key == pygame.K_0:
                Erfan.Hint()
            if event.key == pygame.K_SPACE:
                Erfan.solveShow()
            if (event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE) and Erfan.selected:
                r, c = Erfan.selected
                Erfan.tN[r][c] = 0
            if Erfan.selected and key:
                r, c = Erfan.selected
                if Erfan.table[r][c] == 0:
                    Erfan.tN[r][c] = key
            if event.key == pygame.K_RETURN and Erfan.selected:
                r, c = Erfan.selected
                if Erfan.tN[r][c] != 0:
                    if Erfan.tempTable[r][c] == Erfan.tN[r][c]:
                        Erfan.table[r][c] = Erfan.tN[r][c]
                        Erfan.tN[r][c] = 0
                    else:
                        Erfan.wrongAttempts += 1
                        print(Erfan.wrongAttempts)
    #time = pygame.time.get_ticks()
    #print(format_time(time))
    drawTime()
    pygame.display.update()