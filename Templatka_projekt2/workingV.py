import pygame, sys, random
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

#okienko
screen_width = 1300
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
#screen_hitbox = (0, 0, screen_width, screen_height)
#pygame.draw.rect(screen, (255, 0, 0), screen_hitbox, 2)
pygame.display.set_caption("First Game")
#pygame.mixer.music.load('Game/pigula.mp3')
#pygame.mixer.music.set_volume(0.5)
#pygame.mixer.music.play(-1)
font1 = pygame.font.SysFont("comicsansms", 180)


#czas/fps
clock = pygame.time.Clock()

#tekstury

walk_Right = [pygame.image.load('karoR.png')]
walk_Left = [pygame.image.load('karoL.png')]
walk_Up = [pygame.image.load('karoU.png')]
walk_Down = [pygame.image.load('karoD.png')]
bg = pygame.image.load('bgca.jpg')
char = pygame.image.load('karoR.png')
#postac

class Hero:
    def __init__(self):
            # if porusza sie do gory lub do dolu to rzeba odwrocic szerokosc z wysokoscia
        self.x = 300
        self.y = 500
        self.object_width = 100
        self.object_height = 167
        self.velx = 0
        self.vely = 0
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        #self.hitbox = (self.x + 2, self.y + 2, 100, 167)
        self.score = 0
        self.circle = 0
        self.blink = 0
        self.end = 0


    def draw(self, screen):
        screen.blit(bg, (0, 0))
        text = font.render('Score: ' + str(self.score), 1, (0, 255, 0))
        screen.blit(text, (screen_width - 120, 10))

        if self.left:
            screen.blit(walk_Left[0], (self.x, self.y))
            #self.hitbox = (self.x + 2, self.y + 2, 100, 167)

        elif self.right:
            screen.blit(walk_Right[0], (self.x, self.y))
            #self.hitbox = (self.x + 2, self.y + 2, 100, 167)

        elif self.up:
            screen.blit(walk_Up[0], (self.x, self.y))
            #self.hitbox = (self.x + 2, self.y + 2, 100, 167)

        elif self.down:
            screen.blit(walk_Down[0], (self.x, self.y))
            #self.hitbox = (self.x + 2, self.y + 2, 100, 167)

        pygame.display.update()
        #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)
#pojawiajace sie punkty

#zwykly puknt
class Objekt:
    def __init__(self, screen):
        self.screen = screen
        self.width = 15
        self.height = 15
        self.x = random.randint(0, screen_width - (3 * self.width))
        self.y = random.randint(0, screen_height - (3 * self.height))
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draww(self):
        pygame.draw.circle(self.screen,(255, 255, 10), (self.x, self.y), self.width, self.height)
        pygame.display.update()



#super punkt
class ObjektV2:
    def __init__(self, screen):
        self.screen = screen
        self.width = 20
        self.height = 20
        self.x = random.randint(0, screen_width - 3 * self.width)
        self.y = random.randint(0, (screen_height - 3 * self.height))
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draww(self):
        pygame.draw.circle(self.screen,(255, 0, 0), (self.x, self.y), self.width, self.height)
        pygame.display.update()

class End:
    def __init__(self, screen):
        self.screen = screen
        self.text = font1.render("GAME OVER", True, (255, 255, 255))


    def drawww(self):
        screen.blit(self.text, (270, 200))
        pygame.display.update()




# main loop
run = True
font = pygame.font.SysFont('comicsans', 30, True)
point = Objekt(screen)
super_point = ObjektV2(screen)
maria = Hero()
chance = random.random()
end = End(screen)

while run:
    clock.tick(100)

    #zdobycie punktu
    if chance > 0.8:
        super_point.draww()
        if maria.x < super_point.x and maria.x >= super_point.x - maria.object_width and maria.y < super_point.y and maria.y >= super_point.y - maria.object_height:
            maria.score += 3
            chance = random.random()
            super_point.x = random.randint(0, (screen_width - super_point.width - 20))
            super_point.y = random.randint(0, (screen_height - super_point.height - 20))

    else:
        point.draww()
        if maria.x < point.x and maria.x >= point.x - maria.object_width and maria.y < point.y and maria.y >= point.y - maria.object_height:
            maria.score += 1
            chance = random.random()
            point.x = random.randint(0, (screen_width - point.width - 20))
            point.y = random.randint(0, (screen_height - point.height - 20))



    #End Game
        if maria.x < 0 - maria.object_width + 40:
            maria.vely = 0
            maria.velx = 0
            maria.end = 1
            end.drawww()

        elif maria.x > screen_width - maria.object_width + 40:
            maria.vely = 0
            maria.velx = 0
            maria.end = 1
            end.drawww()

        elif maria.y < 0 - maria.object_height + 40:
            maria.vely = 0
            maria.velx = 0
            maria.end = 1
            end.drawww()

        elif maria.y > screen_height - maria.object_height + 40 :
            maria.vely = 0
            maria.velx = 0
            maria.end = 1
            end.drawww()



    #sterowanie
    keys =pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        maria.blink = 1
        if maria.blink == 1:
           maria.circle += 1
           print(maria.circle)
           if maria.circle == 5:
               maria.circle = 1
               print(maria.circle)

#trzeba popracowac nad zdjeciami zeby ladnie wygladaly
           if maria.circle == 1:
               maria.right = True
               maria.down = False
               maria.left = False
               maria.up = False
               maria.blink = 0

           elif maria.circle == 2:
               maria.right = False
               maria.down = True
               maria.left = False
               maria.up = False
               maria.blink = 0

           elif maria.circle == 3:
               maria.right = False
               maria.down = False
               maria.left = True
               maria.up = False
               maria.blink = 0

           elif maria.circle == 4:
               maria.right = False
               maria.down = False
               maria.left = False
               maria.up = True
               maria.blink = 0


    if maria.end == 0:
        if maria.right == True:
            maria.object_width = 100
            maria.object_height = 167
            maria.velx = 10
            maria.vely = 0

        elif maria.down == True:
            maria.object_width = 167
            maria.object_height = 100
            maria.vely = 10
            maria.velx = 0

        elif maria.left == True:
            maria.object_width = 100
            maria.object_height = 167
            maria.velx = -10
            maria.vely = 0

        elif maria.up == True:
            maria.object_width = 167
            maria.object_height = 100
            maria.vely = -10
            maria.velx = 0

    else:
        maria.velx = 0
        maria.vely = 0


    if maria.velx > 0:
        maria.x += maria.velx + maria.score
    if maria.vely > 0:
        maria.y += maria.vely + maria.score
    if maria.velx < 0:
        maria.x += maria.velx - maria.score
    if maria.vely < 0:
        maria.y += maria.vely - maria.score


    #wychodzenie z gierki
    for event in pygame.event.get():

        #wychodzenie z gierki
        if event.type == pygame.QUIT:
            sys.exit(0)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(0)

    maria.draw(screen)
    #pygame.draw.rect(screen, (255, 0, 0), screen_hitbox, 2)

