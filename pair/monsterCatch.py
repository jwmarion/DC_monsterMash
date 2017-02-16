import pygame, time, random, math


KEY_UP = 273
KEY_DOWN = 274
KEY_LEFT = 276
KEY_RIGHT = 275

KEY_W = 119
KEY_A = 97
KEY_S = 115
KEY_D = 100

KEY_ENTER = 13
KEY_ESCAPE = 27

class Character(object):
    def __init__(self):
        self.x = 1
        self.y = 1
        self.speed = 3
        self.count = 0
        self.dirX = 1
        self.dirY = 1
        self.alive = True

    def move(self):
        if self.x > 510:
            self.x = 5
        if self.x < 5:
            self.x = 509

        if self.y > 475:
            self.y = 5
        if self.y < 5:
            self.y = 474


        self.x += self.speed * self.dirX
        self.y += self.speed * self.dirY

    def randMove(self):
        if self.count == 120:
            self.count = 0
            self.dirX = random.randrange(-1,2)
            self.dirY = random.randrange(-1,2)
        self.count += 1
        self.move()

    def render(self,screen):
        screen.blit(self.img, (self.x, self.y))

    def checkCollision(self, target):
        ma = math.fabs(self.x - target.x)
        mb = math.fabs(self.y - target.y)

        distance = math.sqrt(math.pow(ma, 2) + math.pow(mb, 2))
        print distance
        if distance < 32:
            return True



class Hero(Character):
    def __init__(self):
        self.img = pygame.image.load('../images/hero.png').convert_alpha()
        self.x = 128
        self.y = 120
        self.speed = 22
        self.count = 0
        self.dirX = 1
        self.dirY = 1
        self.alive = True

class Monster(Character):
    def __init__(self):
        self.img = pygame.image.load('../images/monster.png').convert_alpha()
        self.x = 256
        self.y = 240
        self.speed = 2
        self.count = 0
        self.dirX = 1
        self.dirY = 1
        self.alive = True

class Goblin(Character):
    def __init__(self):
        self.img = pygame.image.load('../images/goblin.png').convert_alpha()
        self.x = 50
        self.y = 50
        self.speed = random.randrange(1,4)
        self.count = 0
        self.dirX = 1
        self.dirY = 1
        self.alive = True

    def chase(self, hero):
        if (self.x < hero.x):
            self.dirX = 1
        elif (self.x > hero.x):
            self.dirX = -1
        elif (self.x == hero.x):
            self.dirX = 0

        if (self.y < hero.y):
            self.dirY = 1
        elif (self.y > hero.y):
            self.dirY = -1
        elif (self.y == hero.y):
            self.dirY = 0

        self.move()

def main():


    width = 512
    height = 480
    blue_color = (97, 159, 182)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('My Game')
    clock = pygame.time.Clock()
    background_image = pygame.image.load('../images/background.png').convert_alpha()
    heroImg = pygame.image.load('../images/hero.png').convert_alpha()

    pygame.mixer.init()
    sound = pygame.mixer.Sound('../sounds/win.wav')
    soundLose = pygame.mixer.Sound('../sounds/lose.wav')

    pygame.mixer.music.load('../sounds/battle.wav')
    pygame.mixer.music.play(-1)
    font = pygame.font.Font(None, 25)
    text = font.render("A WINNER IS YOU ----- HIT ENTER TO PLAY AGAIN", True, (0,0,0))
    textLost = font.render("A LOSER IS YOU ------ HIT ENTER TO PLAY AGAIN", True, (0,0,0))

    mon = Monster()
    hero = Hero()
    gobPile = []

    level = 1
    # Game initialization

    stop_game = False
    while not stop_game:
        if len(gobPile) < level:
            gobPile.append(Goblin())

        screen.blit(background_image, (0,0))
        textLevel = font.render(str(level), True, (255,255,255))
        screen.blit(textLevel, (30,30))

        for event in pygame.event.get():

            # Event handling
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_DOWN or event.key == KEY_S:
                    hero.dirY = 1
                    hero.dirX = 0
                    hero.move()
                elif event.key == KEY_UP or event.key == KEY_W:
                    hero.dirX = 0
                    hero.dirY = -1
                    hero.move()
                elif event.key == KEY_LEFT or event.key == KEY_A:
                    hero.dirY = 0
                    hero.dirX = -1
                    hero.move()
                elif event.key == KEY_RIGHT or event.key == KEY_D:
                    hero.dirY = 0
                    hero.dirX = 1
                    hero.move()
            if event.type == pygame.QUIT:
                stop_game = True
            if event.type == pygame.QUIT:
                stop_game = True

        if hero.checkCollision(mon) == True:
            mon.x = -100
            mon.y = -100
            sound.play()
            screen.blit(text, (height/8, width/8))
            pygame.display.update()
            mon.alive = False

            eloop = True
            while eloop == True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == KEY_ESCAPE :
                            stop_game = True
                            eloop = False
                            break;
                        elif event.key == KEY_ENTER:
                            mon.alive = True
                            level += 1
                            mon.x = random.randrange(1,512)
                            mon.y = random.randrange(1,480)
                            eloop = False
                            break;
        for x in range (len(gobPile)):
            if hero.checkCollision(gobPile[x]) == True:
                soundLose.play()
                screen.blit(textLost, (height/8, width/8))
                pygame.display.update()
                hero.alive = False

                eloop = True
                while eloop == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == KEY_ESCAPE :
                                stop_game = True
                                eloop = False
                                break;
                            elif event.key == KEY_ENTER:
                                hero.alive = True
                                level = 1
                                gobPile = []
                                eloop = False
                                break;




        # Game logic

        mon.randMove()
        for y in range(len(gobPile)):
            gobPile[y].chase(hero)



        #screen.fill(blue_color)

        # Game display
        if mon.alive == True:
            mon.render(screen)
        if hero.alive == True:
            hero.render(screen)
        for z in range(len(gobPile)):
            gobPile[z].render(screen)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
