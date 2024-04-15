import pygame
from math import sqrt
import math
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import os
import time
import random
from pygame.sprite import Group

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
mixer.init()

#ALL COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLACK = (80, 80, 80)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE_GRAY = (102, 153, 204)
LIGHT_PURPLE = (204, 204, 255)
VLIGHT_GREY = (220, 220, 220)
LIGHT_GREY = (211, 211, 211)
SILVER = (192, 192, 192)
GREY = (128, 128, 128)
YELLOW = (255,255,0)
MUSTARD = (255, 191, 0)
LIGHT_BROWN = (196, 164, 132)
BROWN = (111, 78, 55)
SHADOW_BROWN = (111, 70, 40)

#ALL VARS
to_right=False
to_left=False
page  = 0
dirt_tile=None
grass_tile=None
tile_size = 50
rows=40
cols=20
lasers=[]
world=None
clock = pygame.time.Clock()
level=1
screen_width=cols*tile_size
screen_height=rows*tile_size
screen=pygame.display.set_mode((1000,1000))
intermediate=pygame.surface.Surface((screen_width,screen_height))
max_down=screen_height-1000
y_scroll=max_down
max_right=screen_width-1000
x_scroll=max_right
game_over=0
people_images=['man_1.jpeg','man_2.jpeg','man_3.jpeg']
settings_font=pygame.font.SysFont('arial',70)
settings_font.set_bold(True)
settings_head=settings_font.render("SETTINGS",True,BLACK)
settings_head_rect=settings_head.get_rect()
settings_head_rect.center=(500,100)
menu_head=settings_font.render("MICROBIAL MAYHEM",True,LIGHT_BLACK)
menu_head_rect=menu_head.get_rect()
menu_head_rect.center=(500,100)
total_lev=4
#load images
_image_library = {}
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert()
        _image_library[path] = image
    return image

level_bg=pygame.transform.scale(get_image('level_bg.jpg'),(screen_width,screen_width))
end_bg=pygame.transform.scale(get_image('end.png'),(tile_size,tile_size))
bg=pygame.transform.scale(get_image('try_bg2.jpeg'),(screen_width,screen_height))
coin_img=get_image('coin.png')
hosp_img=pygame.transform.scale(get_image('hospital.jpeg'),(2*tile_size,2*tile_size))
settings_bg=pygame.transform.scale(get_image('settings_bg.jpeg'),(1000,1000))
dirt_img = pygame.transform.scale(get_image('brown_wood.png'), (tile_size, tile_size))
grass_img = pygame.transform.scale(get_image('brick1.png'), (tile_size, tile_size))
water_img=pygame.transform.scale(get_image('water.png'),(2*tile_size,2*tile_size))

#ALL GROUPS
blob_group = pygame.sprite.Group()
shooter_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
ninja_group =  pygame.sprite.Group()
tile_group = pygame.sprite.Group()
rotator_group = pygame.sprite.Group()
coin_group=pygame.sprite.Group()
volt_group=pygame.sprite.Group()
spike_group=pygame.sprite.Group()
moving_platform_group = pygame.sprite.Group()
my_hospital_group = pygame.sprite.Group()
people_group = pygame.sprite.Group()
bacteria_group = pygame.sprite.Group()
sanitizer_group =  pygame.sprite.Group()
sanitizer_gun_group =  pygame.sprite.Group()
sanitizer_bullet_group =  pygame.sprite.Group()
face_mask_group = pygame.sprite.Group()

#ADD MUSIC
music_lev=0.5
sound_lev=0.5
coin_fx=pygame.mixer.Sound('coin.wav')
coin_fx.set_volume(sound_lev)
jump_fx=pygame.mixer.Sound('jump.wav')
jump_fx.set_volume(sound_lev)
mixer.music.load('intro.wav')
mixer.music.play()
mixer.music.set_volume(music_lev)
click_fx=pygame.mixer.Sound('click.mp3')
click_fx.set_volume(sound_lev)
pickup_fx=pygame.mixer.Sound('pickup.wav')
pickup_fx.set_volume(sound_lev)
shot_fx=pygame.mixer.Sound('shot.wav')
shot_fx.set_volume(sound_lev)
shock_fx=pygame.mixer.Sound('shock.wav')
shock_fx.set_volume(sound_lev)
victory_fx=pygame.mixer.Sound('victory.wav')
victory_fx.set_volume(sound_lev)
def load_sound_lev():
    coin_fx.set_volume(sound_lev)
    jump_fx.set_volume(sound_lev)
    click_fx.set_volume(sound_lev)
    pickup_fx.set_volume(sound_lev)
    shot_fx.set_volume(sound_lev)
    shock_fx.set_volume(sound_lev)
    victory_fx.set_volume(sound_lev)
    mixer.music.set_volume(music_lev)
    
def load_new(row,col):
    global rows,screen_height,intermediate,y_scroll,level_bg,max_down,bg,cols,x_scroll,max_right
    rows=row
    cols=col
    screen_height=tile_size*row
    screen_width=tile_size*col
    intermediate=pygame.surface.Surface((screen_width,screen_height))
    max_down=screen_height-1000
    max_right=screen_width-1000
    y_scroll=max_down
    x_scroll= 0
    level_bg=pygame.transform.scale(get_image('level_bg.jpg'),(screen_width,screen_width))
    bg=pygame.transform.scale(get_image('try_bg2.jpeg'),(screen_width,screen_height))
    
