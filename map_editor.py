import pygame
import os

cd = os.getcwd()

pygame.init()
WIDTH = 1024
HEIGHT = 768
CAMERA_X = 1024
CAMERA_Y = 968
display = pygame.display.set_mode((WIDTH,CAMERA_Y))
pygame.display.set_caption("MAP EDITOR - JB 2018")

print("Prioties: nw, ne, sw, se")


all_sprites = pygame.sprite.Group()
spaces = pygame.sprite.Group()
selections = pygame.sprite.Group()


WHITE = (255,255,255)
GREY = (225,225,225)
GREY2 = (150,150,150)
BLACK = (0,0,0)
RED = (255,0,0)
RED2 = (200,0,0)
ORANGE = (255,165,0)
GREEN = (0,255,0)
DARK_GREEN = (140,198,96)
BLUE = (0,0,255)
YELLOW = (225,225,0)
TURQUOISE = (0,255,255)
PINK = (255,0,255)

TITLE = pygame.font.SysFont("AgencyFB", 100)
TEXT = pygame.font.SysFont("Arial", 30)

wall = pygame.image.load(cd+"/graphics/wall_tile.png").convert()
wall2 = pygame.image.load(cd+"/graphics/wall_tile2.png").convert()
sofa = pygame.image.load(cd+"/graphics/sofa.png")
space = pygame.image.load(cd+"/graphics/space.png").convert()
player_sprite = pygame.image.load(cd+"/graphics/player_sprite1.png").convert()
enemy_sprite = pygame.image.load(cd+"/graphics/enemy_sprite.png").convert()
enemy_sprite2 = pygame.image.load(cd+"/graphics/enemy_sprite2.png").convert()
enemy_sprite3 = pygame.image.load(cd+"/graphics/enemy_sprite3.png").convert()
tile1 = pygame.image.load(cd+"/graphics/tile1.png").convert()
tile2 = pygame.image.load(cd+"/graphics/tile2.png").convert()
tile3 = pygame.image.load(cd+"/graphics/tile3.png").convert()
tile4 = pygame.image.load(cd+"/graphics/tile4.png").convert()
tile5 = pygame.image.load(cd+"/graphics/tile5.png").convert()
tile6 = pygame.image.load(cd+"/graphics/black.png").convert()
left = pygame.image.load(cd+"/graphics/left.png").convert()
right = pygame.image.load(cd+"/graphics/right.png").convert()
up = pygame.image.load(cd+"/graphics/up.png").convert()
down = pygame.image.load(cd+"/graphics/down.png").convert()
space2 = pygame.image.load(cd+"/graphics/space2.png").convert()
pygame.display.set_icon(player_sprite)

TILESIZE = 32
tile_data = []
clock = pygame.time.Clock()

