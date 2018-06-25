import pygame
import random
import math
import time
import os


pygame.mixer.pre_init(22050,-16, 2, 1024)
pygame.init()
cd = os.getcwd()

joysticks = pygame.joystick.get_count()
if joysticks:
    controller = pygame.joystick.Joystick(0)
    controller.init()

WIDTH = 1024
HEIGHT = 768
CAMERA_X = 800
CAMERA_Y = 600

DEV = 0
KILLED = []
OPTIONS = [1]
EXPLOSIONS = []
ENEMIES = pygame.sprite.Group()

tmp_display = pygame.display.set_mode((CAMERA_X,CAMERA_Y))
pygame.display.set_caption("RICO'S REVENGE - JB 2018")

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
tiles = pygame.sprite.Group()
bullets = pygame.sprite.Group()
items = pygame.sprite.Group()
nodes = pygame.sprite.Group()
detectors = pygame.sprite.Group()


TITLE = pygame.font.SysFont("AgencyFB", 100)
TITLE2 = pygame.font.SysFont("AgencyFB", 50)
TEXT = pygame.font.SysFont("AgencyFB", 30)

levels = [
    "level1.txt",
    "level2.txt",
    "level3.txt",
    "level4.txt",
    "level5.txt",
    "level6.txt",
    "level7.txt",
    "level8.txt",
    ]
last = levels[-1]
final_level = last.replace(last[-5],str(int(last[-5])+1))

WHITE = (255,255,255)
GREY = (150,150,150)
GREY2 = (50,50,50)
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

TILESIZE = 32
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE
SPEED = 5
BULLET_SPEED = 20

flags1 = 0
flags2 = pygame.FULLSCREEN

tile1 = pygame.image.load(cd+"/graphics/tile1.png").convert()
tile2 = pygame.image.load(cd+"/graphics/tile2.png").convert()
tile3 = pygame.image.load(cd+"/graphics/tile3.png").convert()
tile4 = pygame.image.load(cd+"/graphics/tile4.png").convert()
tile5 = pygame.image.load(cd+"/graphics/tile5.png").convert()
wall = pygame.image.load(cd+"/graphics/wall_tile.png").convert()
wall2 = pygame.image.load(cd+"/graphics/wall_tile2.png").convert()
sofa = pygame.image.load(cd+"/graphics/sofa.png").convert()
player_sprite1 = pygame.image.load(cd+"/graphics/player_sprite1.png").convert_alpha()
player_sprite2 = pygame.image.load(cd+"/graphics/player_sprite2.png").convert_alpha()
player_sprite3 = pygame.image.load(cd+"/graphics/player_sprite3.png").convert_alpha()
enemy_sprite = pygame.image.load(cd+"/graphics/enemy_sprite.png").convert_alpha()
enemy_sprite2 = pygame.image.load(cd+"/graphics/enemy_sprite2.png").convert_alpha()
enemy_sprite3 = pygame.image.load(cd+"/graphics/enemy_sprite3.png").convert_alpha()
enemy_sprite4 = pygame.image.load(cd+"/graphics/enemy_sprite4.png").convert_alpha()
rip = pygame.image.load(cd+"/graphics/rip.png").convert_alpha()
bullet = pygame.image.load(cd+"/graphics/bullet.png").convert_alpha()
flame = pygame.image.load(cd+"/graphics/flame.png").convert_alpha()
blood = pygame.image.load(cd+"/graphics/blood.png").convert_alpha()
grenade = pygame.image.load(cd+"/graphics/grenade.png").convert_alpha()
exploded = pygame.image.load(cd+"/graphics/exploded.png").convert_alpha()
exploded2 = pygame.image.load(cd+"/graphics/exploded2.png").convert_alpha()
enemy_exploded = pygame.image.load(cd+"/graphics/enemy_exploded.png").convert_alpha()
menu_background = pygame.image.load(cd+"/graphics/menu_background.png").convert()
menu_background2 = pygame.image.load(cd+"/graphics/menu_background2.png").convert()
left = pygame.image.load(cd+"/graphics/left.png").convert()
right = pygame.image.load(cd+"/graphics/right.png").convert()
up = pygame.image.load(cd+"/graphics/up.png").convert()
down = pygame.image.load(cd+"/graphics/down.png").convert()
black = pygame.image.load(cd+"/graphics/black.png").convert()
paused_image = pygame.image.load(cd+"/graphics/paused.png").convert_alpha()
crater = pygame.image.load(cd+"/graphics/crater.png").convert_alpha()
extraction = pygame.image.load(cd+"/graphics/extraction.png").convert()
cc = pygame.image.load(cd+"/graphics/controls.png").convert()
gore1 = pygame.image.load(cd+"/graphics/gore1.png").convert_alpha()
gore2 = pygame.image.load(cd+"/graphics/gore2.png").convert_alpha()
gore3 = pygame.image.load(cd+"/graphics/gore3.png").convert_alpha()
fire_damage = pygame.image.load(cd+"/graphics/fire_damage.png").convert_alpha()
fire = pygame.image.load(cd+"/graphics/fire.png").convert_alpha()
fire2 = pygame.image.load(cd+"/graphics/fire2.png").convert_alpha()

AR = pygame.mixer.Sound(cd+"/sounds/gun1.wav")
SHOTGUN = pygame.mixer.Sound(cd+"/sounds/gun2.wav")
FLAMETHROWER = pygame.mixer.Sound(cd+"/sounds/flame_noise.wav")
grenade_sound = pygame.mixer.Sound(cd+"/sounds/grenade_sound.wav")
death_sound = pygame.mixer.Sound(cd+"/sounds/lose_sound.wav")
enemy_killed = pygame.mixer.Sound(cd+"/sounds/enemy_killed.wav")
game_music = pygame.mixer.Sound(cd+"/sounds/main_music.wav")
game_music.set_volume(0.3)
menu_theme = pygame.mixer.Sound(cd+"/sounds/menu_theme.wav")
click = pygame.mixer.Sound(cd+"/sounds/click.wav")
victory_music = pygame.mixer.Sound(cd+"/sounds/pause_music.wav")
speech = pygame.mixer.Sound(cd+"/sounds/speech.wav")

pygame.display.set_icon(player_sprite1)
clock = pygame.time.Clock()

def generate_random():
    nw = ["nw1.txt","nw2.txt","nw3.txt","nw4.txt"]
    ne = ["ne1.txt","ne2.txt","ne3.txt","ne4.txt"]
    sw = ["sw1.txt","sw2.txt","sw3.txt"]
    se = ["se1.txt","se2.txt","se3.txt"]
    map = []
    p1 = random.choice(nw)
    p2 = random.choice(ne)
    p3 = random.choice(sw)
    p4 = random.choice(se)

    counter = 0
    counter2 = 0
    for i in range(28):
        line = ""
        if i < 13:
            with open(p1) as f:
                lines = f.readlines()
                line += lines[counter].replace("\n", "").strip()
            with open(p2) as f:
                lines = f.readlines()
                line += lines[counter].replace("\n", "").strip()
            counter += 1
        else:
            with open(p3) as f:
                lines = f.readlines()
                line += lines[counter2].replace("\n", "").strip()
            with open(p4) as f:
                lines = f.readlines()
                line += lines[counter2].replace("\n", "").strip()
            counter2 += 1

        map.append(line)
        
    return map

