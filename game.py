import pygame
from pygame.locals import *
import pickle
from os import path
import os
import time
import random

from pygame.sprite import Group
pygame.init()

_image_library = {}
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert()
        _image_library[path] = image
    return image
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
GOLD_YELLOW = (255, 234, 0)
GOLD = (255, 215, 0)
MUSTARD = (255, 191, 0)
LIGHT_BROWN = (196, 164, 132)
BROWN = (111, 78, 55)
SHADOW_BROWN = (111, 70, 40)

page  = 0
dirt_tile=None
grass_tile=None
tile_size = 50
rows=40
cols=20
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
people_images=['man_1.jpeg','man_2.jpeg','man_3.jpeg']
# vertical_platform_group = pygame.sprite.Group()
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
level_bg=pygame.transform.scale(get_image('level_bg.jpg'),(screen_width,screen_width))
end_bg=pygame.transform.scale(get_image('end.png'),(tile_size,tile_size))
bg=pygame.transform.scale(get_image('bg1.jpg'),(screen_width,screen_height))
coin_img=get_image('coin.png')
# end_bg.set_colorkey(BLACK)
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
    bg=pygame.transform.scale(get_image('bg1.jpg'),(screen_width,screen_height))
    
level_data=[{"rows":40,"cols":40,'x':50,'y':50},{"rows":40,'cols':20,'x':50,'y':1800},{"rows":60,'cols':20,'x':50,'y':2800},{"laser":[30,40],"tiles":[60,57,54,30,20],"rows":40,'cols':20,'x':50,'y':1800}]

class World():
    def __init__(self, data):
        global dirt_tile,grass_tile
        load_new(level_data[level-1]["rows"],level_data[level-1]['cols'])
        tile_num=0
        self.tile_list = []
        dirt_img = pygame.transform.scale(
            get_image('brown_wood.png'), (tile_size, tile_size))
        grass_img = pygame.transform.scale(
            get_image('brick1.png'), (tile_size, tile_size))
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
                    laser_group.add(laser(col_pos * tile_size, row_pos * tile_size,1,4,1))
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
                    my_img = pygame.transform.scale(my_img,(50,100))
                    people_group.add(People(col_pos * tile_size, row_pos * tile_size,my_img))
                elif ele == 14:
                    maskk=face_mask(col_pos * tile_size, row_pos * tile_size)
                    face_mask_group.add(maskk)
                elif ele == 15:
                    sanitize=sanitizer(col_pos * tile_size, row_pos * tile_size)
                    sanitizer_group.add(sanitize)
                elif ele == 14:
                    pass
                    
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
        if key[0]:
            x,y = pygame.mouse.get_pos()
            if self.image_rect.collidepoint(x,y) and not self.click:
                self.click=True
        else:
            self.click=False
        return self.click
    
start_btn = Btn(250,350,400,200,'play.jpeg')    
quit_btn = Btn(250,550,400,200,'quit.jpeg')
settings_btn=Btn(800,900,100,100,'quit.jpeg')

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

my_new_platform =platform(100,400,600,600,2,0)
moving_platform_group.add(my_new_platform)
my_new_platform = platform(1200,1800,1050,1050,2,0)
moving_platform_group.add(my_new_platform)
my_new_platform = platform(600,600,900,1300,0,2)
moving_platform_group.add(my_new_platform)
my_new_platform = platform(800,800,200,600,0,2)
moving_platform_group.add(my_new_platform)

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

    def draw(self):
        screen.blit(self.image, self.rect)

class Hospital(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image("hospital.jpeg"),(100,100))  # Load hospital image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        my_hospital_group.add(self)

    def draw(self):
        screen.blit(self.image, self.rect)


