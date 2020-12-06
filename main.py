import pygame, sys, random
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.dir = Vector2(0,0)
        self.checkAdd = False

    def drawSnake(self):
        for block in self.body:
            xPos = int(xAdjust + block.x * gridCell_size)
            yPos = int(yAdjust + block.y * gridCell_size)
            blockRect = pygame.Rect(xPos, yPos, gridCell_size, gridCell_size)

            if(block == self.body[0]):
                pygame.draw.circle(screen, (46, 140, 212),
                                   (blockRect.left + (gridCell_size // 2), blockRect.top + (gridCell_size // 2)),
                                   blockRect.width//2)
            elif(block == self.body[len(self.body)-1]):
                blockRect.width -= 10
                blockRect.height -= 10
                blockRect.left += 5
                blockRect.top += 5
                pygame.draw.rect(screen, (46, 140, 212), blockRect)
            else:
                pygame.draw.rect(screen, (46, 140, 212), blockRect)

    def moveSnake(self):

        if self.checkAdd == True:
            bodyCopy = self.body[:]
            bodyCopy.insert(0, bodyCopy[0] + self.dir)
            self.body = bodyCopy[:]
            self.checkAdd = False
        else:
            bodyCopy = self.body[:-1]
            bodyCopy.insert(0, bodyCopy[0] + self.dir)
            self.body = bodyCopy[:]

    def addBlock(self):
        self.checkAdd = True

    def resetSnake(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.dir = Vector2(0, 0)
class Fruit:
    def __init__(self):
        self.x = random.randint(0, gridCell_num-1)
        self.y = random.randint(0, gridCell_num-1)
        self.position = Vector2(self.x, self.y)
        self.shrink = True
        self.radius = 0

    def drawFruit(self):
        xPos = int(xAdjust +self.position.x * gridCell_size)
        yPos = int(yAdjust + self.position.y * gridCell_size)
        fruitRect = pygame.Rect(xPos, yPos, gridCell_size, gridCell_size)
        realRadius = fruitRect.width//2

        if(self.radius == 0):
            self.radius = fruitRect.width//2

        if(self.radius >=10 and self.shrink):
            self.radius -= 0.2
            if(self.radius <= 10):
                self.shrink = False
        elif(self.radius <= 10 or self.shrink != True):
            self.radius += 0.2
            if(self.radius >= 15):
                self.shrink = True
        pygame.draw.circle(screen, (196, 24, 52), (fruitRect.left + (gridCell_size//2), fruitRect.top + (gridCell_size//2)), self.radius)

    def randomize(self):
        self.x = random.randint(0, gridCell_num-1)
        self.y = random.randint(0, gridCell_num-1)
        self.position = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.moveSnake()
        self.overlapCheck()
        self.loseGame()

    def drawElements(self):
        self.fruit.drawFruit()
        self.snake.drawSnake()

    def drawGrid(self):

        gridX = 0
        gridY = 0
        alt = True

        for i in range(gridCell_num):
            for j in range(gridCell_num):
                gridRect = pygame.Rect(xAdjust + gridX, yAdjust + gridY, gridCell_size, gridCell_size)
                pygame.draw.rect(screen, (31, 41, 54), gridRect)

                gridY += 60
                if (gridY >= 600):
                    break

            gridX += 30

            if (alt):
                gridY = 30
                alt = False
            else:
                gridY = 0
                alt = True

            if (gridX > 600):
                break

    def drawText(self):
        self.gameFont = pygame.font.Font("ARCADECLASSIC.ttf", 50)
        self.scoreText = str(len(main.snake.body) - 3)


        scoreSurf = self.gameFont.render(self.scoreText, True, (255, 255, 255))
        scoreXPos = int(gridCell_num * gridCell_size + 300)
        scoreYPos = int(gridCell_num * gridCell_size - 100)
        scoreRect = scoreSurf.get_rect(center = (scoreXPos, scoreYPos))
        scoreWidth = 40
        if(int(self.scoreText) > 9):
            scoreWidth += 30
        if(int(self.scoreText) > 99):
            scoreWidth += 30
        scoreBord = pygame.Rect(scoreRect.left - 7, scoreRect.top, scoreWidth, 50)

        pygame.draw.rect(screen, (31, 41, 54), scoreBord)
        pygame.draw.rect(screen, (0, 0, 0), scoreBord, 2)
        screen.blit(scoreSurf, scoreRect)

    def overlapCheck(self):
        if self.fruit.position == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.addBlock()

        for block in self.snake.body[1:]:
            if block == self.fruit.position:
                self.fruit.randomize()

    def loseGame(self):
        if(self.snake.body[0].x >= gridCell_num or self.snake.body[0].x < 0 or self.snake.body[0].y >= gridCell_num or self.snake.body[0].y < 0):
            self.gameOver()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()

    def gameOver(self):
        self.snake.resetSnake()



pygame.init()

gridCell_size = 30
gridCell_num = 20

screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()

gameScreenBord = pygame.Surface((10 + gridCell_num* gridCell_size,10 + gridCell_num* gridCell_size))
gameScreenBord.fill((167, 206, 209))
gameScreen = pygame.Surface((gridCell_num * gridCell_size, gridCell_num * gridCell_size))
gameScreen.fill((38, 52, 69))

snakeSurf = pygame.Surface((30, 30)) #snake
snakeSurf.fill((46, 140, 212))

x_pos = 540
y_pos = 360
xAdjust = 200
yAdjust = 50

main = Main()

updateScreen = pygame.USEREVENT

difficulty = 100
pygame.time.set_timer(updateScreen, difficulty)  # add if statement, put in an if statement inside the loop based on the button
 # easy = 100, medium = 70, hard = 50, impossible = 35


while True:
    for event in pygame.event.get():
        #pygame.time.set_timer(updateScreen, difficulty)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == updateScreen:
            main.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if(main.snake.dir.y != 1):
                    main.snake.dir = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if (main.snake.dir.y != -1):
                    main.snake.dir = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if (main.snake.dir.x != 1):
                    main.snake.dir = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if (main.snake.dir.x != -1):
                    main.snake.dir = Vector2(1, 0)

    screen.fill((38, 52, 69))

    screen.blit(gameScreenBord, (xAdjust-5, yAdjust-5))
    screen.blit(gameScreen, (xAdjust, yAdjust))
    main.drawGrid()
    main.drawElements()
    main.drawText()
    pygame.display.update()
    clock.tick(60)