class Text:

    """
    Arguments
    ---------
    display = pygame window
    x = text x (center)
    y = text y (center)
    text = text string
    font = text font
    text_colour = colour of text
    """

    def __init__(self,display,x,y,text,font,text_colour):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.display = display
        self.text_colour = text_colour

        self.message = self.font.render(self.text, 1, self.text_colour)
        self.display.blit(self.message, (self.x, self.y))

    def update(self):
        self.display.blit(self.message, (self.x, self.y))

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
        self.org_image = player_sprite1
        self.rect = self.org_image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = self.rect.x
        self.y = self.rect.y
        self.counter = 0
        self.grenade_counter = 100
        self.grenade_ammo = 2

    def rotate(self):
        mx, my = pygame.mouse.get_pos()
        self.degrees = int(math.degrees(math.atan2(CAMERA_X/2-mx,CAMERA_Y/2-my)))
        self.image = pygame.transform.rotate(self.org_image, self.degrees)

    def gun(self,gun):
        if gun == "ar":
            self.ammo = 20
            self.reload_rate = 10
            self.gun = "ar"
            self.gun_noise = AR
            self.org_image = player_sprite1
        elif gun == "shotgun":
            self.ammo = 20
            self.reload_rate = 50
            self.gun = "shotgun"
            self.gun_noise = SHOTGUN
            self.org_image = player_sprite2
        elif gun == "flamethrower":
            self.ammo = 20
            self.reload_rate = 3
            self.gun = "flamethrower"
            self.gun_noise = FLAMETHROWER
            self.org_image = player_sprite3

    def c_gun(self,gun):
        if gun == "ar":
            self.ammo = 20
            self.reload_rate = 10
            self.gun = "ar"
            self.gun_noise = AR
            self.org_image = player_sprite1
        elif gun == "shotgun":
            self.ammo = 20
            self.reload_rate = 50
            self.gun = "shotgun"
            self.gun_noise = SHOTGUN
            self.org_image = player_sprite2
        elif gun == "flamethrower":
            self.ammo = 20
            self.reload_rate = 3
            self.gun = "flamethrower"
            self.gun_noise = FLAMETHROWER
            self.org_image = player_sprite3
        

    def fire(self,dest_x,dest_y):
        if self.gun == "ar":
            bullet = Bullet(self.rect.x+16,self.rect.y+16,dest_x,dest_y,"player")
            self.ammo -= 1
        elif self.gun == "shotgun":
            bullet = Bullet(self.rect.x+16,self.rect.y+16,dest_x,dest_y,"player")
            bullet = Bullet(self.rect.x+16,self.rect.y+16,dest_x,dest_y+20,"player")
            bullet = Bullet(self.rect.x+16,self.rect.y+16,dest_x,dest_y-20,"player")
            bullet = Bullet(self.rect.x+16,self.rect.y+16,dest_x+20,dest_y,"player")
            bullet = Bullet(self.rect.x+16,self.rect.y+16,dest_x-20,dest_y,"player")
            self.ammo -= 4
        elif self.gun == "flamethrower":
            x_increase = random.randint(-20,20)
            y_increase = random.randint(-20,20)
            flame = Flame(self.rect.x+16,self.rect.y+16,dest_x+x_increase,dest_y+y_increase,self,"player")
            self.ammo -= 0.5

        if self.ammo < 0:
            self.ammo = 0

    def update(self):
        self.rotate()
        self.counter += 1
        self.grenade_counter += 1
        if not joysticks:
            if pygame.mouse.get_pressed()[0] and self.counter > self.reload_rate and self.ammo > 0:
                self.counter = 0
                pygame.mixer.Sound.play(self.gun_noise)
                dest_x,dest_y =  pygame.mouse.get_pos()
                self.fire(dest_x,dest_y)
            elif pygame.mouse.get_pressed()[2] and self.grenade_counter > 100 and self.grenade_ammo >= 1:
                self.grenade_counter = 0
                dest_x,dest_y =  pygame.mouse.get_pos()
                grenade = Grenade(self.rect.x+16,self.rect.y+16,dest_x,dest_y,self,"player")
                self.grenade_ammo -= 1
        else:
            if controller.get_button(7) and self.counter > self.reload_rate and self.ammo > 0:
                self.counter = 0
                pygame.mixer.Sound.play(self.gun_noise)
                dest_x,dest_y =  pygame.mouse.get_pos()
                self.fire(dest_x,dest_y)
            elif controller.get_button(6) and self.grenade_counter > 100 and self.grenade_ammo >= 1:
                self.grenade_counter = 0
                dest_x,dest_y =  pygame.mouse.get_pos()
                grenade = Grenade(self.rect.x+16,self.rect.y+16,dest_x,dest_y,self,"player")
                self.grenade_ammo -= 1

        if self.x > WIDTH:
            self.x = WIDTH
        elif self.x < 0:
            self.x = 0
        elif self.y > HEIGHT:
            self.y = HEIGHT
        elif self.y < 0:
            self.y = 0
            
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy(pygame.sprite.Sprite):
    """Enemy Class"""
    def __init__(self,x,y,TYPE,rnd=0):
        self.groups = all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = enemy_sprite
        self.rect = enemy_sprite.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        if rnd:
            self.TYPE = random.randint(1,4)
        else:
            self.TYPE = TYPE
        self.suicider = 0
        if self.TYPE == 1:
            self.gun = "ar"
            self.reload_rate = 10
            self.org_image = enemy_sprite
            self.counter = 0
        elif self.TYPE == 2:
            self.gun = "shotgun"
            self.reload_rate = 50
            self.org_image = enemy_sprite2
            self.counter = 40
        elif self.TYPE == 3:
            self.gun = "smg"
            self.reload_rate = 5
            self.org_image = enemy_sprite3
            self.counter = -10
        elif self.TYPE == 4:
            self.gun = "flamethrower"
            self.reload_rate = 5
            self.org_image = enemy_sprite4
            self.counter = 0
            
        self.image = self.org_image
        self.x = self.rect.x
        self.y = self.rect.y
        self.seen = False
        self.move_x = 0
        self.move_y = 1
        self.detection = 0
        self.detections = []
        self.can_see = False

    def setup(self,player):
        self.player = player

    def rotate(self,target_x,target_y):
        degrees = int(math.degrees(math.atan2(self.x-self.player.x,self.y-self.player.y)))
        self.image = pygame.transform.rotate(self.org_image, degrees)

    def move(self,destination):
        self.rotate(self.player.x,self.player.y)
        dest_x,dest_y =  destination.x,destination.y
        x_diff = dest_x - self.x
        y_diff = dest_y - self.y
        angle = math.atan2(y_diff, x_diff)
        change_x = math.cos(angle) * 2
        change_y = math.sin(angle) * 2
        self.x += change_x
        self.y += change_y

    def has_los(self):
        self.seen = True       
        if self.counter > self.reload_rate:
            if self.gun == "ar":
                pygame.mixer.Sound.play(AR)
                b = Bullet(self.x+16,self.y+16,self.player.x+16,self.player.y+16,"enemy")
            elif self.gun == "smg":
                pygame.mixer.Sound.play(AR)
                b = Bullet(self.x+16,self.y+16,self.player.x+16,self.player.y+16,"enemy")
            elif self.gun == "shotgun":
                pygame.mixer.Sound.play(SHOTGUN)
                bullet = Bullet(self.rect.x+16,self.rect.y+16,self.player.x,self.player.y,"enemy")
                bullet = Bullet(self.rect.x+16,self.rect.y+16,self.player.x,self.player.y+20,"enemy")
                bullet = Bullet(self.rect.x+16,self.rect.y+16,self.player.x,self.player.y-20,"enemy")
                bullet = Bullet(self.rect.x+16,self.rect.y+16,self.player.x+20,self.player.y,"enemy")
                bullet = Bullet(self.rect.x+16,self.rect.y+16,self.player.x-20,self.player.y,"enemy")
            elif self.gun == "flamethrower":
                pygame.mixer.Sound.play(FLAMETHROWER)
                x_increase = random.randint(-20,20)
                y_increase = random.randint(-20,20)
                flame = Flame(self.rect.x+16,self.rect.y+16,self.player.x+x_increase,self.player.y+y_increase,self,"enemy")
                
            self.counter = 0


    def update(self):
        self.detection += 1
        self.counter += 1
        self.pos = (self.rect.x,self.rect.y)
        player_pos = (self.player.rect.x,self.player.rect.y)
        distance = int(math.sqrt((self.x-self.player.x)**2+(self.y-self.player.y)**2))

        if self.detection > 1:
            self.detection = 0
            if distance < 400:
                los = LOS(self,self.player.x,self.player.y)
                self.detections.append(los)
                
        self.can_see = False
        for los in self.detections:
            if los.rect.colliderect(self.player.rect):
                self.can_see = True

        for bullet in bullets:
            if bullet.master == "player":
                distance = int(math.sqrt((self.x-bullet.org_x)**2+(self.y-bullet.org_y)**2))
                if distance < 200 and self.player.gun != "flamethrower":
                    self.seen = True
                elif distance < 50 and self.player.gun == "flamethrower":
                    self.seen = True
                    
        
        if self.can_see and distance < 400:
            self.has_los()

        if self.seen == True:
            self.move_x = 0
            self.move_y = 0
            self.move(self.player)

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.rect.x <= wall.rect.x:
                    self.change_x = 0
                    self.x -= 2
                if self.rect.x >= wall.rect.x:
                    self.change_x = 0
                    self.x += 2
                if self.rect.y <= wall.rect.y:
                    self.change_y = 0
                    self.y -= 2
                if self.rect.y >= wall.rect.y:
                    self.change_y = 0
                    self.y += 2

        self.x += self.move_x
        self.y += self.move_y
        self.rect.x = self.x
        self.rect.y = self.y