class People(pygame.sprite.Sprite):

    def __init__(self, x, y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        people_group.add(self)

    def draw(self):
        screen.blit(self.image, self.rect)

class SanitizerGun(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(get_image('sanitizer_gun.jpeg'),(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.taken = 0
        sanitizer_gun_group.add(self)

my_gun = SanitizerGun(100,200)

class Sanitizerbullet(pygame.sprite.Sprite) :

    def __init__(self, x, y,is_right,move_speed,width,height,damage):
        pygame.sprite.Sprite.__init__(self)
        self.image= get_image('sanitizer_drop.jpeg')
        self.image=pygame.transform.scale(self.image,(width,height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.move_direction=is_right
        self.rect.x = x+self.move_direction*tile_size
        self.rect.y = y
        self.move_speed= move_speed
        self.damage = damage
        
    def update(self):
        dx=self.move_direction*self.move_speed
        for bacteria in bacteria_group:
            if bacteria.rect.colliderect(self.rect.x + dx, self.rect.y, tile_size, tile_size):
                bacteria.health-=self.damage
                self.kill()
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, tile_size, tile_size):
                self.kill()
        self.rect.x+=dx 

class character():
    def __init__(self, x, y,folder,len):
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
        for i in range(1, len+1):
            img = pygame.transform.scale(get_image(f'{folder}/guy{i}.png'), (40, 80))
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
                self.vel_y = -14
                self.in_air = True
            elif not self.jumped:
                self.vel_y =-13
                self.jumped=True
                             
    def draw_char(self, surface,world):
        global game_over,page
        walk_limit = 8
        key = pygame.key.get_pressed()
        dx = 0
        dy = 0
        col_thresh=10
        up=False
        down=False
        left=False
        right=False
        if self.vaccine:
            self.vaccine_health -= 0.04
            if(self.vaccine_health<=0):
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
        if key[pygame.K_s] and self.sanitizer_bullet_count>0 and self.shoot_ctr==10:
            self.shoot_ctr=0
            self.sanitizer_bullet_count -=1
            self.shot=True
            if self.direction_r==True :
                bullet_dir = 1
            else :
                bullet_dir = -1
            sanitizer_bullet_group.add(Sanitizerbullet(self.rect.x+50,self.rect.y+10,bullet_dir,5,20,20,20))
        else:
            self.shoot_ctr=min(10,self.shoot_ctr+1)

            

        dy = self.vel_y
        self.vel_y = min(10, self.vel_y+1)
        for tile in world.tile_list:  
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if(tile[1].x>self.rect.x):
                    right=True
                else:
                    left=True
            elif tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y==0:
                    up=True
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                    up=True
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air=False
                    self.jumped=False
                    down=True
        
        for moving_tile in moving_platform_group:
            if moving_tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if moving_tile.rect.colliderect(self.rect.x-2*moving_tile.x_direction, self.rect.y, self.width, self.height):
                    dx=moving_tile.x_direction*moving_tile.x_speed
                    if(moving_tile.x_direction==1):
                        left=True
                    else:
                        right=True
            if not (self.rect.x+self.rect.width <= moving_tile.rect.x or self.rect.x>=moving_tile.rect.x + moving_tile.rect.width):
                if moving_tile.rect.bottom<self.rect.y and self.rect.y+dy<moving_tile.rect.bottom:
                    dy=moving_tile.rect.bottom-self.rect.y
                    self.vel_y=0
                    up=True
                if moving_tile.rect.top>=self.rect.bottom and self.rect.bottom+dy>=moving_tile.rect.top:
                    self.rect.bottom=moving_tile.rect.top-2
                    dy=0
                    dx+=moving_tile.x_speed*moving_tile.x_direction
                    self.in_air=False
                    self.jumped=False
                    down=True
            
        
        for hosp in my_hospital_group:
            if hosp.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.vaccine = 1
                self.vaccine_health = 200

        for guns in sanitizer_gun_group:
            if guns.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                sanitizer_gun_group.remove(guns)
                self.sanitizer_bullet_count +=5
        for mask in face_mask_group:
            if mask.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.mask_protection_time+=100
                face_mask_group.remove(mask)
        for sanit in sanitizer_group:
            if sanit.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                # self.mask_protection_time+=100
                sanitizer_group.remove(sanit)

        if pygame.sprite.spritecollide(self, bullet_group, True):
            if self.mask_immunity==0:
                self.health-=5
        if pygame.sprite.spritecollide(self,coin_group,True):
            self.coins+=1
        if pygame.sprite.spritecollide(self,volt_group,False) or pygame.sprite.spritecollide(self,spike_group,False):
            if self.mask_immunity==0:
                self.health-=5
        
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
        if (up and down)or(left and right):
            game_over = 1
            
    def draw(self):
        # pygame.draw.rect(screen,WHITE,self.rect,2)
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
        self.size=(int(1.5*tile_size),int(1.5*tile_size))
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

    #   pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)
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
    def __init__(self, x, y,is_right,move_speed,is_up):
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
    def update(self,player):
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
                          
class App():
    def __init__(self):
        self.running = True
        self.size = (1000,1000)
        # self.display_surf = pygame.display.set_mode(self.size)
        self.change=False
    def on_init(self):
        self.running = True 

    def draw_grid(self):
        for i in range(cols):
            pygame.draw.line(intermediate, WHITE, (
                0+i*tile_size, 0), (0+i*tile_size,screen_height))
        for i in range(rows):
            pygame.draw.line(intermediate, WHITE, (
                0, 0+i*tile_size), (screen_width, 0+i*tile_size))
    def draw_rect_angle(self,rect, pivot, angle):
        pts = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
        pts = [(pygame.math.Vector2(p) - pivot).rotate(-angle) + pivot for p in pts]
        for i in range(4):
            if self.player.rect.clipline(pts[i],pts[(i+1)%4]):
                return True
        return False
    def on_render(self):
        global page,game_over,level
        if page == 3 :
            if game_over==-1 :
                screen.fill(BLACK)
                intermediate.blit(bg, (0, 0))
                world.draw_world(intermediate)
                self.player.draw_char(intermediate,world)
                moving_platform_group.update()
                moving_platform_group.draw(intermediate)
                # self.draw_grid()
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
                people_group.draw(intermediate)
                my_hop = Hospital(400,540)
                my_hospital_group.draw(intermediate)
                sanitizer_gun_group.update(self.player)
                sanitizer_gun_group.draw(intermediate)
                sanitizer_bullet_group.update()
                sanitizer_bullet_group.draw(intermediate)
                face_mask_group.draw(intermediate)

                # vertical_platform_group.update()
                # vertical_platform_group.draw(intermediate)

                for tile in tile_group.sprites():
                    tile.draww()
                for rot in rotator_group.sprites():
                    if self.draw_rect_angle(pygame.Rect(rot.x,rot.y,100,200),(rot.x,rot.y),rot.angle):
                        game_over=1
                screen.blit(intermediate,(-x_scroll,-y_scroll))
                self.player.draw()
            elif game_over==1:
                screen.fill(BLACK)
                self.reset()
                page=1
        if page==2:
            screen.fill(BLACK)
            screen.blit(level_bg,(0,0))
            if self.change:
                for i in range (1,3) :
                    xx = f"char{i}"
                    screen.blit(pygame.transform.scale(get_image(xx+"/guy1.png"),(300,300)),pygame.Rect(((i-1)%2)*500+100,100+500*int((i-1)/2),300,300))
                    char_btn = Btn(((i-1)%2)*500+100,400+500*int((i-1)/2),300,100,f"Level {i}.png")
                    char_btn.draw_btn()
                    if char_btn.update():
                        game_over=-1
                        page=3 
                        lst = os.listdir(xx) # your directory path
                        num = len(lst)-1
                        load(level)
                        self.player = character(level_data[level-1]['x'],level_data[level-1]['y'] ,xx,num) 
                        self.change=False
            else:
                self.change=True  
                time.sleep(0.2)
        if page == 1 :
            screen.fill(BLACK)
            screen.blit(level_bg,(0,0))
            if self.change:
                for i in range (1,5) :
                    xx = f"Level {i}.png"
                    screen.blit(pygame.transform.scale(get_image(f"img{i}.png"),(300,300)),pygame.Rect(((i-1)%2)*500+100,100+500*int((i-1)/2),300,300))
                    level_btn = Btn(((i-1)%2)*500+100,400+500*int((i-1)/2),300,100,xx)
                    level_btn.draw_btn()
                    if level_btn.update():
                        level=i
                        page=2 
                        self.change=False 
            else:
                self.change=True  
                time.sleep(0.2)

        if page == 0 :
            my_img = get_image('4.jpeg')
            my_img = pygame.transform.scale(my_img,(1000,1000))
            screen.blit(my_img,my_img.get_rect())
            
            start_btn.draw_btn()
            quit_btn.draw_btn()
            settings_btn.draw_btn()
            if start_btn.update():
                page=1
            if quit_btn.update():
                pygame.quit()
            if settings_btn.update():
                page=-1
                
        if page==-1:
            pass
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

        self.player.coins=0
    def on_execute(self):
        global y_scroll
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
    
theApp = App()
theApp.on_execute()