level_data=[{"rows":40,"cols":40,'x':60,'y':50,"mov_tile":[(12,26,0,2),(36,21,2,0),(38,38,3,0)],"tiles":[80,80,80]}
            ,{"rows":60,'cols':20,'x':100,'y':2700,"laser":[50,40]},
            {"rows":60,'cols':20,'x':750,'y':300,"mov_tile":[(5,57,0,2)]},
            {"rows":20,'cols':60,'x':250,'y':700,"mov_tile":[(58,16,2.5,0)]}]

class World():
    def __init__(self, data):
        global dirt_tile,grass_tile
        load_new(level_data[level-1]["rows"],level_data[level-1]['cols'])
        tile_num=0
        mov_tile=0
        laser_num=0
        self.tile_list = []
        row_pos = 0
        for row in data:
            col_pos = 0
            # x1 = 0 
            for ele in row:
                if ele == 1:
                    img_rect = dirt_img.get_rect()
                    img_rect.x = tile_size*col_pos
                    img_rect.y = tile_size*row_pos
                    self.tile_list.append((dirt_img, img_rect))
                elif ele == 2:
                    img_rect = grass_img.get_rect()
                    img_rect.x = tile_size*col_pos
                    img_rect.y = tile_size*row_pos
                    self.tile_list.append((grass_img, img_rect))
                #add enemies
                elif ele == 3:
                    blob = Enemy(col_pos * tile_size, row_pos * tile_size + 15)
                    blob_group.add(blob)
                elif ele == 4:
                    my_shooter = shooter(col_pos * tile_size, row_pos * tile_size,60,1,10)
                    my_shooter_img_rect = my_shooter.image.get_rect()
                    my_shooter_img_rect.x = tile_size*col_pos
                    my_shooter_img_rect.y = tile_size*row_pos
                    shooter_group.add(my_shooter)
                    self.tile_list.append((my_shooter.image, my_shooter_img_rect))
                elif ele == 5:
                    my_shooter = shooter(col_pos * tile_size, row_pos * tile_size,40,-1,10)
                    my_shooter_img_rect = my_shooter.image.get_rect()
                    my_shooter_img_rect.x = tile_size*col_pos
                    my_shooter_img_rect.y = tile_size*row_pos
                    shooter_group.add(my_shooter)
                    self.tile_list.append((my_shooter.image, my_shooter_img_rect))
                elif ele == 6:
                    laser_group.add(laser(col_pos * tile_size, row_pos * tile_size,1,4,1,level_data[level-1]["laser"][laser_num]))
                    laser_num+=1
                elif ele == 7:
                    ninja_group.add(Ninja(col_pos * tile_size, row_pos * tile_size))
                elif ele == 8:
                    img=pygame.transform.scale(get_image('white_tile.png'),(tile_size,tile_size))
                    tile=tiles(col_pos * tile_size, row_pos * tile_size,img,level_data[level-1]["tiles"][tile_num])
                    tile_num+=1
                    tile_group.add(tile)
                    self.tile_list.append((img,tile.rect))
                elif ele == 9:
                    img=pygame.transform.scale(get_image('zaps.png'),(2*tile_size,4*tile_size))
                    rot=rotator(col_pos * tile_size, row_pos * tile_size,img,10)
                    rotator_group.add(rot)
                elif ele == 10:
                    coin=coins(col_pos * tile_size, row_pos * tile_size)
                    coin_group.add(coin)
                elif ele == 11:
                    volt=Volts(col_pos * tile_size, row_pos * tile_size,get_image('volts.jpg'))
                    volt_group.add(volt)
                elif ele == 12:
                    spik=spike(col_pos * tile_size, row_pos * tile_size,get_image('bacteria-ball.png'))
                    spike_group.add(spik)
                elif ele == 13:
                    my_img = get_image(random.choice(people_images))
                    my_img = pygame.transform.scale(my_img,(50,80))
                    people_group.add(People(col_pos * tile_size, row_pos * tile_size,my_img))
                elif ele == 14:
                    ele=level_data[level-1]['mov_tile'][mov_tile]
                    mov_tile+=1
                    moving_platform_group.add(platform(col_pos * tile_size,ele[0]*tile_size, row_pos * tile_size,ele[1]*tile_size,ele[2],ele[3]))
                elif ele == 15:
                    sanitize=SanitizerGun(col_pos * tile_size, row_pos * tile_size)
                    sanitizer_gun_group.add(sanitize)
                elif ele == 16:
                    maskk=face_mask(col_pos * tile_size, row_pos * tile_size)
                    face_mask_group.add(maskk)
                elif ele == 17:
                    sanitize=sanitizer(col_pos * tile_size, row_pos * tile_size)
                    sanitizer_group.add(sanitize)
                elif ele == 18:
                    hosp=Hospital(col_pos * tile_size, row_pos * tile_size)
                    my_hospital_group.add(hosp)
                elif ele == 19:
                    bact=Bacteria(col_pos * tile_size, row_pos * tile_size,40,20,2)
                    bacteria_group.add(bact)
                elif ele == 20:
                    img_rect = water_img.get_rect()
                    img_rect.x = tile_size*col_pos
                    img_rect.y = tile_size*row_pos
                    self.tile_list.append((water_img, img_rect))
                    
                col_pos += 1
            row_pos += 1

    def draw_world(self, surface):
        for tile in self.tile_list:
            surface.blit(tile[0], tile[1])
            # pygame.draw.rect(surface,tile[1])