class Button:

    """
    Arguments
    ---------
    display = pygame window
    x = button x
    y = button y
    width = buttton width
    height = button height
    text = text on button
    font = text font
    text_colour = colour of text
    colour = button colour
    """

    def __init__(self,display,x,y,width,height,text,font,text_colour,colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_colour = text_colour
        self.colour = colour
        self.display = display
        self.font = font

        pygame.draw.rect(self.display,self.colour,(self.x,self.y,
                                              self.width,
                                              self.height))

        self.message = self.font.render(self.text, 1, self.text_colour)
        x = self.x+(self.width/2)
        y = self.y+(self.height/2)
        self.text_rect = self.message.get_rect(center=(x, y))
        self.display.blit(self.message, self.text_rect)

    def clicked(self):
        m_x, m_y = pygame.mouse.get_pos()
        if m_x in range(self.x,self.x+self.width):
            if m_y in range(self.y,self.y+self.height):
                return True

    def update(self):
        pygame.draw.rect(self.display,self.colour,(self.x,self.y,
                                              self.width,
                                              self.height))
        self.display.blit(self.message, self.text_rect)

class Player(pygame.sprite.Sprite):
    """Player Class"""
    def __init__(self,x,y):
        self.groups = all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = player_sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy(pygame.sprite.Sprite):
    """Enemy Class"""
    def __init__(self,x,y,TYPE):
        self.groups = all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.TYPE = TYPE
        if TYPE == 1:
            self.image = enemy_sprite
        if TYPE == 2:
            self.image = enemy_sprite2
        if TYPE == 3:
            self.image = enemy_sprite3
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

class Wall(pygame.sprite.Sprite):
    """Wall class"""
    def __init__(self,x,y,TYPE):
        self.x = x
        self.y = y
        self.groups = all_sprites
        self.TYPE = TYPE

        pygame.sprite.Sprite.__init__(self, self.groups)
        if TYPE == 1:
            self.image = wall
        elif TYPE == 2:
            self.image = wall2
        elif TYPE == 3:
            self.image = sofa
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

class Space(pygame.sprite.Sprite):
    """Space Class"""
    def __init__(self,x,y,red=0):
        self.x = x
        self.y = y
        self.groups = all_sprites, spaces
        pygame.sprite.Sprite.__init__(self, self.groups)
        if red:
            self.image = space2
        else:
            self.image = space
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Tile(pygame.sprite.Sprite):
    """Tile Class"""
    def __init__(self,x,y,TYPE):
        self.x = x
        self.y = y
        self.TYPE= TYPE
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        if TYPE == 1:
            self.image = tile1
        elif TYPE == 2:
            self.image = tile2
        elif TYPE == 3:
            self.image = tile3
        elif TYPE == 4:
            self.image = tile4
        elif TYPE == 5:
            self.image = tile5
        elif TYPE == 6:
            self.image = tile6
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Node(pygame.sprite.Sprite):
    """Tile Class"""
    def __init__(self,x,y,TYPE):
        self.x = x
        self.y = y
        self.TYPE= TYPE
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        if TYPE == 1:
            self.image = left
        elif TYPE == 2:
            self.image = right
        elif TYPE == 3:
            self.image = up
        elif TYPE == 4:
            self.image = down
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Selection(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        self.groups = all_sprites, selections
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

def build():
    finished = False
    selected = 0
    X_TIMES = int(WIDTH/TILESIZE)
    Y_TIMES = int(HEIGHT/TILESIZE)
    x = 0
    y = 0
    for i in range(Y_TIMES):
        for j in range(X_TIMES):
            if j == int(X_TIMES/2) or i == int(Y_TIMES/2):
                s = Space(x*TILESIZE,y*TILESIZE,red=1)
            else:
                s = Space(x*TILESIZE,y*TILESIZE)
            x += 1
        x = 0
        y += 1
    map = []
    save_file = input("Enter map file: ")
    with open(save_file) as f:
        for line in f.readlines():
            map.append(line)
        x = 0
        y = 0
        for layer in map:
            for tile in layer:
                if tile != " ":
                    for sprite in all_sprites:
                        if sprite.__class__.__name__ == "Space":
                            if sprite.rect.collidepoint((x*32,y*32)):
                                sprite.kill()
                if tile == "W":
                    wall = Wall(x*32,y*32,1)
                elif tile == "w":
                    wall = Wall(x*32,y*32,2)
                elif tile == "s":
                    wall = Wall(x*32,y*32,3)
                elif tile == "p":
                    player = Player(x*32,y*32)
                elif tile == "e":
                    enemy = Enemy(x*32,y*32,1)
                elif tile == "E":
                    enemy = Enemy(x*32,y*32,2)
                elif tile == "S":
                    enemy = Enemy(x*32,y*32,3)
                elif tile == "1":
                    t = Tile(x*32,y*32,1)
                elif tile == "2":
                    t = Tile(x*32,y*32,2)
                elif tile == "3":
                    t = Tile(x*32,y*32,3)
                elif tile == "4":
                    t = Tile(x*32,y*32,4)
                elif tile == "5":
                    t = Tile(x*32,y*32,5)
                elif tile == "6":
                    t = Tile(x*32,y*32,6)
                elif tile == "L":
                    n = Node(x*32,y*32,1)
                elif tile == "R":
                    n = Node(x*32,y*32,2)
                elif tile == "U":
                    n = Node(x*32,y*32,3)
                elif tile == "D":
                    n = Node(x*32,y*32,4)
                x += 1
            x = 0
            y += 1


    selection = 1
        
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    x = 0
                    y = 0
                    for _ in range(Y_TIMES):
                        row = ""
                        for _ in range(X_TIMES):
                            character = " "
                            for sprite in all_sprites:
                                if sprite.rect.collidepoint((x,y)):
                                    if sprite.__class__.__name__ == "Wall":
                                        if sprite.TYPE == 1:
                                            character = "W"
                                        elif sprite.TYPE == 2:
                                            character = "w"
                                        elif sprite.TYPE == 3:
                                            character = "s"
                                    elif sprite.__class__.__name__ == "Player":
                                        character = "p"
                                    elif sprite.__class__.__name__ == "Enemy":
                                        if sprite.TYPE == 1:
                                            character = "e"
                                        elif sprite.TYPE == 2:
                                            character = "E"
                                        elif sprite.TYPE == 3:
                                            character = "S"
                                    elif sprite.__class__.__name__ == "Tile":
                                        if sprite.TYPE == 1:
                                            character = "1"
                                        elif sprite.TYPE == 2:
                                            character = "2"
                                        elif sprite.TYPE == 3:
                                            character = "3"
                                        elif sprite.TYPE == 4:
                                            character = "4"
                                        elif sprite.TYPE == 5:
                                            character = "5"
                                        elif sprite.TYPE == 6:
                                            character = "6"
                                    elif sprite.__class__.__name__ == "Node":
                                        if sprite.TYPE == 1:
                                            character = "L"
                                        elif sprite.TYPE == 2:
                                            character = "R"
                                        elif sprite.TYPE == 3:
                                            character = "U"
                                        elif sprite.TYPE == 4:
                                            character = "D"
                                
                            row += character
                            x += 32
                        tile_data.append(row)
                        x = 0
                        y += 32

                    save_file = input("Enter map file: ")
                    print("Expoting...")
                    with open(save_file, "w") as f:
                        for line in tile_data:
                            f.write(line)
                            f.write("\n")
                    print("Exported!")
                    for i in tile_data:
                        tile_data.remove(i)


        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            for space in spaces:
                if space.rect.collidepoint(pos):
                    if selection == 1:
                        wall = Wall(space.rect.x,space.rect.y,1)
                    elif selection == 2:
                        wall = Wall(space.rect.x,space.rect.y,2)
                    elif selection == 3:
                        player = Player(space.rect.x,space.rect.y)
                    elif selection == 4:
                        enemy = Enemy(space.rect.x,space.rect.y,1)
                    elif selection == 5:
                        tile = Tile(space.rect.x,space.rect.y,1)
                    elif selection == 6:
                        tile = Tile(space.rect.x,space.rect.y,2)
                    elif selection == 7:
                        tile = Tile(space.rect.x,space.rect.y,3)
                    elif selection == 8:
                        tile = Tile(space.rect.x,space.rect.y,4)
                    elif selection == 9:
                        wall = Wall(space.rect.x,space.rect.y,3)
                    elif selection == 10:
                        node = Node(space.rect.x,space.rect.y,1)
                    elif selection == 11:
                        node = Node(space.rect.x,space.rect.y,2)
                    elif selection == 12:
                        node = Node(space.rect.x,space.rect.y,3)
                    elif selection == 13:
                        node = Node(space.rect.x,space.rect.y,4)
                    elif selection == 14:
                        enemy = Enemy(space.rect.x,space.rect.y,2)
                    elif selection == 15:
                        tile = Tile(space.rect.x,space.rect.y,5)
                    elif selection == 16:
                        tile = Tile(space.rect.x,space.rect.y,6)
                    elif selection == 17:
                        enemy = Enemy(space.rect.x,space.rect.y,3)
                    space.kill()
        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            for sprite in all_sprites:
                if sprite.rect.collidepoint(pos):
                    space = Space(sprite.rect.x,sprite.rect.y)
                    sprite.kill()


        display.fill(DARK_GREEN)

        s1 = Button(display,0,CAMERA_Y-200,100,100,"Wall 1",TEXT,WHITE,BLACK)
        s2 = Button(display,101,CAMERA_Y-200,100,100,"Wall 2",TEXT,WHITE,BLACK)
        s3 = Button(display,202,CAMERA_Y-200,100,100,"Player",TEXT,WHITE,BLACK)
        s4 = Button(display,303,CAMERA_Y-200,100,100,"Enemy 1",TEXT,WHITE,BLACK)
        s5 = Button(display,404,CAMERA_Y-200,100,100,"Tile 1",TEXT,WHITE,BLACK)
        s6 = Button(display,505,CAMERA_Y-200,100,100,"Tile 2",TEXT,WHITE,BLACK)
        s7 = Button(display,606,CAMERA_Y-200,100,100,"Tile 3",TEXT,WHITE,BLACK)
        s8 = Button(display,707,CAMERA_Y-200,100,100,"Tile 4",TEXT,WHITE,BLACK)
        s9 = Button(display,808,CAMERA_Y-200,100,100,"Sofa",TEXT,WHITE,BLACK)
        s10 = Button(display,909,CAMERA_Y-200,100,100,"Left",TEXT,WHITE,BLACK)
        s11 = Button(display,0,CAMERA_Y-100,100,100,"Right",TEXT,WHITE,BLACK)
        s12 = Button(display,101,CAMERA_Y-100,100,100,"Up",TEXT,WHITE,BLACK)
        s13 = Button(display,202,CAMERA_Y-100,100,100,"Down",TEXT,WHITE,BLACK)
        s14 = Button(display,303,CAMERA_Y-100,100,100,"Enemy 2",TEXT,WHITE,BLACK)
        s15 = Button(display,404,CAMERA_Y-100,100,100,"Tile 5",TEXT,WHITE,BLACK)
        s16 = Button(display,505,CAMERA_Y-100,100,100,"Tile 6",TEXT,WHITE,BLACK)
        s17 = Button(display,606,CAMERA_Y-100,100,100,"Enemy 3",TEXT,WHITE,BLACK)

        if pygame.mouse.get_pressed()[0]:
            if s1.clicked():
                selection = 1
            elif s2.clicked():
                selection = 2
            elif s3.clicked():
                selection = 3
            elif s4.clicked():
                selection = 4
            elif s5.clicked():
                selection = 5
            elif s6.clicked():
                selection = 6
            elif s7.clicked():
                selection = 7
            elif s8.clicked():
                selection = 8
            elif s9.clicked():
                selection = 9
            elif s10.clicked():
                selection = 10
            elif s11.clicked():
                selection = 11
            elif s12.clicked():
                selection = 12
            elif s13.clicked():
                selection = 13
            elif s14.clicked():
                selection = 14
            elif s15.clicked():
                selection = 15
            elif s16.clicked():
                selection = 16
            elif s17.clicked():
                selection = 17

        
        all_sprites.update()
        all_sprites.draw(display)
        pygame.display.update()
        clock.tick(60)

build()


    