class LOS(pygame.sprite.Sprite):
    """Invisible projectile, used for LOS detection"""
    def __init__(self,master,dest_x,dest_y):
        self.groups = detectors
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = pygame.Surface((10,10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.master = master
        self.x = self.master.x
        self.y = self.master.y

        x_diff = (dest_x+16) - self.x
        y_diff = (dest_y+16) - self.y
        angle = math.atan2(y_diff, x_diff)
        self.change_x = int(math.cos(angle) * 14)
        self.change_y = int(math.sin(angle) * 14)

    def update(self):
        self.x += self.change_x
        self.y += self.change_y
        if self.x > WIDTH or self.x < 0:
            if self in self.master.detections:
                self.master.detections.remove(self)
            self.kill()
        elif self.y > HEIGHT or self.y < 0:
            if self in self.master.detections:
                self.master.detections.remove(self)
            self.kill()
        for wall in walls:
            if wall.rect.colliderect(self.rect):
                if wall.x != 0 and wall.y != 0:
                    if self in self.master.detections:
                        self.master.detections.remove(self)
                    self.kill()
        self.rect.center = (self.x,self.y)
        
        


class Bullet(pygame.sprite.Sprite):
    """Bullet Class"""
    def __init__(self,px,py,dest_x,dest_y,master):
        self.groups = all_sprites, bullets
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = bullet
        self.rect = self.image.get_rect()
        self.x = px
        self.y = py
        self.org_x = px
        self.org_y = py
        self.master = master
        

        if master == "player":
            x_diff = dest_x - CAMERA_X/2
            y_diff = dest_y - CAMERA_Y/2
            degrees = int(math.degrees(math.atan2(CAMERA_X/2-dest_x,CAMERA_Y/2-dest_y)))
            self.image = pygame.transform.rotate(bullet, degrees)
            angle = math.atan2(y_diff, x_diff)
            self.change_x = math.cos(angle) * BULLET_SPEED
            self.change_y = math.sin(angle) * BULLET_SPEED
        elif master == "enemy":
            x_diff = dest_x - px
            y_diff = dest_y - py
            degrees = int(math.degrees(math.atan2(px-dest_x,py-dest_y)))
            self.image = pygame.transform.rotate(bullet, degrees)
            angle = math.atan2(y_diff, x_diff)
            self.change_x = math.cos(angle) * BULLET_SPEED
            self.change_y = math.sin(angle) * BULLET_SPEED


    def update(self):
        self.x += self.change_x
        self.y += self.change_y
        self.rect.center = (self.x,self.y)

class Flame(pygame.sprite.Sprite):
    """Flame Class"""
    def __init__(self,px,py,dest_x,dest_y,player,master):
        self.groups = all_sprites, bullets
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.org_image = flame
        self.rect = self.org_image.get_rect()
        self.x = px
        self.y = py
        self.org_x = px
        self.org_y = py
        self.master = master
        self.player = player
        
        if master == "player":
            x_diff = dest_x - CAMERA_X/2
            y_diff = dest_y - CAMERA_Y/2
            degrees = int(math.degrees(math.atan2(CAMERA_X/2-dest_x,CAMERA_Y/2-dest_y)))
            self.image = pygame.transform.rotate(self.org_image, degrees)
            angle = math.atan2(y_diff, x_diff)
            self.change_x = math.cos(angle) * 10
            self.change_y = math.sin(angle) * 10
        elif master == "enemy":
            x_diff = dest_x - px
            y_diff = dest_y - py
            degrees = int(math.degrees(math.atan2(px-dest_x,py-dest_y)))
            self.image = pygame.transform.rotate(self.org_image, degrees)
            angle = math.atan2(y_diff, x_diff)
            self.change_x = math.cos(angle) * 10
            self.change_y = math.sin(angle) * 10
        self.active = 0

    def update(self):
        self.x += self.change_x
        self.y += self.change_y        
        distance = int(math.sqrt((self.x-self.player.x)**2+(self.y-self.player.y)**2))
        if distance > 100:
            self.active = 1
        if distance > 200 and self.master=="player":
            self.kill()
        if distance > 300 and self.master=="enemy":
            self.kill()
        
        for wall in walls:
            if wall.rect.colliderect(self.rect):
                if wall.x != 0 and wall.y != 0:
                    self.kill()
        if self.x > WIDTH or self.x < 0:
            self.kill()
        elif self.y > HEIGHT or self.y < 0:
            self.kill()

        if self.active:
            col_tiles = [t for t in tiles if t.rect.colliderect(self.rect) and not t.fire_damage]
            for tile in col_tiles:
                tile.fire_damage = True
                fire = Fire(tile.rect.x,tile.rect.y)
            
        self.rect.center = (self.x,self.y)

class Grenade(pygame.sprite.Sprite):
    """Grenade Class"""
    def __init__(self,px,py,dest_x,dest_y,player,master):
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = grenade
        self.rect = self.image.get_rect()
        self.x = px
        self.y = py
        self.org_x = px
        self.org_y = py
        self.player = player
        self.master = master
        x_diff = dest_x - CAMERA_X/2
        y_diff = dest_y - CAMERA_Y/2
        degrees = int(math.degrees(math.atan2(CAMERA_X/2-dest_x,CAMERA_Y/2-dest_y)))
        self.image = pygame.transform.rotate(grenade, degrees)
        angle = math.atan2(y_diff, x_diff)
        self.change_x = math.cos(angle) * 10
        self.change_y = math.sin(angle) * 10
        self.timer = 0

    def explode(self):
        item = Item(self.x-32,self.y-32,crater)
        for wall in walls:
            distance = int(math.sqrt((self.x-wall.rect.x)**2+(self.y-wall.rect.y)**2))
            if distance < 50:
                item = Item(wall.rect.x,wall.rect.y,exploded2)
                for i in range(10):
                    part = Particle(wall.rect.x,wall.rect.y)
                wall.kill()
        for sprite in all_sprites:
            if sprite.__class__.__name__ == "Enemy":
                distance = int(math.sqrt((self.x-sprite.rect.x)**2+(self.y-sprite.rect.y)**2))
                if distance < 100:
                    pygame.mixer.Sound.play(enemy_killed)
                    item = Item(sprite.x,sprite.y,enemy_exploded)
                    self.kill()
                    sprite.kill()
                    KILLED.append(sprite)
                    self.player.ammo += 5
                    self.player.grenade_ammo += 0.5

                elif 100 < distance < 200:
                    sprite.seen = True
                                        
        for tile in tiles:
            distance = int(math.sqrt((self.x-tile.rect.x)**2+(self.y-tile.rect.y)**2))
            if distance < 50:
                item = Item(tile.rect.x,tile.rect.y,exploded)
                flame = Fire(tile.rect.x,tile.rect.y)
        pygame.mixer.Sound.play(grenade_sound)
        self.kill()

    def update(self):
        self.timer += 1
        if self.timer > 20:
            EXPLOSIONS.append(1)
            self.explode()
        
        for wall in walls:
            if self.rect.colliderect(wall.rect) and self.timer > 1:
                if self.rect.x <= wall.rect.x:
                    self.rect.x -= 5
                if self.rect.x >= wall.rect.x:
                    self.rect.x += 5
                if self.rect.y <= wall.rect.y:
                    self.rect.y -= 5
                if self.rect.y >= wall.rect.y:
                    self.rect.y += 5

                self.change_x = 0
                self.change_y = 0

        self.x += self.change_x
        self.y += self.change_y
        self.rect.center = (self.x,self.y)
            

class Wall(pygame.sprite.Sprite):
    """Wall class"""
    def __init__(self,x,y,TYPE):
        self.x = x
        self.y = y
        self.groups = all_sprites, walls

        pygame.sprite.Sprite.__init__(self, self.groups)
        if TYPE == 1:
            self.image = wall
        elif TYPE == 2:
            self.image = wall2
        elif TYPE == 3:
            self.image = sofa
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Item(pygame.sprite.Sprite):
    """Item Class"""
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self, items)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Fire(pygame.sprite.Sprite):
    """Fire class"""
    def __init__(self,x,y):
        self.x = x
        self.y = y
        groups = items,bullets
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = fire
        self.fire = fire
        self.fire2 = fire2
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.timer = 100
        self.counter = 0
        self.master = "neutral"

    def update(self):
        self.timer -= 1
        if self.timer < 0:
            for tile in tiles:
                if self.rect.colliderect(tile.rect):
                    tile.kill()
            self.kill()
        
        if self.counter > 5:
            if OPTIONS[0]:
                smoke = Smoke(self.rect.x+16,self.rect.y+16)
        if self.counter > 10:
            if self.image == self.fire:
                self.image = self.fire2
            elif self.image == self.fire2:
                self.image = self.fire
        if self.counter > 25:
            self.counter = 0
            rand = random.randint(1,4)
            if rand == 1:
                for tile in tiles:
                    distance = int(math.sqrt((self.rect.x-tile.rect.x)**2+(self.rect.y-tile.rect.y)**2))
                    if distance < 100 and not tile.fire_damage:
                        fire = Fire(tile.rect.x,tile.rect.y)
                        tile.fire_damage = True
                        return 0       
        self.counter += 1

class Smoke(pygame.sprite.Sprite):
    """Smoke class"""
    def __init__(self,x,y):
        groups = all_sprites
        pygame.sprite.Sprite.__init__(self, groups)
        size = random.randint(5,10)
        self.image = pygame.Surface((size,size)).convert()
        rnd = random.randint(1,2)
        if rnd == 1:
            self.image.fill(GREY)
        elif rnd == 2:
            self.image.fill(GREY2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 50

    def update(self):
        self.timer -= 1
        if self.timer < 0:
            self.kill()
            return 0
        self.rect.x += random.uniform(-1,1)
        self.rect.y += random.uniform(-1,1)

class Particle(pygame.sprite.Sprite):
    """Particle class"""
    def __init__(self,x,y):
        groups = all_sprites
        pygame.sprite.Sprite.__init__(self, groups)
        size = random.randint(5,10)
        self.image = pygame.Surface((size,size)).convert()
        rnd = random.randint(1,2)
        if rnd == 1:
            self.image.fill(GREY)
        else:
            self.image.fill(GREY2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = random.randint(-5,5)
        self.change_y = random.randint(-5,5)
        self.timer = random.randint(1,100)
        self.end = 0

    def update(self):
        self.timer -= 1
        if self.timer < 0:
            self.change_x = 0
            self.change_y = 0
            self.end = 1
            return 0

        if not self.end:
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if self.rect.x <= wall.rect.x:
                        self.rect.x -= 10
                    if self.rect.x >= wall.rect.x:
                        self.rect.x += 10
                    if self.rect.y <= wall.rect.y:
                        self.rect.y -= 10
                    if self.rect.y >= wall.rect.y:
                        self.rect.y += 10

                    self.change_x = -(self.change_x+random.randint(-20,20))*0.25
                    self.change_y = -(self.change_y+random.randint(-20,20))*0.25
                    
        self.rect.x += self.change_x
        self.rect.y += self.change_y


class Tile(pygame.sprite.Sprite):
    """Tile Class"""
    def __init__(self,x,y,TYPE):
        self.x = x
        self.y = y
        self.groups = tiles
        self.fire_damage = False
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
            self.image = black
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        

class Gore(pygame.sprite.Sprite):
    """Item Class"""
    def __init__(self,x,y,bullet):
        self.x = x
        self.y = y
        self.dis_x = random.randint(-50,50)
        self.dis_y = random.randint(-50,50)
        self.d_x = self.x + self.dis_x
        self.d_y = self.y + self.dis_y
        pygame.sprite.Sprite.__init__(self, items)
        n = random.randint(1,3)
        if n == 1:
            self.org_image = gore1
        elif n == 2:
            self.org_image = gore2
        elif n == 3:
            self.org_image = gore3
        self.image = self.org_image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        degrees = int(math.degrees(math.atan2(x-self.d_x,y-self.d_y)))
        self.image = pygame.transform.rotate(self.org_image, degrees)
        angle = math.atan2(x-self.d_x,y-self.d_y)
        self.change_x = bullet.change_x + random.randint(-15,15)
        self.change_y = bullet.change_y + random.randint(-15,15)
        self.distance = random.randint(1,75)
        self.counter = 0
        self.blood = []
        self.end = False

    def update(self):
        if self.end:
##            for i in self.blood:
##                i.kill()
##            self.kill()
            return 0
        
        if not self.end:
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if self.rect.x <= wall.rect.x:
                        self.rect.x -= 10
                    if self.rect.x >= wall.rect.x:
                        self.rect.x += 10
                    if self.rect.y <= wall.rect.y:
                        self.rect.y -= 10
                    if self.rect.y >= wall.rect.y:
                        self.rect.y += 10

                    self.change_x = -(self.change_x+random.randint(-20,20))*0.25
                    self.change_y = -(self.change_y+random.randint(-20,20))*0.25
                

        if self.counter > self.distance:
            self.end = True
            self.change_x = 0
            self.change_y = 0

        if self.change_y != 0 or self.change_y != 0:
            self.counter += 1
            if self.counter % random.randint(5,20) == 0:
                item = Item(self.rect.x,self.rect.y,blood)
                self.blood.append(item)
                            
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        

class Node(pygame.sprite.Sprite):
    """Node Class"""
    def __init__(self,x,y,TYPE):
        self.x = x
        self.y = y
        self.groups = nodes
        self.TYPE = TYPE
        self.chosen = False
        pygame.sprite.Sprite.__init__(self, self.groups)
        if DEV == 1:
            if TYPE == 1:
                self.image = left
            elif TYPE == 2:
                self.image = right
            elif TYPE == 3:
                self.image = up
            elif TYPE == 4:
                self.image = down
            self.rect = self.image.get_rect()
            self.chosen = True
        else:
            self.image = pygame.Surface((32,32))
            self.rect = self.image.get_rect()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def update(self):
        if self.chosen == False:
            for tile in tiles:
                dist = int(math.sqrt((self.rect.x-tile.rect.x)**2+(self.rect.y-tile.rect.y)**2))
                if dist <= 32:
                    self.image = tile.image
                    self.chosen = True
        for sprite in ENEMIES:
            if sprite.seen == False:
                image = sprite.org_image
                if self.rect.colliderect(sprite.rect):
                    if self.TYPE == 1:
                        sprite.move_y = 0
                        sprite.move_x = -1
                        degrees = int(math.degrees(math.atan2(sprite.x-1000,sprite.y)))
                        
                        sprite.image = pygame.transform.rotate(image, 90)
                    elif self.TYPE == 2:
                        sprite.move_y = 0
                        sprite.move_x = 1
                        degrees = int(math.degrees(math.atan2(sprite.x+1000,sprite.y)))
                        sprite.image = pygame.transform.rotate(image, 270)
                    elif self.TYPE == 3:
                        sprite.move_x = 0
                        sprite.move_y = -1
                        sprite.image = pygame.transform.rotate(image, 0)
                    elif self.TYPE == 4:
                        sprite.move_x = 0
                        sprite.move_y = 1
                        sprite.image = pygame.transform.rotate(image, 180)

class Game():
    """Game Class"""
    def __init__(self):
        self.display = pygame.display.set_mode((CAMERA_X,CAMERA_Y),flags1)
        self.screen_option = 1
        pygame.mixer.stop()
        pygame.mixer.Sound.play(menu_theme, -1)
        self.menu()

    def menu(self):
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        selection = 1
        speed = 0
        up = 0
        down = 0
        while True:
            self.display.blit(menu_background, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(click)
                        if selection == 1:
                            self.level_select()
                        elif selection == 2 and self.screen_option == 1:
                            self.display = pygame.display.set_mode((CAMERA_X,CAMERA_Y),flags2)
                            self.screen_option = 2
                        elif selection == 2 and self.screen_option == 2:
                            self.display = pygame.display.set_mode((CAMERA_X,CAMERA_Y),flags1)
                            self.screen_option = 1
                        elif selection == 3:
                            self.credits()
                        elif selection == 4:
                            pygame.quit()
                            quit()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        up = 1
                        selection -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        down = 1
                        selection += 1
                elif event.type == pygame.KEYUP:
                    speed = 0
                    down = 0
                    up = 0
                    

            if up: speed -= 0.1
            elif down: speed += 0.1
            if speed > 1: speed = 1
            if speed < -1:speed = -1
            selection  += int(speed)
            if selection > 4:
                selection = 1
            elif selection < 1:
                selection = 4

            if selection == 1:
                start = Text(self.display,CAMERA_X-350,150,"START",TITLE2,RED)
                QUIT = Text(self.display,CAMERA_X-350,450,"QUIT",TITLE2,WHITE)
                CREDITS = Text(self.display,CAMERA_X-350,350,"CREDITS/CONTROLS",TITLE2,WHITE)
                if self.screen_option == 1:
                    screen = Text(self.display,CAMERA_X-350,250,"FULLSCREEN",TITLE2,WHITE)
                elif self.screen_option == 2:
                    screen = Text(self.display,CAMERA_X-350,250,"WINDOWED",TITLE2,WHITE)
            elif selection == 2:
                QUIT = Text(self.display,CAMERA_X-350,450,"QUIT",TITLE2,WHITE)
                CREDITS = Text(self.display,CAMERA_X-350,350,"CREDITS/CONTROLS",TITLE2,WHITE)
                start = Text(self.display,CAMERA_X-350,150,"START",TITLE2,WHITE)
                if self.screen_option == 1:
                    screen = Text(self.display,CAMERA_X-350,250,"FULLSCREEN",TITLE2,RED)
                elif self.screen_option == 2:
                    screen = Text(self.display,CAMERA_X-350,250,"WINDOWED",TITLE2,RED)
            elif selection == 3:
                QUIT = Text(self.display,CAMERA_X-350,450,"QUIT",TITLE2,WHITE)
                CREDITS = Text(self.display,CAMERA_X-350,350,"CREDITS/CONTROLS",TITLE2,RED)
                start = Text(self.display,CAMERA_X-350,150,"START",TITLE2,WHITE)
                if self.screen_option == 1:
                    screen = Text(self.display,CAMERA_X-350,250,"FULLSCREEN",TITLE2,WHITE)
                elif self.screen_option == 2:
                    screen = Text(self.display,CAMERA_X-350,250,"WINDOWED",TITLE2,WHITE)
            elif selection == 4:
                QUIT = Text(self.display,CAMERA_X-350,450,"QUIT",TITLE2,RED)
                CREDITS = Text(self.display,CAMERA_X-350,350,"CREDITS/CONTROLS",TITLE2,WHITE)
                start = Text(self.display,CAMERA_X-350,150,"START",TITLE2,WHITE)
                if self.screen_option == 1:
                    screen = Text(self.display,CAMERA_X-350,250,"FULLSCREEN",TITLE2,WHITE)
                elif self.screen_option == 2:
                    screen = Text(self.display,CAMERA_X-350,250,"WINDOWED",TITLE2,WHITE)


            pygame.display.update()
            clock.tick(20)

    def credits(self):
        self.display.blit(cc,(0,0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    return self.menu()
            pygame.display.update()
            clock.tick(20)
            
            

    def level_select(self):
        pygame.mixer.stop()
        pygame.mixer.Sound.play(menu_theme, -1)
        for sprite in all_sprites:
            all_sprites.remove(sprite)
        with open("unlocked.txt","r") as f:
            data = f.read().split("|")

        data.remove(data[-1])
        buttons = {}

        self.display.blit(menu_background2, (0,0))
        custom = Button(self.display,10,10,100,100,"GENERATE",TEXT,BLACK,RED)
        x = 120
        y = 10
        for i,level in enumerate(levels):
            if x > 700:
                x = 10
                y += 110
            level = level.replace(".txt","")
            if level in data:
                level = Button(self.display,x,y,100,100,level,TEXT,BLACK,WHITE)
                buttons[i] = level
                x += 110
            else:
                level = Button(self.display,x,y,100,100,level,TEXT,BLACK,GREY2)
                x += 110

            
                            
        while True:
            MENU = Button(self.display,int(CAMERA_X/2-390),int(CAMERA_Y-110),100,100,"MENU",TEXT,BLACK,WHITE)    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if pygame.mouse.get_pressed()[0]:
                if custom.clicked():
                    pygame.mixer.Sound.play(click)
                    self.load("NEW_MAP.txt")
                    self.update()

                elif MENU.clicked():
                    pygame.mixer.Sound.play(click)
                    return self.menu()

                for i in buttons:
                    level = buttons[i]
                    if level.clicked():
                        pygame.mixer.Sound.play(click)
                        return self.load(levels[i])

            pygame.display.update()
            clock.tick(20)

    def won(self):
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        pygame.mixer.stop()
        pygame.mixer.Sound.play(menu_theme, -1)
        if self.area_name != "NEW_MAP.txt":
            with open("unlocked.txt","r") as f:
                data = f.read(-1).split("|")
                self.area_name = self.area_name.replace(".txt","")
                tmp = str(int(self.area_name[-1])+1)
                next_stage = self.area_name.replace(self.area_name[-1],tmp)
                next_stage = next_stage
                if next_stage not in data:
                    with open("unlocked.txt","a") as f:
                        f.write(next_stage)
                        f.write("|")
                    
                    
        self.display.blit(menu_background2, (0,0))
        MENU = Button(self.display,int(CAMERA_X/2-300),int(CAMERA_Y-200),300,100,"CONTINUE",TEXT,BLACK,WHITE)
        VICTORY = Text(self.display,CAMERA_X/2-100,100,"VICTORY",TITLE,WHITE)
        TIME = Text(self.display,CAMERA_X/2-100,250,"TIME: "+str(int(time.time()-self.org_time)),TITLE2,WHITE)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if pygame.mouse.get_pressed()[0]:
                if MENU.clicked():
                    pygame.mixer.Sound.play(click)
                    return self.level_select()

            pygame.display.update()
            clock.tick(20)

    def load(self,area):
        self.map = []
        for sprite in all_sprites:
            all_sprites.remove(sprite)
        for tile in tiles:
            tiles.remove(tile)
        for wall in walls:
            walls.remove(wall)
        for bullet in bullets:
            bullets.remove(bullet)
        for item in items:
            items.remove(item)
        for node in nodes:
            nodes.remove(node)
        for los in detectors:
            detectors.remove(los)
        for enemy in ENEMIES:
            ENEMIES.remove(enemy)

        if area != "NEW_MAP.txt":
            with open(area) as f:
                for line in f.readlines():
                    self.map.append(line)
            flag = 0
        else:
            self.map = generate_random()
            flag = 1
            
        x = 0
        y = 0
        for layer in self.map:
            for tile in layer.strip():
                if tile == "W":
                    wall = Wall(x,y,1)
                elif tile == "w":
                    wall = Wall(x,y,2)
                elif tile == "s":
                    wall = Wall(x,y,3)
                elif tile == "p":
                    self.player = Player(x,y)
                    index = layer.index(tile)
                    tile = layer[index-1]
                    t = Tile(x,y,int(tile))
                    self.extraction = Item(x*32,y*32,extraction)
                elif tile == "e":
                    enemy = Enemy(x,y,1,rnd=flag)
                    ENEMIES.add(enemy)   
                    index = layer.index(tile)
                    tile = layer[index-1]
                    t = Tile(x,y,int(tile))
                elif tile == "E":
                    enemy = Enemy(x,y,2,rnd=flag)
                    ENEMIES.add(enemy)
                    index = layer.index(tile)
                    tile = layer[index-1]
                    t = Tile(x,y,int(tile))
                elif tile == "S":
                    enemy = Enemy(x,y,3,rnd=flag)
                    ENEMIES.add(enemy)
                    index = layer.index(tile)
                    tile = layer[index-1]
                    t = Tile(x,y,int(tile))
                elif tile == "1":
                    t = Tile(x,y,1)
                elif tile == "2":
                    t = Tile(x,y,2)
                elif tile == "3":
                    t = Tile(x,y,3)
                elif tile == "4":
                    t = Tile(x,y,4)
                elif tile == "5":
                    t = Tile(x,y,5)
                elif tile == "6":
                    t = Tile(x,y,6)
                elif tile == "L":
                    n = Node(x,y,1)
                elif tile == "R":
                    n = Node(x,y,2)
                elif tile == "U":
                    n = Node(x,y,3)
                elif tile == "D":
                    n = Node(x,y,4)
                x += 1
                
            x = 0
            y += 1

        for enemy in ENEMIES:
            enemy.setup(self.player)


        gun_chosen = False
        while not gun_chosen:
            self.display.blit(menu_background2, (0,0))
            title = Text(self.display,CAMERA_X/2-200,100,"Gun Selection",TITLE,WHITE)
            AR = Button(self.display,int(CAMERA_X/2-400),int(CAMERA_Y/2),200,100,"AR",TEXT,BLACK,WHITE)
            FLAMETHROWER = Button(self.display,int(CAMERA_X/2-100),int(CAMERA_Y/2),200,100,"FLAMETHROWER",TEXT,BLACK,WHITE)
            SHOTGUN = Button(self.display,int(CAMERA_X/2+200),int(CAMERA_Y/2),200,100,"SHOTGUN",TEXT,BLACK,WHITE)
            MENU = Button(self.display,int(CAMERA_X/2-100),int(CAMERA_Y/2+200),200,100,"BACK",TEXT,BLACK,WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.Sound.play(click)
                    if AR.clicked():
                        self.player.gun("ar")
                        gun_chosen = True
                    elif SHOTGUN.clicked():
                        self.player.gun("shotgun")
                        gun_chosen = True
                    elif FLAMETHROWER.clicked():
                        self.player.gun("flamethrower")
                        gun_chosen = True
                    elif MENU.clicked():
                        return self.level_select()
                    
            pygame.display.update()
            clock.tick(20)

        self.x_move = 0
        self.y_move = 0
        self.counter = 0
        self.area_name = area
        pygame.mixer.stop()
        pygame.mixer.Sound.play(game_music, -1)
        if area == "level1.txt":
            pygame.mixer.Sound.play(speech)
        self.org_time = time.time()
        self.update()
        

    def collision(self,target):
        if target.__class__.__name__ == "Wall":
            if self.player.rect.colliderect(target.rect):
                if self.player.rect.x <= target.rect.x:
                    self.player.x -= 1
                    if self.x_move == 5:
                        self.x_move = 0
                    if joysticks:
                        self.x_move = 0
                if self.player.rect.x >= target.rect.x:
                    self.player.x += 1
                    if self.x_move == -5:
                        self.x_move = 0
                    if joysticks:
                        self.x_move = 0
                if self.player.rect.y <= target.rect.y:
                    self.player.y -= 1
                    if self.y_move == 5:
                        self.y_move = 0
                    if joysticks:
                        self.y_move = 0
                if self.player.rect.y >= target.rect.y:
                    self.player.y += 1
                    if self.y_move == -5:
                        self.y_move = 0
                    if joysticks:
                        self.y_move = 0

    def bullet_collision(self):
        for bullet in bullets:
            if bullet.x > WIDTH or bullet.x < 0:
                bullet.kill()
                self.grenade = 10
            elif bullet.y > HEIGHT or bullet.y < 0:
                bullet.kill()
                self.grenade = 10
            for wall in walls:
                if wall.rect.colliderect(bullet.rect):
                    if wall.x != 0 and wall.y != 0:
                        bullet.kill()
                        self.grenade = 10
            if bullet.master == "enemy":
                if bullet.rect.colliderect(self.player.rect):
                    pygame.mixer.Sound.play(death_sound)
                    splatter = random.randint(5,20)
                    x_offset = self.player.rect.x-CAMERA_X/2
                    y_offset = self.player.rect.y-CAMERA_Y/2
                    for _ in range(splatter):
                        x = self.player.x + random.randint(1,50)
                        y = self.player.y + random.randint(1,50)
                        item = Item(x,y,blood)
                        self.display.blit(item.image, (item.rect.x-x_offset, item.rect.y-y_offset))
                    self.player.kill()
                    bullet.kill()
                    death = Text(self.display,CAMERA_X/2,CAMERA_Y/2-200,"YOU DIED",TITLE,RED)
                    pygame.display.update()
                    
                    time.sleep(1)
                    for enemy in ENEMIES:
                        ENEMIES.remove(enemy)
                    return self.load(self.area_name)
            elif bullet.master == "player":
                for enemy in ENEMIES:
                    if bullet.rect.colliderect(enemy.rect):
                        pygame.mixer.Sound.play(enemy_killed)
                        splatter = random.randint(5,20)
                        for _ in range(splatter):
                            x = enemy.x + random.randint(1,50)
                            y = enemy.y + random.randint(1,50)
                            item = Item(x,y,blood)
                        for _ in range(10):
                            gore = Gore(enemy.x,enemy.y,bullet)
                        item = Item(x,y,rip)
                        bullet.kill()
                        enemy.kill()
                        ENEMIES.remove(enemy)
                        self.player.ammo += 5
                        self.player.grenade_ammo += 0.5
                        self.grenade = 10
                        surf = pygame.Surface((800,600))
                        surf.set_alpha(50)
                        surf.fill((255,0,0))
                        self.display.blit(surf, (0,0))
                        pygame.display.update()
                        time.sleep(0.02)
            elif bullet.master == "neutral":
                for enemy in ENEMIES:
                    if enemy.TYPE != 4:
                        if bullet.rect.colliderect(enemy.rect):
                            pygame.mixer.Sound.play(enemy_killed)
                            splatter = random.randint(5,20)
                            for _ in range(splatter):
                                x = enemy.x + random.randint(1,50)
                                y = enemy.y + random.randint(1,50)
                                item = Item(x,y,blood)
                            item = Item(x,y,rip)
                            bullet.kill()
                            enemy.kill()
                            ENEMIES.remove(enemy)

                if bullet.rect.colliderect(self.player.rect):
                    pygame.mixer.Sound.play(death_sound)
                    splatter = random.randint(5,20)
                    x_offset = self.player.rect.x-CAMERA_X/2
                    y_offset = self.player.rect.y-CAMERA_Y/2
                    for _ in range(splatter):
                        x = self.player.x + random.randint(1,50)
                        y = self.player.y + random.randint(1,50)
                        item = Item(x,y,blood)
                        self.display.blit(item.image, (item.rect.x-x_offset, item.rect.y-y_offset))
                    self.player.kill()
                    bullet.kill()
                    death = Text(self.display,CAMERA_X/2,CAMERA_Y/2-200,"YOU DIED",TITLE,RED)
                    pygame.display.update()
                    
                    time.sleep(1)
                    for enemy in ENEMIES:
                        ENEMIES.remove(enemy)
                    return self.load(self.area_name)

    def paused(self):
        pause = True
        while pause:
            self.display.blit(paused_image, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = False
                        

            pygame.display.update()
            clock.tick(20)

            
    def update(self):
        victory = 0
        self.grenade = 0
        old_ammo = self.player.ammo
        old_grenade_ammo = self.player.grenade_ammo
        old_time = int(time.time())
        ammo = Text(self.display,CAMERA_X-110,15,"AMMO: "+str(self.player.ammo),TEXT,GREEN)
        grenade_ammo = Text(self.display,CAMERA_X-110,50,"GRENADES: "+str(int(self.player.grenade_ammo)),TEXT,WHITE)
        TIME = Text(self.display,CAMERA_X-110,75,"TIME: "+str(int(time.time()-self.org_time)),TEXT,WHITE)
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        guns = ["ar","shotgun","flamethrower"]
        switch = guns.index(self.player.gun)
        degrees = 0
        while True:
            self.counter += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.x_move = 0
                        self.y_move = -SPEED

                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.x_move = 0
                        self.y_move = SPEED

                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.y_move = 0
                        self.x_move = -SPEED

                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.y_move = 0
                        self.x_move = SPEED

                    elif event.key == pygame.K_r:
                        return self.load("NEW_MAP.txt")

                    elif event.key == pygame.K_1:
                        self.player.c_gun("ar")
                    elif event.key == pygame.K_2:
                        self.player.c_gun("shotgun")
                    elif event.key == pygame.K_3:
                        self.player.c_gun("flamethrower")

                    elif event.key == pygame.K_SPACE:
                        self.paused()

                    elif event.key == pygame.K_ESCAPE:
                        for enemy in ENEMIES:
                            ENEMIES.remove(enemy)
                        self.menu()

                elif event.type == pygame.KEYUP:
                    self.x_move = 0
                    self.y_move = 0

                elif event.type == pygame.JOYBUTTONDOWN:
                    if controller.get_button(4):
                        switch -= 1
                        if switch > 2:
                            switch = 0
                        if switch < 0:
                            switch = 2
                        self.player.c_gun(guns[switch])
                    elif controller.get_button(5):
                        switch += 1
                        if switch > 2:
                            switch = 0
                        if switch < 0:
                            switch = 2
                        self.player.c_gun(guns[switch])
                    elif controller.get_button(12):
                        for enemy in ENEMIES:
                            ENEMIES.remove(enemy)
                        self.menu()

                    


            if joysticks:
                self.x_move = int(controller.get_axis(0)*5)
                self.y_move = int(controller.get_axis(1)*5)

            for wall in walls:
                if self.player.rect.colliderect(wall.rect):
                    self.collision(wall)

            if len(KILLED) != 0:
                ENEMIES.remove(KILLED[0])
                for i in KILLED:
                    KILLED.remove(i)

            stage_clear = True
            if len(ENEMIES) > 0:
                stage_clear = False

            self.bullet_collision()
              

            self.player.x += self.x_move
            self.player.y += self.y_move
                

            
            all_sprites.update()
            nodes.update()
            detectors.update()
            items.update()


            if joysticks:
                m_x,m_y = pygame.mouse.get_pos()
                m_x += int(controller.get_axis(2)*20)
                m_y += int(controller.get_axis(3)*20)
                pygame.mouse.set_pos((m_x,m_y))

            m_x,m_y = pygame.mouse.get_pos()
            m_x -= 400
            m_y -= 300
            m_x = m_x*0.25
            m_y = m_y*0.25

            if len(EXPLOSIONS) > 0:
                for e in EXPLOSIONS:
                    EXPLOSIONS.remove(e)
                self.grenade = 40
            else:
                x_offset = self.player.rect.x-CAMERA_X/2+m_x
                y_offset = self.player.rect.y-CAMERA_Y/2+m_y

            if self.grenade > 0:
                x_offset= self.player.rect.x-CAMERA_X/2+random.randint(-4,4)+m_x
                y_offset= self.player.rect.y-CAMERA_Y/2+random.randint(-4,4)+m_y
                self.grenade -= 1

            self.display.fill(BLACK)               
            for tile in tiles:
                self.display.blit(tile.image, (tile.rect.x-x_offset, tile.rect.y-y_offset))
            for sprite in nodes:
                self.display.blit(sprite.image, (sprite.rect.x-x_offset, sprite.rect.y-y_offset))
            for item in items:
                self.display.blit(item.image, (item.rect.x-x_offset, item.rect.y-y_offset))
            for sprite in all_sprites:
                self.display.blit(sprite.image, (sprite.rect.x-x_offset, sprite.rect.y-y_offset))

            if DEV:
                for los in detectors:
                    self.display.blit(los.image, (los.rect.x-x_offset, los.rect.y-y_offset))

            cur_fps = int(clock.get_fps())
            fps = Text(self.display,25,15,"FPS: "+str(cur_fps),TEXT,WHITE)
            
            if self.player.ammo != old_ammo:     
                if self.player.ammo == 0:
                    ammo = Text(self.display,CAMERA_X-110,15,"AMMO: "+str(self.player.ammo),TEXT,RED)
                elif self.player.ammo < 20:
                    ammo = Text(self.display,CAMERA_X-110,15,"AMMO: "+str(self.player.ammo),TEXT,ORANGE)
                else:
                    ammo = Text(self.display,CAMERA_X-110,15,"AMMO: "+str(self.player.ammo),TEXT,GREEN)
                old_ammo = self.player.ammo

            if self.player.grenade_ammo  != old_grenade_ammo:
                grenade_ammo = Text(self.display,CAMERA_X-110,50,"GRENADES: "+str(int(self.player.grenade_ammo)),TEXT,WHITE)
                old_grenade_ammo = self.player.grenade_ammo

            if int(time.time()) != old_time:  
                TIME = Text(self.display,CAMERA_X-110,75,"TIME: "+str(int(time.time()-self.org_time)),TEXT,WHITE)
                old_time = int(time.time())

            current_gun = Text(self.display,15,45,"GUN: "+self.player.gun.upper(),TEXT,WHITE)
            
            ammo.update()
            grenade_ammo.update()
            TIME.update()

            if not pygame.display.get_active():
                self.paused()
                
            if stage_clear:
                if victory == 0:
                    victory = 1
                    pygame.mixer.stop()
                    pygame.mixer.Sound.play(victory_music, -1)
                victory = Text(self.display,400,25," GET TO THE EXTRACTION POINT ",TEXT,TURQUOISE)
                for item in items:
                    if item.image == extraction:
                        if item.rect.colliderect(self.player.rect):
                            return self.won()
                
            pygame.display.update()
            clock.tick(60)
        
    

game = Game()