class Btn():

    def __init__(self,x,y,width,height,img):
        self.width = width
        self.height= height
        self.image = get_image(img)
        self.image = pygame.transform.scale(self.image,(width,height))
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
        self.click=False
    
    def draw_btn(self):
        screen.blit(self.image,self.image_rect)

    def update(self):
        key = pygame.mouse.get_pressed()
        if key[0] and not self.click:
            self.click=True
            x,y = pygame.mouse.get_pos()
            # print('comes')
            if self.image_rect.collidepoint(x,y):
                # print('does')
                return True
        elif not key[0]:
            self.click=False
        return False
    
start_btn = Btn(250,350,400,200,'play.jpeg')    
quit_btn = Btn(250,550,400,200,'quit.jpeg')
settings_btn=Btn(800,900,100,100,'settings.jpeg')

class toggle():
    def __init__(self,x,y,width,height,ini,text):
        self.width = width
        self.height= height
        self.val=ini
        self.rect=pygame.Rect(x,y,width,height)
        font=pygame.font.Font(None,50)
        self.text=font.render(text,True,WHITE)
        self.text_rect=self.text.get_rect()
        self.text_rect.topright=(x-40,y-5)
        self.click=False
        self.prev=self.rect.x+self.rect.width*self.val
        self.clicked=False

    def draw(self):
        screen.blit(self.text,(self.text_rect))
        pygame.draw.rect(screen,WHITE,self.rect,10)
        pygame.draw.circle(screen,YELLOW,(self.rect.x+self.rect.width*self.val,int(self.rect.y+self.rect.height//2)),int(self.height//2)+5)
        pygame.draw.circle(screen,BLACK,(self.rect.x+self.rect.width*self.val,int(self.rect.y+self.rect.height//2)),int(self.height//2)+5,4)
    
    def update(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0] and not self.clicked:
            x,y = pygame.mouse.get_pos()
            if self.click:
                if x>self.prev:
                    if(x>self.rect.x+self.rect.width):
                        self.val=1
                    else:
                        self.val=(x-self.rect.x)/self.width
                elif x<self.prev:
                    if(x<self.rect.x):
                        self.val=0
                    else:
                        self.val=(x-self.rect.x)/self.width
                self.prev=self.rect.x+self.rect.width*self.val
                    
            elif sqrt((x-self.rect.x-self.rect.width*self.val)**2 + (y-self.rect.y-self.rect.height//2)**2)<self.height//2:
                self.click=True
            else:
                self.clicked=True
        else:
            self.click=False
        if not mouse[0]:
            self.clicked=False

game_sound_btn=toggle(400,400,200,30,0.5,"SOUND")
game_music_btn=toggle(400,500,200,30,0.5,"MUSIC")

class menu_btn():
    def __init__(self,x,y,width,height,text):
        self.rect=pygame.Rect(x,y,width,height)
        self.font=pygame.font.Font(None,40)
        self.text=self.font.render(text,True,LIGHT_BLACK)
        self.text_rect=self.text.get_rect()
        self.text_rect.center=(x+width//2,y+height//2)
        self.click=False
    
    def draw(self):
        pygame.draw.rect(screen,YELLOW,self.rect)
        pygame.draw.circle(screen,YELLOW,(self.rect.x,int(self.rect.y+self.rect.height/2)),self.rect.height/2.0)
        pygame.draw.circle(screen,YELLOW,(self.rect.x+self.rect.width,int(self.rect.y+self.rect.height/2)),self.rect.height/2.0)
        screen.blit(self.text,self.text_rect)
    
    def update(self):
        mouse=pygame.mouse.get_pressed()
        if mouse[0] and not self.click:
            self.click=True
            (x,y)=pygame.mouse.get_pos()
            if self.rect.collidepoint(x,y):
                return True
        elif not mouse[0]:
            self.click=False
        return False
settings_menu=menu_btn(450,700,100,50,"MENU")
        
class platform(pygame.sprite.Sprite):

    def __init__(self,x1,x2,y1,y2,x_speed,y_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image('white_tile.png'),(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.x1= x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.rect.x = x1
        self.rect.y = y1
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.x_direction = 1 
        self.y_direction = 1

    def update(self):
        self.rect.x += self.x_speed * self.x_direction   
        self.rect.y += self.y_speed * self.y_direction 
        if self.rect.left <self.x1  or self.rect.right > self.x2:
            self.x_direction *= -1
        if self.rect.bottom > self.y2  or self.rect.top < self.y1:
            self.y_direction *= -1


class Health_Bar():
    def __init__(self,max_health):
        self.max_health = max_health
        self.current_health = max_health
        self.width = 200
        self.infect = 0 ; 

    def update(self, health,vaccine,vaccine_health):
        self.current_health = health
        health_ratio = self.current_health / self.max_health
        bar_width = int(self.width * health_ratio)
        health_bar_rect_1 = pygame.Rect(0,0, self.width, 50)
        pygame.draw.rect(screen, BLACK, health_bar_rect_1)
        if self.infect==0 :
            health_bar_rect_2 = pygame.Rect(0,0, bar_width, 50)
            pygame.draw.rect(screen, GREEN, health_bar_rect_2)
        else :
            health_bar_rect_2 = pygame.Rect(0,0, bar_width, 50)
            pygame.draw.rect(screen, RED, health_bar_rect_2)
        
        if vaccine==1:
            health_bar_rect_3 = pygame.Rect(200,0, vaccine_health, 50)
            pygame.draw.rect(screen, LIGHT_GREY, health_bar_rect_3)

class face_mask(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.transform.flip(get_image('mask.jpeg'),True,False),(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        face_mask_group.add(self)

    def draw(self):
        screen.blit(self.image, self.rect)

class sanitizer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image('sanitizer.png'),(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sanitizer_group.add(self)


class Hospital(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = hosp_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        my_hospital_group.add(self)

class People(pygame.sprite.Sprite):

    def __init__(self, x, y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y+20
        people_group.add(self)
        self.radii=45
        self.inc=1

    def draww(self):
        pygame.draw.circle(intermediate,WHITE,(self.rect.x+25,self.rect.y+40),self.radii,3)
    
    def update(self):
        if(self.radii==100):
            self.inc=-1
        elif self.radii==45:
            self.inc=1
        self.radii+=self.inc
        self.draww()
        
        

class SanitizerGun(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image('sanitizer_gun.jpeg'),(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.taken = 0
        sanitizer_gun_group.add(self)


class Sanitizerbullet(pygame.sprite.Sprite) :

    def __init__(self, x, y,is_right,move_speed,width,height,damage):
        pygame.sprite.Sprite.__init__(self)
        self.image= get_image('sanitizer_drop.jpeg')
        self.image=pygame.transform.scale(self.image,(width,height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_speed= move_speed
        self.damage = damage
        self.calc_direction()

    def calc_direction(self):
        mouse_pos = pygame.mouse.get_pos()

        dx, dy = mouse_pos[0]+x_scroll - self.rect.x, mouse_pos[1]+y_scroll - self.rect.y
        print(dx,dy)
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist 
        self.direction_x = dx
        self.direction_y = dy
        self.direction = 0
    def update(self):

        if self.direction is not None:
            self.rect.x += self.direction_x * self.move_speed
            self.rect.y += self.direction_y * self.move_speed

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect):
                    self.kill() 

            for bacter in bacteria_group:
                if self.rect.colliderect(bacter.rect):
                    bacter.health -= self.damage
                    self.kill() 

class Bacteria(pygame.sprite.Sprite):
    def __init__(self,x,y,health,distance,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image('bacteria.jpeg'),(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.distance = distance
        self.speed = speed
        self.health = health
        self.counter = 0 
        self.move = False

    def update(self, player):

        if abs(self.rect.y-player.rect.y)<=100 and abs(self.rect.x-player.rect.x)<=200:
            self.move = True
        if self.move:
            dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            dx, dy = dx / dist, dy / dist 
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        if self.health<=0:
            self.kill()

    def draw(self):
        screen.blit(self.image,self.rect)
        
def collision(rleft, rtop, width, height,center_x, center_y, radius):
    rright, rbottom = rleft + width/2, rtop + height/2
    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False 
    for x in (rleft, rleft+width):
        for y in (rtop, rtop+height):
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True 

    return False

class character():
    def __init__(self, x, y,file,imgs):
        self.images_r = []
        self.images_l = []
        self.index = 0
        self.counter = 0
        self.jumped = False
        self.health = 100
        self.health_bar = Health_Bar(100)
        self.vaccine = 0
        self.vaccine_health = 0
        self.sanitizer_bullet_count = 0 
        for i in range(0, len(imgs)):
            img = pygame.transform.scale(get_image(file+imgs[i]), (45, 80))
            img.set_colorkey(BLACK)
            img_flip = pygame.transform.flip(img, True, False)
            self.images_r.append(img)
            self.images_l.append(img_flip)
        self.image = self.images_r[self.index]
        self.in_air = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.vel_y = 0
        self.direction_r = True
        self.coins=0
        self.font=pygame.font.Font(None,40)
        self.coin_img=pygame.transform.scale(coin_img,(tile_size,tile_size))
        self.collide_up=False
        self.collide_down=False
        self.shoot_ctr=0
        self.mask_protection_time = 0
        self.mask_immunity = 0
        
    def jump(self,event):
        if event.key==pygame.K_SPACE:
            if not self.in_air:
                jump_fx.play()
                self.vel_y = -14
                self.in_air = True
            elif not self.jumped:
                jump_fx.play()
                self.vel_y =-14
                self.jumped=True
                             
    def draw_char(self, surface,world):
        global game_over,page
        walk_limit = 8
        key = pygame.key.get_pressed()
        mouse  = pygame.mouse.get_pressed()
        dx = 0
        dy = 0
        col_thresh=10
        up=False
        down=False
        left=False
        right=False
        if self.vaccine:
            self.vaccine_health -= 0.1
            if(self.vaccine_health<0):
                self.vaccine = 0

        if key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            dx = -5
            self.counter += 1
            self.direction_r = False
        if key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
            dx = 5
            self.counter += 1
            self.direction_r = True
        if not (key[pygame.K_LEFT] ^ key[pygame.K_RIGHT]):
            self.index = 0
        if self.counter == walk_limit:
            self.index = (self.index+1) % len(self.images_r)
            self.counter = 0
        if self.direction_r:
            self.image = self.images_r[self.index]
        else:
            self.image = self.images_l[self.index]
        if mouse[0] and self.sanitizer_bullet_count>0 and self.shoot_ctr==10:
            shot_fx.play()
            self.shoot_ctr=0
            self.sanitizer_bullet_count -=1
            self.shot=True
            if self.direction_r==True :
                bullet_dir = 1
            else :
                bullet_dir = -1
            sanitizer_bullet_group.add(Sanitizerbullet(self.rect.x,self.rect.y+40,bullet_dir,5,20,20,20))
        else:
            self.shoot_ctr=min(10,self.shoot_ctr+1)

            

        dy = self.vel_y
        self.vel_y = min(10, self.vel_y+1)
        
        for volt in volt_group.sprites():
            if self.rect.colliderect(volt.rect):
                if(self.rect.bottom>=volt.rect.top+10):
                    dy=-30
                    self.vel_y=-10
                elif self.rect.top>=volt.rect.bottom-10:
                    dy=30
                    self.vel_y=5
                if self.rect.x>=volt.rect.x+volt.rect.width-20:
                    dx=30
                elif self.rect.x+self.rect.width<=volt.rect.x+20:
                    dx=-30
                self.health-=5
                shock_fx.play()
        
        for moving_tile in moving_platform_group:
            if moving_tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if moving_tile.rect.colliderect(self.rect.x-2*moving_tile.x_direction, self.rect.y, self.width, self.height):
                    dx=moving_tile.x_direction*moving_tile.x_speed
                    if(moving_tile.x_direction==1):
                        left=True
                    else:
                        right=True
            if not (self.rect.x+self.rect.width < moving_tile.rect.x or self.rect.x>moving_tile.rect.x + moving_tile.rect.width):
                if moving_tile.rect.bottom+moving_tile.y_direction*moving_tile.y_speed-self.rect.y<2 and self.rect.y+dy<=moving_tile.rect.bottom+moving_tile.y_direction*moving_tile.y_speed:
                    dy=moving_tile.rect.bottom-self.rect.y
                    self.vel_y=0
                    up=True
                if moving_tile.rect.top>=self.rect.bottom and self.rect.bottom+dy>=moving_tile.rect.top:
                    self.rect.bottom=moving_tile.rect.top-2
                    if(moving_tile.y_direction==-1):
                        dy=-moving_tile.y_speed
                    else:
                        dy=0
                    dx+=moving_tile.x_speed*moving_tile.x_direction
                    self.in_air=False
                    self.jumped=False
                    down=True
            
        for tile in world.tile_list:  
            if tile[0]==water_img and tile[1].colliderect(self.rect):
                self.health=0
                game_over=1
                return
            
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            elif tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air=False
                    self.jumped=False
            if abs(tile[1].x-self.rect.x-self.rect.width)<2 and not(self.rect.y>tile[1].bottom or self.rect.bottom<tile[1].y):
                right=True
            if abs(tile[1].x+tile[1].width-self.rect.x)<2 and not(self.rect.y>tile[1].bottom or self.rect.bottom<tile[1].y):
                left=True
            if abs(tile[1].bottom-self.rect.y)<2 and not(self.rect.x>tile[1].x+tile[1].width or self.rect.x+self.rect.width<tile[1].x):
                up=True
            if abs(tile[1].y-self.rect.bottom)<2 and not(self.rect.x>tile[1].x+tile[1].width or self.rect.x+self.rect.width<tile[1].x):
                down=True
        
        for hosp in my_hospital_group:
            if hosp.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.vaccine = 1
                self.vaccine_health = 200

        for guns in sanitizer_gun_group:
            if guns.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and key[pygame.K_p]:
                pickup_fx.play()
                sanitizer_gun_group.remove(guns)
                self.sanitizer_bullet_count +=40
        for mask in face_mask_group:
            if mask.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and key[pygame.K_p]:
                pickup_fx.play()
                self.mask_protection_time+=100
                face_mask_group.remove(mask)
        for sanit in sanitizer_group:
            if sanit.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and key[pygame.K_p] :
                pickup_fx.play()
                # self.mask_protection_time+=100
                sanitizer_group.remove(sanit)
        for monster in bacteria_group:
            if monster.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                bacteria_group.remove(monster)
                self.health -= 20
        
        for people in people_group.sprites():
            if collision(self.rect.x,self.rect.y,self.rect.width,self.rect.height,people.rect.x+25,people.rect.y+40,people.radii):
                self.health-=1

        if pygame.sprite.spritecollide(self, bullet_group, True):
            if self.mask_immunity==0 and self.vaccine==0:
                self.health-=5
        if pygame.sprite.spritecollide(self,coin_group,True):
            self.coins+=1
            coin_fx.play()
            
        if pygame.sprite.spritecollide(self,spike_group,False):
            if self.mask_immunity==0 and self.vaccine==0:
                self.health-=3
        
        if self.mask_protection_time>0 :
            self.mask_protection_time -= 0.2
            self.mask_immunity = 1
        else :
            self.mask_immunity = 0
        if self.health==0:
            game_over = 1
            
        self.rect.x += dx
        self.rect.y += dy
        global y_scroll,x_scroll
        if (self.rect.y<max_down+400):
            y_scroll=max(0,self.rect.y-400)
        else:
            y_scroll=min(max_down,self.rect.y-400)
        if (self.rect.x < max_right+400):
            x_scroll=max(0,self.rect.x-400)
        else:
            x_scroll=min(max_right,self.rect.x-400)
        surface.blit(self.image, self.rect)
        if self.rect.x<0 or self.rect.y<0:
            game_over = 1
        if (up and down)or(left and right) or (self.health<=0):
            game_over = 1
            
    def draw(self):
        self.health_bar.update(self.health,self.vaccine,self.vaccine_health)
        text=self.font.render(str(self.coins),True,WHITE)
        screen.blit(text,(220,20))
        screen.blit(self.coin_img,(250,5))
        
class coins(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image =pygame.transform.scale(coin_img,(tile_size,tile_size))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('blob.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.attack_counter=0
        self.in_attack=False

    def update(self):
        if not self.in_attack:
            self.rect.x += self.move_direction
            self.move_counter += 1
            if abs(self.move_counter) > 50:
                self.move_direction *= -1
                self.move_counter *= -1
        else:
            pass


class bullet(pygame.sprite.Sprite) :
    def __init__(self, x, y,is_right,image,move_speed,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image= get_image(image)
        self.image=pygame.transform.scale(self.image,(width,height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.move_direction=is_right
        self.rect.x = x+self.move_direction*tile_size
        self.rect.y = y
        self.move_speed= move_speed
        
    def update(self):
        dx=self.move_direction*self.move_speed
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, tile_size, tile_size):
                self.kill()
        self.rect.x+=dx 

class Volts(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image =img
        # self.image.set_colorkey(WHITE)
        self.image= pygame.transform.scale(self.image,(3*tile_size,tile_size))
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.image=pygame.transform.flip(self.image,False,True)

class spike(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image =img
        self.image.set_colorkey(BLACK)
        self.size=(int(1.2*tile_size),int(1.2*tile_size))
        self.image= pygame.transform.scale(self.image,self.size)
        self.orig_img=self.image
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.topleft=self.rect.topleft
        self.angle=0
        
    def update(self):
        self.angle=(self.angle+3)%360
        self.image=pygame.transform.rotate(self.orig_img,self.angle)
        self.image=pygame.transform.scale(self.image,self.size)
        new_rect=self.image.get_rect()
        new_rect.topleft=self.rect.topleft
        
class Ninja(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = pygame.image.load('orc/idle2.png').convert()
        self.orig_image= pygame.transform.scale(self.orig_image,(2*tile_size,2*tile_size))
        # self.orig_image.set_colorkey(BLACK)
        self.rect=self.orig_image.get_rect()
        self.image=self.orig_image
        self.rect.x = x
        self.rect.y = y-(tile_size-10)
        self.move_direction = 1
        self.move_counter = 0
        self.index_counter = 0 
        self.index = 0
        self.images_r=[]
        self.images_l=[]
        for i in range(1,5):
            img=get_image(f"orc/attack{i}.jpg")
            # img.set_colorkey(WHITE)
            self.images_r.append(pygame.transform.scale(img,(3*tile_size,2*tile_size)))
            self.images_l.append(pygame.transform.flip(self.images_r[i-1],True,False))
        for i in range(6,8):
            img=get_image(f"orc/attack{i}.jpg")
            # img.set_colorkey(WHITE)
            self.images_r.append(pygame.transform.scale(img,(3*tile_size,2*tile_size)))
            self.images_l.append(pygame.transform.flip(self.images_r[7-i],True,False))
        self.in_attack=False

    def update(self,player):
        global game_over
        if self.in_attack:
            self.move_counter += 1
            if self.move_counter == 20:
                self.index+=1
                self.move_counter=0
            if self.move_direction == 1 : 
                self.image = self.images_r[self.index]
            else :
                self.image = self.images_l[self.index]
            if self.index==3:
                rect=pygame.Rect(self.rect.x-2*tile_size,self.rect.y,tile_size,tile_size)
                if rect.colliderect(player.rect):
                    game_over=1
            if self.index==5:
                self.index=0
                self.in_attack=False
        else:
            self.image=self.orig_image
            if abs(player.rect.y-self.rect.y)<=tile_size:
                if player.rect.x<self.rect.x and self.rect.x-player.rect.x<=tile_size:
                    self.move_direction=-1
                    self.in_attack=True
                elif player.rect.x>self.rect.x and player.rect.x-self.rect.x<=2.5*tile_size:
                    self.move_direction=1
                    self.in_attack=True
        
class rotator(pygame.sprite.Sprite):
    def __init__(self, x, y,image,move_speed):
        pygame.sprite.Sprite.__init__(self)
        image.set_colorkey(BLACK)
        self.image=image
        self.orig=image
        self.origr=self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x=x
        self.y=y
        self.speed=move_speed
        self.counter=0
        self.angle=0
    def blitRotate(self, pos, originPos, angle):
        image_rect = self.orig.get_rect(topleft = (pos[0], pos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        self.image = pygame.transform.rotate(self.orig, angle)
        self.rect = self.image.get_rect(center = rotated_image_center)

    def update(self):
        self.counter+=1
        if self.counter==self.speed:
            self.counter=0
            self.angle=(self.angle+3)%360
        self.blitRotate((self.x,self.y),(self.x,self.y),self.angle)
        
class tiles(pygame.sprite.Sprite):
    def __init__(self, x, y,image,time):
        pygame.sprite.Sprite.__init__(self)
        self.image=image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.time=time
        self.counter=40
        self.font = pygame.font.Font('freesansbold.ttf', 60)
    def draww(self):
        self.counter-=1
        if self.counter==0:
            self.time-=1
            if(self.time==0):
                world.tile_list.pop(world.tile_list.index((self.image,self.rect)))
                self.kill()
            self.counter=40
        text = self.font.render(f"{self.time}", True, WHITE)
        intermediate.blit(text,self.rect)

class shooter(pygame.sprite.Sprite):
    def __init__(self, x, y, shoot_rate,is_right,move_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('shooter.png').convert()
        self.image=pygame.transform.scale(self.image,(tile_size,tile_size))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.move_direction=is_right
        self.rect.x = x
        self.rect.y = y
        self.shoot_counter = 0
        self.rate=shoot_rate
        self.move_speed= move_speed
    def update(self):
        self.shoot_counter += 1
        if self.shoot_counter == self.rate:
            self.shoot_counter=0
            bullet_group.add(bullet(self.rect.x,self.rect.y,self.move_direction,'virus.png',self.move_speed,int(2*tile_size//3),int(2*tile_size//3)))
            
class laser(pygame.sprite.Sprite):
    def __init__(self, x, y,is_right,move_speed,is_up,time):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image('blob.png')
        self.image=pygame.transform.scale(self.image,(tile_size,tile_size))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.move_dir=is_right
        self.move_direction=is_up
        self.rect.x = x
        self.rect.y = y
        self.move_speed= move_speed
        self.move_counter=0
        self.least=self.rect.x+tile_size
        self.time=time
    def update(self,player):
        if self.time==0:
            global game_over
            if self.move_counter==0:
                least=screen_width
                for tile in world.tile_list:
                    if abs(self.rect.y-tile[1][1])<=tile_size//2: 
                        if self.move_dir==1:
                            if tile[1][0]>self.rect.x:
                                least=min(least,tile[1][0])
                        elif (tile[1][0]<=self.rect.x):
                            least=min(least,tile[1][0])
                self.least=least
            rect=pygame.Rect(self.rect.x+tile_size,self.rect.y,self.least-self.rect.x-tile_size,tile_size//2)
            pygame.draw.rect(intermediate,RED,rect)
            if rect.colliderect(player.rect):
                game_over=1
            intermediate.blit(end_bg,(self.least-tile_size,self.rect.y))
                    
            self.move_counter+=1
            if self.move_counter==self.move_speed:
                self.rect.y-=self.move_direction*3
                self.move_counter=0
        else:
            self.time-=1
    
class App():
    def __init__(self):
        self.running = True
        self.size = (1000,1000)
        self.coins=0
        # self.display_surf = pygame.display.set_mode(self.size)
        self.change=False
    def on_init(self):
        self.running = True 

    def draw_grid(self):
        font=pygame.font.Font(None,30)
        for i in range(cols):
            pygame.draw.line(intermediate, WHITE, (
                0+i*tile_size, 0), (0+i*tile_size,screen_height))
            text=font.render(str(i),True,WHITE)
            intermediate.blit(text,pygame.Rect(0+i*tile_size,0,20,20))
        for i in range(rows):
            pygame.draw.line(intermediate, WHITE, (
                0, 0+i*tile_size), (screen_width, 0+i*tile_size))
            text=font.render(str(i),True,WHITE)
            intermediate.blit(text,pygame.Rect(0, 0+i*tile_size,20,20))
    def draw_rect_angle(self,rect, pivot, angle):
        pts = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
        pts = [(pygame.math.Vector2(p) - pivot).rotate(-angle) + pivot for p in pts]
        for i in range(4):
            if self.player.rect.clipline(pts[i],pts[(i+1)%4]):
                return True
        return False
    def on_render(self):
        screen.fill(BLACK)
        global page,game_over,level
        if page == 3 :
            if game_over==-1 :
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    page = 1
                intermediate.blit(bg, (0, 0))
                world.draw_world(intermediate)
                self.player.draw_char(intermediate,world)
                moving_platform_group.update()
                moving_platform_group.draw(intermediate)
                self.draw_grid()
                blob_group.update()
                blob_group.draw(intermediate)
                shooter_group.update()
                shooter_group.draw(intermediate)
                bullet_group.update()
                bullet_group.draw(intermediate)
                laser_group.update(self.player)
                laser_group.draw(intermediate)
                ninja_group.update(self.player)
                ninja_group.update(self.player)
                ninja_group.draw(intermediate)
                tile_group.draw(intermediate)
                rotator_group.draw(intermediate)
                rotator_group.update()
                coin_group.draw(intermediate)
                volt_group.draw(intermediate)
                volt_group.update()
                spike_group.draw(intermediate)
                spike_group.update()
                people_group.update()
                people_group.draw(intermediate)
                my_hospital_group.draw(intermediate)
                sanitizer_gun_group.update(self.player)
                sanitizer_gun_group.draw(intermediate)
                sanitizer_bullet_group.update()
                sanitizer_bullet_group.draw(intermediate)
                face_mask_group.draw(intermediate)
                bacteria_group.update(self.player)
                bacteria_group.draw(intermediate)
                for tile in tile_group.sprites():
                    tile.draww()
                for rot in rotator_group.sprites():
                    if self.draw_rect_angle(pygame.Rect(rot.x,rot.y,100,200),(rot.x,rot.y),rot.angle):
                        game_over=1
                screen.blit(intermediate,(-x_scroll,-y_scroll))
                self.player.draw()
            elif game_over==1:
                self.reset()
                page=1
            elif game_over==0:
                victory_fx.play()
                self.coins+=self.player.coins
                page=1
                self.reset()
        if page==2:
            all=["guy1.png","guy1.png","zwalk0.bmp"]
            screen.blit(level_bg,(0,0))
            if self.change:
                for i in range (1,4) :
                    xx = f"char{i}/"
                    screen.blit(pygame.transform.scale(get_image(xx+all[i-1]),(300,300)),pygame.Rect(((i-1)%2)*500+100,100+500*int((i-1)/2),300,300))
                    char_btn = Btn(((i-1)%2)*500+100,400+500*int((i-1)/2),300,100,f"Level {i}.png")
                    char_btn.draw_btn()
                    if char_btn.update():
                        click_fx.play()
                        pygame.mixer.music.play(-1)
                        game_over=-1
                        page=3 
                        lst = os.listdir(xx)
                        load(level)
                        self.player = character(level_data[level-1]['x'],level_data[level-1]['y'] ,f"char{i}/",lst) 
                        self.change=False
            else:
                self.change=True  
                time.sleep(0.2)
        if page == 1 :
            screen.blit(settings_bg,(0,0))
            if self.change:
                for i in range (1,5) :
                    xx = f"Level {i}.png"
                    screen.blit(pygame.transform.scale(get_image(f"img{i}.png"),(300,300)),pygame.Rect(((i-1)%2)*500+100,100+500*int((i-1)/2),300,300))
                    level_btn = Btn(((i-1)%2)*500+100,400+500*int((i-1)/2),300,100,xx)
                    level_btn.draw_btn()
                    if level_btn.update():
                        pygame.mixer.music.load(f"level{i}.wav")
                        click_fx.play()
                        level=i
                        page=2 
                        self.change=False 
            else:
                self.change=True  
                time.sleep(0.2)

        if page == 0 :
            if not mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.mixer.music.load('main_theme.wav')
                pygame.mixer.music.play(-1)
            screen.blit(settings_bg,(0,0))
            
            start_btn.draw_btn()
            quit_btn.draw_btn()
            settings_btn.draw_btn()
            screen.blit(menu_head,menu_head_rect)
            if start_btn.update():
                page=1
                pygame.mixer.music.fadeout(1000)
                click_fx.play()
            if quit_btn.update():
                pygame.quit()
            if settings_btn.update():
                pygame.mixer.music.pause()
                click_fx.play()
                page=-1
        
        if page==-1:
            global music_lev,sound_lev
            screen.blit(settings_bg,(0,0))
            game_music_btn.draw()
            game_music_btn.update()
            music_lev=game_music_btn.val
            game_sound_btn.draw()
            game_sound_btn.update()
            sound_lev=game_sound_btn.val
            load_sound_lev()
            settings_menu.draw()
            screen.blit(settings_head,settings_head_rect)
            if settings_menu.update():
                click_fx.play()
                page=0
                pygame.mixer.music.unpause()
                time.sleep(0.2)
            
        pygame.display.flip()
        clock.tick(30)

    def reset(self):
        self.__init__()
        blob_group.empty()
        shooter_group.empty()
        bullet_group.empty()
        ninja_group.empty()
        laser_group.empty()
        tile_group.empty()
        rotator_group.empty()
        coin_group.empty()
        volt_group.empty()
        spike_group.empty()
        people_group.empty()
        sanitizer_gun_group.empty()
        sanitizer_bullet_group.empty()
        face_mask_group.empty()
        moving_platform_group.empty()
        self.player.coins=0
        
    def on_execute(self):
        global y_scroll,to_right,to_left
        to_right=False
        to_left=False
        if self.on_init() == False:
            self.running = False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:
                        y_scroll=max(0,y_scroll-30)
                        
                    elif event.button == 5:
                        y_scroll=min(max_down,30+y_scroll)
                elif event.type== pygame.KEYDOWN:
                    if event.key== pygame.K_SPACE:
                        self.player.jump(event)
                
            self.on_render()
            

        pygame.quit()
def load(level):
    global world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

# print(sorted(pygame.font.get_fonts())) 
theApp = App()
theApp.on_execute()
