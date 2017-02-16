import pygame, random

class goblin():
    def __init__(self):
        self.x = random.randrange(1,600)
        self.y = random.randrange(100,300)
        self.speed = 3
        self.gob = pygame.image.load('images/goblin.png').convert_alpha()

    def move(self):
        mx = random.randrange(-1,2)
        my = random.randrange(-1,2)
        self.x += mx * self.speed
        self.y += my * self.speed

    def render(self, screen):
        screen.blit(self.gob, (self.y, self.x))
        screen.blit(gobImg, (x,y))

def main():
    width = 706
    height = 404
    #blue_color = (97, 159, 182)


    pygame.init()
    screen = pygame.display.set_mode((width, height))
    background_image = pygame.image.load('images/woods.png').convert_alpha()
    pygame.display.set_caption('My Game')
    clock = pygame.time.Clock()

    gobPile = []

    gobNum = 5

    for x in range(gobNum):
        gobPile.append(goblin())


    # Game initialization

    stop_game = False
    while not stop_game:
        for event in pygame.event.get():

            # Event handling

            if event.type == pygame.QUIT:
                stop_game = True


        # Game logic

        # Draw background


        screen.blit(background_image, (0,0))
        for g in gobPile:
            g.move()
            g.render(screen)
        # Game display

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
