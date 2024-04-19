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
BLUE_CORNERS = (108,68,15)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE_GRAY = (102, 153, 204)
BLUE = (0,0,255)
LIGHT_PURPLE = (204, 204, 255)
VLIGHT_GREY = (220, 220, 220)
LIGHT_GREY = (211, 211, 211)
SILVER = (192, 192, 192)
GREY = (128, 128, 128)
YELLOW = (255,255,0)
LIGHT_ORANGE= (255, 213, 128)
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
people_images=['man_1.png','man_3.png']
settings_font=pygame.font.SysFont('arial',70)
small_font=pygame.font.SysFont(None,68)
smallest_font=pygame.font.SysFont(None,40)
settings_font.set_bold(True)
settings_head=settings_font.render("SETTINGS",True,BLACK)
settings_head_rect=settings_head.get_rect()
settings_head_rect.center=(500,100)
head_list=[]
rev_list=[]
bacteria_images=['bacteria.png','bacteria4.png','bacteria3.png']
maxx=50
for i in range(1,maxx+1):
    menu_head=settings_font.render("MICROBIAL MAYHEM",True,pygame.color.Color(255,255,255))
    menu_head.set_alpha(i+200)
    menu_head_rect=menu_head.get_rect()
    menu_head_rect.center=(500,100)
    head_list.append((menu_head,menu_head_rect))
    rev_list.append((menu_head,menu_head_rect))
rev_list.reverse()
for ele in rev_list:
    head_list.append(ele)
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
end_bg=pygame.transform.scale(get_image('lava.jpg'),(int(5*tile_size/5),int(5*tile_size/5)))
bg=pygame.transform.scale(get_image('bg.png'),(screen_width,screen_height))
coin_img=pygame.transform.scale(get_image('coin.png'),(50,50))
hosp_img=pygame.transform.scale(get_image('hospital.jpeg'),(2*tile_size,2*tile_size))
settings_bg=pygame.transform.scale(get_image('settings_bg.jpeg'),(1000,1000))
dirt_img = pygame.transform.scale(get_image('brown_wood.png'), (tile_size, tile_size))
grass_img = pygame.transform.scale(get_image('brick1.png'), (tile_size, tile_size))
water_img=pygame.transform.scale(get_image('fungi3.png'),(2*tile_size,2*tile_size))
gate_img=pygame.transform.scale(get_image('gate.png'),(tile_size,int(1.5*tile_size)))
gate_img.set_colorkey(BLACK)
gate_rect=None
level_imgs=[]
level_numbers= []
total_lev=6
completed_lev=6
for i in range(1,total_lev+1):
    img=pygame.transform.scale(get_image(f"level{i}.png"),(200,250))
    rect=img.get_rect()
    rect.x=((i-1)%3)*300+100
    rect.y=200+400*((i-1)//3)
    level_imgs.append((img,rect))
    text = small_font.render(f"{i}",True,LIGHT_ORANGE)
    text_rect = text.get_rect()
    text_rect.x = rect.x + 90
    text_rect.y = rect.bottom + 20
    level_numbers.append((text,text_rect))
total_char=6
char_imgs=[]
all=["guy1.png","Idle (1).png","zwalk0.bmp","zwalk0.bmp","Idle (1).png","Idle (1).png"]
for i in range(1,total_char+1):
    img=pygame.transform.scale(get_image(f"char{i}/{all[i-1]}"),(100,100))
    rect=img.get_rect()
    rect.x=i*150-50
    rect.y=600
    char_imgs.append((img,rect))
#ALL GROUPS
enemy_group = pygame.sprite.Group()
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
new_platform_group= pygame.sprite.Group()
boss_group = pygame.sprite.Group()
bacteria_bullet_group = pygame.sprite.Group()

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
    global rows,screen_height,screen_width,intermediate,y_scroll,level_bg,max_down,bg,cols,x_scroll,max_right
    rows=row
    cols=col
    screen_height=tile_size*row
    screen_width=tile_size*col
    intermediate=pygame.surface.Surface((screen_width,screen_height))
    max_down=screen_height-1000
    max_right=screen_width-1000
    y_scroll=max_down
    x_scroll= 0
    bg=pygame.transform.scale(get_image('try_bg2.jpeg'),(screen_width,screen_height))
    
level_data=[{"rows":20,'cols':40,'x':100,'y':450,"mov_tile":[(10,14,0,2),(37,18,2,0)]}
            ,{"rows":60,'cols':39,'x':100,'y':2700,"laser":[50,40],"mov_tile":[(12,60,0,3)]}
            ,{"rows":60,'cols':20,'x':700,'y':400,"mov_tile":[(5,57,0,2)]}
            ,{"rows":20,'cols':60,'x':200,'y':700,"mov_tile":[(27,6,2,0)],"coord_tile":[[(100,700,2),(2300,700,3),(2300,1100,2)],[(350,1100,2),(2500,1100,2),(2500,700,2),(2800,700,2),(2800,200,2),(1500,200,2)],[(400,1100,2),(2850,1100,2),(2850,200,2)]]}
            ,{"rows":40,"cols":40,'x':60,'y':50,"mov_tile":[(12,26,0,2),(36,21,2,0),(38,38,3,0)],"tiles":[80,80,80]}
            ,{"rows":47,'cols':43,'x':50,'y':50}]

class World():
    def __init__(self, data):
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
                elif ele == 3:
                    blob = Enemy(col_pos * tile_size, row_pos * tile_size,"enemy",1,10,10)
                    enemy_group.add(blob)
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
                    volt=Volts(col_pos * tile_size, row_pos * tile_size,get_image('volts.png'))
                    volt_group.add(volt)
                elif ele == 12:
                    spik=spike(col_pos * tile_size, row_pos * tile_size,get_image('virus.png'))
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
                elif ele ==21 :
                    global gate_rect
                    gate_rect= gate_img.get_rect()
                    gate_rect.x = tile_size*col_pos
                    gate_rect.y = tile_size*row_pos+tile_size//2
                elif ele ==22 :
                   boss=Boss(col_pos * tile_size, row_pos * tile_size)
                   boss_group.add(boss)
                col_pos += 1
            row_pos += 1
        if "coord_tile" in level_data[level-1].keys():
            for plats in level_data[level-1]["coord_tile"]:
                moving_platform_group.add(new_platform(plats))

    def draw_world(self, surface):
        for tile in self.tile_list:
            surface.blit(tile[0], tile[1])
          

class bacteria_bullet(pygame.sprite.Sprite):

    def __init__(self, x, y,vel_x,vel_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image('bacteria2.png'),(24,15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = vel_x
        self.velocity_y = vel_y
        bacteria_bullet_group.add(self)
        self.counter = 0 
    def update(self):
        self.counter+= 1
        for tilee in world.tile_list:
            if tilee[1].colliderect(self):
                self.kill()
        if self.counter >2 :
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y
            self.counter = 0 

class Boss(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image('bacteria.png'),(100,100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 5
        self.velocity_y = -5
        self.last_shoot = 0
        self.health = 400
        self.counter = 0
        boss_group.add(self)

    def update(self):
        self.last_shoot+=1
        self.counter += 1
        if self.counter>20:
            if self.velocity_x>0:
                if self.velocity_y>0:
                    self.velocity_y = -self.velocity_y
                    self.counter = 0 
                else :
                    self.velocity_x = -self.velocity_x
                    self.velocity_y = - self.velocity_y
                    self.counter = 0
            else :
                if self.velocity_y>0:
                    self.velocity_y = -self.velocity_y
                    self.counter = 0 
                else :
                    self.velocity_x = -self.velocity_x
                    self.velocity_y = - self.velocity_y
                    self.counter = 0

        if self.last_shoot==30:
            self.last_shoot = 0 
            create = bacteria_bullet(self.rect.x + 100, self.rect.y,20,0)
            bacteria_bullet_group.add(create)
            create = bacteria_bullet(self.rect.x + 100, self.rect.y+50,20,15)
            bacteria_bullet_group.add(create)
            create = bacteria_bullet(self.rect.x + 50, self.rect.y+100,15,20)
            bacteria_bullet_group.add(create)
            create = bacteria_bullet(self.rect.x, self.rect.y + 100,0,20)
            bacteria_bullet_group.add(create)
            create = bacteria_bullet(self.rect.x-50, self.rect.y + 100,-15,20)
            bacteria_bullet_group.add(create)
            create = bacteria_bullet(self.rect.x-100, self.rect.y + 50,-20,15)
            bacteria_bullet_group.add(create)
            create = bacteria_bullet(self.rect.x - 100, self.rect.y,-20,0)
            bacteria_bullet_group.add(create)
            create = bacteria_bullet(self.rect.x - 50, self.rect.y-100,-15,-20)
            bacteria_bullet_group.add(create)
            create = bacteria_bullet(self.rect.x - 100, self.rect.y-50,-20,-15)
            bacteria_bullet_group.add(create)
            create = bacteria_bullet(self.rect.x, self.rect.y - 100,0,-20)
            bacteria_bullet_group.add(create)
            create = bacteria_bullet(self.rect.x+50, self.rect.y - 100,15,-20)
            bacteria_bullet_group.add(create)
            create = bacteria_bullet(self.rect.x+100, self.rect.y - 50,20,-15)
            bacteria_bullet_group.add(create)
            for _ in range(4):
                angle = random.uniform(0, 2 * math.pi)  
                velocity = 25
                vel_xx = velocity * math.cos(angle)
                vel_yy = velocity * math.sin(angle)
                create = bacteria_bullet(self.rect.x, self.rect.y, vel_xx, vel_yy)
                bacteria_bullet_group.add(create)
        else :
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y     
        for sanit in sanitizer_bullet_group:
            if self.rect.colliderect(sanit.rect):
                self.health -= 20
        if self.health <= 0:
            self.kill()

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
        self.alpha=181
        self.does=False
        self.dec=True
    
    def draw_btn(self):
        if not self.does:
            if(self.dec):
                self.alpha-=2
                if self.alpha<=181:
                    self.dec=False
            else:
                self.alpha+=2
                if self.alpha>=245:
                    self.dec=True
            self.image.set_alpha(self.alpha)
        screen.blit(self.image,self.image_rect)

    def update(self):
        key = pygame.mouse.get_pressed()
        x,y = pygame.mouse.get_pos()
        if self.image_rect.collidepoint(x,y):
            self.image.set_alpha(255)
            self.does=True
        else:
            self.does=False
        if key[0] and not self.click:
            self.click=True
            if self.does:
                return True
        elif not key[0]:
            self.click=False
        return False
    
play_btn = Btn(300,300,400,150,'play.jpg')
settings_btn=Btn(300,480,400,150,'settings.jpg')   
quit_btn = Btn(300,660,400,150,'quit.jpg')
back_btn = Btn (50,50,50,50,'back.png')
start_btn = Btn (400,800,200,120,'start.png')

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
        pygame.draw.circle(screen,BLACK,(self.rect.x+self.rect.width*self.val,int(self.rect.y+self.rect.height//2)),int(self.height//2)+5)
    
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

class new_platform(pygame.sprite.Sprite):
    def __init__(self,list):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image('white_tile.png'),(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = list[0][0]
        self.rect.y = list[0][1]
        self.list=list
        self.next=1
        hyp=math.hypot(list[1][0]-list[0][0],list[1][1]-list[0][1])
        self.x_direction=(list[1][0]-list[0][0])/hyp
        self.y_direction=(list[1][1]-list[0][1])/hyp
        self.x_speed=int(list[0][2]*self.x_direction)
        self.y_speed=int(list[0][2]*self.y_direction)
        if self.x_direction>0:
            self.x_direction=1
        else:
            self.x_direction=-1
            self.x_speed=-self.x_speed
        if self.y_direction>0:
            self.y_direction=1
        else:
            self.y_direction=-1
            self.y_speed=-self.y_speed
        
    def update(self):
        self.rect.x += self.x_speed*self.x_direction
        self.rect.y += self.y_speed*self.y_direction
        next=self.next
        if abs(self.rect.x-self.list[next][0])<2 and abs(self.rect.y-self.list[next][1])<2:
            next+=1
            if(next==len(self.list)):
                self.kill()
                return
            self.rect.x=self.list[next-1][0]
            self.rect.y=self.list[next-1][1]
            hyp=math.hypot(self.list[next][0]-self.list[next-1][0],self.list[next][1]-self.list[next-1][1])
            self.x_direction=(self.list[next][0]-self.list[next-1][0])/hyp
            self.y_direction=(self.list[next][1]-self.list[next-1][1])/hyp
            self.next=next
            self.x_speed=self.x_direction*self.list[next-1][2]
            self.y_speed=self.y_direction*self.list[next-1][2]
            if self.x_direction>0:
                self.x_direction=1
            else:
                self.x_direction=-1
                self.x_speed=-self.x_speed
            if self.y_direction>0:
                self.y_direction=1
            else:
                self.y_direction=-1
                self.y_speed=-self.y_speed

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
            health_bar_rect_3 = pygame.Rect(200,0, 2*vaccine_health, 50)
            pygame.draw.rect(screen, LIGHT_GREY, health_bar_rect_3)

class face_mask(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.transform.flip(get_image('mask.png'),True,False),(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        face_mask_group.add(self)

    def draw(self):
        screen.blit(self.image, self.rect)

class sanitizer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(get_image('vaccine.jpeg'),(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sanitizer_group.add(self)
    
    def draw(self):
        screen.blit(self.image,self.rect)


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
        self.image = pygame.transform.scale(get_image('sanitizer_gun.png'),(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.taken = 0
        sanitizer_gun_group.add(self)


class Sanitizerbullet(pygame.sprite.Sprite) :

    def __init__(self, x, y,is_right,move_speed,width,height,damage):
        pygame.sprite.Sprite.__init__(self)
        self.image= get_image('sanitizer_drop.png')
        self.image=pygame.transform.scale(self.image,(width,height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_speed= move_speed
        self.damage = damage
        self.calc_direction()

    def kill_me(self):
        self.kill()
    def calc_direction(self):
        mouse_pos = pygame.mouse.get_pos()

        dx, dy = mouse_pos[0]+x_scroll - (self.rect.x+self.rect.width//2), mouse_pos[1]+y_scroll - (self.rect.y+self.rect.height//2)
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

        self.image = pygame.transform.scale(get_image(random.choice(bacteria_images)),(50,50))
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
            if not(imgs[i]=='.DS_Store'):
                img = pygame.transform.scale(get_image(file+imgs[i]), (44, 80))
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
            self.vaccine_health -= 0.01
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
        if mouse[0] and self.sanitizer_bullet_count>0 and self.shoot_ctr==15:
            shot_fx.play()
            self.shoot_ctr=0
            self.sanitizer_bullet_count -=1
            self.shot=True
            if self.direction_r==True :
                bullet_dir = 1
            else :
                bullet_dir = -1
            sanitizer_bullet_group.add(Sanitizerbullet(self.rect.x,self.rect.y+40,bullet_dir,15,20,20,20))
        else:
            self.shoot_ctr=min(15,self.shoot_ctr+1)

            

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
                self.health-=5
                shock_fx.play()
        
        # for moving_tile in moving_platform_group:
        #     if moving_tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
        #         dx = 0
        #         if moving_tile.rect.colliderect(self.rect.x-2*moving_tile.x_direction, self.rect.y, self.width, self.height):
        #             dx=moving_tile.x_direction*moving_tile.x_speed
        #             if(moving_tile.x_direction==1):
        #                 left=True
        #             else:
        #                 right=True
        #     if not (self.rect.x+self.rect.width < moving_tile.rect.x or self.rect.x>moving_tile.rect.x + moving_tile.rect.width):
        #         if moving_tile.rect.bottom+moving_tile.y_direction*moving_tile.y_speed-self.rect.y<2 and self.rect.y+dy<=moving_tile.rect.bottom+moving_tile.y_direction*moving_tile.y_speed:
        #             dy=moving_tile.rect.bottom-self.rect.y-2
        #             self.vel_y=3
        #             up=True
        #         elif moving_tile.rect.top+moving_tile.y_direction*moving_tile.y_speed>=self.rect.top and self.rect.bottom+dy>=moving_tile.rect.top+moving_tile.y_direction*moving_tile.y_speed:
        #             self.rect.bottom=moving_tile.rect.top+moving_tile.y_direction*moving_tile.y_speed-2
        #             if(moving_tile.y_direction==-1):
        #                 dy=-moving_tile.y_speed
        #             else:
        #                 dy=0
        #             dx+=moving_tile.x_speed*moving_tile.x_direction
        #             self.in_air=False
        #             self.jumped=False
        #             down=True
        for moving_tile in moving_platform_group:
            if moving_tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and not (moving_tile.x_speed==0):
                if self.rect.x<moving_tile.rect.x:
                    self.rect.x=moving_tile.rect.x-self.rect.width
                else:
                    self.rect.x=(moving_tile.rect.x+moving_tile.rect.width)
                dx=0
                if moving_tile.rect.colliderect(self.rect.x-moving_tile.x_direction,self.rect.y,self.rect.width,self.rect.height):
                    self.rect.x+=moving_tile.x_direction*moving_tile.x_speed
                    
            if not (self.rect.x+self.rect.width <= moving_tile.rect.x or self.rect.x+dx>=moving_tile.rect.x + moving_tile.rect.width):
                if not (self.rect.top<=moving_tile.rect.top and self.rect.bottom>=moving_tile.rect.bottom):
                    if self.rect.y+dy<moving_tile.rect.y and self.rect.bottom+dy>=moving_tile.rect.y and dy>=0:
                        self.rect.bottom=moving_tile.rect.top-1
                        if(moving_tile.y_direction==-1):
                            dy=-moving_tile.y_speed
                        else:
                            dy=0
                        self.rect.x+=moving_tile.x_speed*moving_tile.x_direction
                        self.vel_y=1
                        self.in_air=False
                        self.jumped=False
                        down=True
                    elif self.rect.y+dy<=moving_tile.rect.bottom and self.rect.bottom+dy>moving_tile.rect.bottom:
                        self.rect.top=moving_tile.rect.bottom+1
                        dy=0
                        self.vel_y=1
                        up=True
                
        for tile in world.tile_list:  
            if tile[0]==water_img and tile[1].colliderect(self.rect.x,self.rect.y+1,self.width,self.height):
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
                    self.vel_y = 1
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
            if hosp.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and key[pygame.K_v]:
                self.vaccine = 1
                self.vaccine_health = 200
                my_hospital_group.remove(hosp)

        for guns in sanitizer_gun_group:
            if guns.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and key[pygame.K_p]:
                pickup_fx.play()
                sanitizer_gun_group.remove(guns)
                self.sanitizer_bullet_count += 20

        for mask in face_mask_group:
            if mask.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and key[pygame.K_p]:
                pickup_fx.play()
                self.mask_protection_time = min(100,self.mask_protection_time+50)
                face_mask_group.remove(mask)

        for sanit in sanitizer_group:
            if sanit.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                pickup_fx.play()
                self.health = min(100,self.health+30)
                sanitizer_group.remove(sanit)

        for monster in bacteria_group:
            if monster.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                bacteria_group.remove(monster)
                if self.mask_protection_time>=40:
                    self.mask_protection_time -= 40
                else :
                    self.health -= (40-self.mask_protection_time)
                    self.mask_protection_time = 0 
                
        for people in people_group.sprites():

            if collision(self.rect.x,self.rect.y,self.rect.width,self.rect.height,people.rect.x+25,people.rect.y+40,people.radii):
                self.health-=1

        for bulett in bacteria_bullet_group:
            if bulett.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                if self.mask_protection_time>=10:
                    self.mask_protection_time -= 10
                else :
                    self.health -= (10-self.mask_protection_time)
                    self.mask_protection_time = 0 
                bacteria_bullet_group.remove(bulett)

        if pygame.sprite.spritecollide(self, bullet_group, True):
                self.health-=5
        if pygame.sprite.spritecollide(self,coin_group,True):
            self.coins+=1
            coin_fx.play()
            
        if pygame.sprite.spritecollide(self,spike_group,False):
                self.health-=3
        
        if self.mask_protection_time>0 :
            self.mask_protection_time -= 0.05
            
        self.rect.x += dx
        self.rect.x=max(0,self.rect.x)
        self.rect.x=min(screen_width,self.rect.x)
        self.rect.y += dy
        self.rect.y=max(0,self.rect.y)
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
        if (up and down)or(left and right) or (self.health<=0) or self.rect.y>screen_height:
            game_over = 1
        
        if self.rect.colliderect(gate_rect):
            game_over=0
            
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
    def __init__(self, x, y,attack_images,speed,health,damage):
        pygame.sprite.Sprite.__init__(self)
        lst=[f for f in os.listdir(attack_images)]
        lst.pop(0)
        lst.sort()
        self.r_imgs=[]
        self.l_imgs=[]

        for img in lst:
            new_img=pygame.transform.scale(get_image(attack_images+"/"+img),(80,60))
            self.l_imgs.append(new_img)
            self.r_imgs.append(pygame.transform.flip(new_img,True,False))
        self.image=self.r_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y-20
        self.attack_counter=0
        self.in_attack=0
        self.attack_imgs = attack_images
        self.index = 0 
        self.attack = False
        self.original_x = x
        self.step=0
        self.move_max=100
        self.move_direction = 1
        self.speed = speed
        self.health = health
        self.damage = damage

    def update(self,player):
        if not self.attack:
            self.attack_counter-=1
            if self.attack_counter<=0 and not ((player.rect.bottom<self.rect.y) or player.rect.top>self.rect.bottom):
                if abs(self.rect.x-player.rect.x)<200:
                    self.attack=True
                    self.step=(self.rect.x-player.rect.x)/4
                    self.attack_counter=30
                    self.attacked=False
        else:
            if self.in_attack==0:
                self.in_attack=4
                if self.index==0:
                    self.in_attack=15
                self.index+=1
                if(self.index==len(self.r_imgs)):
                    self.attack=False
                    self.index=0
                    self.rect.x=self.original_x
                    self.image=self.l_imgs[0]
                else:
                    if(self.step>0):
                        self.image=self.l_imgs[self.index]
                    else:
                        self.image=self.r_imgs[self.index]
                    self.rect.x-=self.step
                    if(self.rect.colliderect(player.rect)) and not self.attacked:
                        player.health-=self.damage
                        self.attacked=True
            else:
                self.in_attack-=1

        for bullett in sanitizer_bullet_group:
            if bullett.rect.colliderect(self.rect):
                    self.health -= 2.5
                    sanitizer_bullet_group.remove(bullett)
        if self.health<=0:
            self.kill()

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
        self.image= pygame.transform.scale(self.image,(int(3.8*tile_size),tile_size))
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
        self.i=0
        self.player_num=0
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
        screen.fill(WHITE)
        global page,game_over,level,completed_lev
        if page == 3 :
            if game_over==-1 :
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    page = 1
                intermediate.blit(bg, (0, 0))
                intermediate.blit(gate_img,gate_rect)
                world.draw_world(intermediate)
                moving_platform_group.draw(intermediate)
                moving_platform_group.update()
                self.player.draw_char(intermediate,world)
                # self.draw_grid()
                enemy_group.update(self.player)
                enemy_group.draw(intermediate)
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
                sanitizer_group.draw(intermediate)
                bacteria_group.update(self.player)
                bacteria_group.draw(intermediate)
                new_platform_group.draw(intermediate)
                new_platform_group.update()
                boss_group.update()
                boss_group.draw(intermediate)
                bacteria_bullet_group.update()
                bacteria_bullet_group.draw(intermediate)
                for tile in tile_group.sprites():
                    tile.draww()
                for rot in rotator_group.sprites():
                    if self.draw_rect_angle(pygame.Rect(rot.x,rot.y,100,200),(rot.x,rot.y),rot.angle):
                        game_over=1
                screen.blit(intermediate,(-x_scroll,-y_scroll))
                self.player.draw()
                if(game_over==1):
                    screen.blit(pygame.transform.scale(get_image('game_over0.jpeg'),(400,400)),pygame.Rect(300,300,400,400,))
                elif (game_over==0):
                    screen.blit(pygame.transform.scale(get_image('win.webp'),(400,400)),pygame.Rect(300,300,400,400,))
            elif game_over==1:
                time.sleep(2)
                self.reset()
                page=1
            elif game_over==0:
                victory_fx.play()
                time.sleep(2)
                completed_lev=min(max(level+1,completed_lev),total_lev)
                self.coins+=self.player.coins
                print(self.coins)
                self.reset()
                page=1
        if page==2:
            screen.blit(bg,(0,0))
            back_btn.draw_btn()
            pygame.draw.rect(screen,BLUE_GRAY,pygame.Rect(0,560,1000,180))
            txt=smallest_font.render("SELECT A CHARACTER",True,WHITE)
            txt_rect=txt.get_rect()
            txt_rect.bottom=550
            txt_rect.x=20
            screen.blit(txt,txt_rect)
            if self.change:
                if back_btn.update():
                    click_fx.play()
                    page=1
                    self.change=False
                for i in range (6) :
                    screen.blit(char_imgs[i][0],char_imgs[i][1])
                start_btn.draw_btn()
                img=pygame.transform.scale(get_image(f"char{self.player_num+1}/{all[self.player_num]}"),(200,200))
                img.set_colorkey(BLACK)
                rect=pygame.Rect(400,200,200,200)
                screen.blit(img,rect)
                x,y=pygame.mouse.get_pos()
                mouse=pygame.mouse.get_pressed()
                if not self.click and mouse[0]:
                    self.click=True
                    for i in range(total_char):
                        if char_imgs[i][1].collidepoint((x,y)):
                            click_fx.play()
                            self.player_num=i
                elif not mouse[0]:
                    self.click=False
                if start_btn.update():
                    click_fx.play()
                    self.change=False
                    game_over=-1
                    page=3 
                    lst = os.listdir(f"char{self.player_num+1}")
                    lst.sort()
                    self.player = character(level_data[level-1]['x'],level_data[level-1]['y'] ,f"char{self.player_num+1}/",lst) 
                    pygame.mixer.music.play(-1)
                    load(level)
            else:
                self.change=True  
                time.sleep(0.1)
        if page == 1 :
            screen.blit(bg,(0,0))
            screen.blit(coin_img,(900,50))
            text=small_font.render(f"$ {str(self.coins)}",True,WHITE)
            rect=text.get_rect()
            rect.topright=(880,50)
            screen.blit(text,rect)
            if self.change:
                back_btn.draw_btn()
                if back_btn.update():
                    click_fx.play()
                    page=0
                    self.change=False
                for i in range (completed_lev) :
                    screen.blit(level_imgs[i][0],level_imgs[i][1])
                    screen.blit(level_numbers[i][0],level_numbers[i][1])
                x,y=pygame.mouse.get_pos()
                mouse=pygame.mouse.get_pressed()
                if not self.click and mouse[0]:
                    for i in range(completed_lev):
                        self.click=True
                        if level_imgs[i][1].collidepoint((x,y)):
                            i+=1
                            pygame.mixer.music.load(f"level{i}.wav")
                            click_fx.play()
                            level=i
                            page=2 
                            self.change=False 
                elif not mouse[0]:
                    self.click=False
            else:
                self.change=True  
                time.sleep(0.1)

        if page == 0 :
            if not mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.mixer.music.load('main_theme.wav')
                pygame.mixer.music.play(-1)
            screen.blit(bg,(0,0))
            play_btn.draw_btn()
            quit_btn.draw_btn()
            settings_btn.draw_btn()
            screen.blit(head_list[self.i][0],head_list[self.i][1])
            self.i=(self.i+1)%len(head_list)
            if play_btn.update():
                page=1
                self.click=True
                pygame.mixer.music.fadeout(1000)
                click_fx.play()
            if quit_btn.update():
                with open('info.txt','w') as f:
                    f.write(str(self.coins)+'\n')
                    f.write(str(completed_lev)+'\n')
                    f.close()
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
                time.sleep(0.1)
            
        pygame.display.flip()
        clock.tick(30)

    def reset(self):
        self.i=0
        self.player_num=0
        enemy_group.empty()
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
        bacteria_group.empty()
        moving_platform_group.empty()
        bacteria_bullet_group.empty()
        boss_group.empty()
        sanitizer_group.empty()
        face_mask_group.empty()
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
                    with open('info.txt','w') as f:
                        f.write(str(self.coins)+'\n')
                        f.write(str(completed_lev)+'\n')
                        f.close()
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

with open ('info.txt','r') as file:
    coinz=int(file.readline())
    lev=int(file.readline())
    file.close()
theApp = App()
theApp.coins=coinz
completed_lev=lev
theApp.on_execute()