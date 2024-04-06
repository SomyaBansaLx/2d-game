import pygame
from pygame.locals import *
import pickle
from os import path
import os
import time
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
world=None
clock = pygame.time.Clock()
level=1
screen_width=cols*tile_size
screen_height=rows*tile_size
screen=pygame.display.set_mode((1000,1000))
intermediate=pygame.surface.Surface((screen_width,screen_height))
max_down=screen_height-1000
y_scroll=max_down
game_over=0
level_bg=pygame.transform.scale(get_image('level_bg.jpg'),(screen_width,screen_width))
end_bg=pygame.transform.scale(get_image('end.png'),(tile_size,tile_size))
# end_bg.set_colorkey(BLACK)


class World():
    def __init__(self, data):
        global dirt_tile,grass_tile
        self.tile_list = []
        dirt_img = pygame.transform.scale(
            get_image('brick1.png'), (tile_size, tile_size))
        grass_img = pygame.transform.scale(
            get_image('grass.png'), (tile_size, tile_size))
        row_pos = 0
        for row in data:
            col_pos = 0
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
                    laser_group.add(laser(col_pos * tile_size, row_pos * tile_size,1,2,1))
                elif ele == 7:
                    ninja_group.add(Ninja(col_pos * tile_size, row_pos * tile_size))
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

start_btn = Btn(350,450,300,100,'start.jpg')        

class character():
    def __init__(self, x, y):
        self.images_r = []
        self.images_l = []
        self.index = 0
        self.counter = 0
        self.jumped = False
        for i in range(1, 5):
            img = pygame.transform.scale(get_image(f'guy{i}.png'), (40, 80))
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
    def jump(self,event):
        if event.key==pygame.K_SPACE:
            if not self.in_air:
                self.vel_y = -15
                self.in_air = True
            elif not self.jumped:
                self.vel_y =-15
                self.jumped=True
                
    def draw_char(self, surface,world):
        global game_over,page
        walk_limit = 8
        key = pygame.key.get_pressed()
        dx = 0
        dy = 0
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
            
        dy = self.vel_y
        self.vel_y = min(10, self.vel_y+1)
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air=False
                    self.jumped=False
        if pygame.sprite.spritecollide(self, bullet_group, True):
            game_over=1
            page=1
            print(game_over)
        self.rect.x += dx
        self.rect.y += dy
        global y_scroll
        if (self.rect.y<max_down+400):
            y_scroll=max(0,self.rect.y-400)
        else:
            y_scroll=min(max_down,self.rect.y-400)
        surface.blit(self.image, self.rect)

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

class Ninja(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = pygame.image.load('ninja/NEWrun/1.png').convert()
        self.image_1 = pygame.transform.scale(self.image_1,(100,150))
        self.image_1.set_colorkey(BLACK)
        self.image_2 = pygame.image.load('ninja/NEWrun/5.png').convert()
        self.image_2 = pygame.transform.scale(self.image_2,(100,150))
        self.image_2.set_colorkey(BLACK)
        self.rect=self.image_1.get_rect()
        self.rect.x = x
        self.rect.y = y-75
        self.move_direction = 1
        self.move_counter = 0
        self.index = 0
        self.images_r = [self.image_1,self.image_2]
        img_flip_1 = pygame.transform.flip(self.image_1, True, False)
        img_flip_2 = pygame.transform.flip(self.image_2, True, False)
        self.images_l = [img_flip_1,img_flip_2]
        self.image = 0

        

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) >20 :
            self.index = 1 - self.index
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
            self.index = 0 
        if self.move_direction == 1 : 
            self.image = self.images_r[self.index]
        else :
            self.image = self.images_l[self.index]
        intermediate.blit(self.image,self.rect)
        

    # def update_2(self,x,y):
    #     if self.y==y :
    #         if self.x<=x:



  
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
            bullet_group.add(bullet(self.rect.x+int(self.move_direction*(tile_size//4)),self.rect.y,self.move_direction,'lava.png',self.move_speed,tile_size//2,tile_size//2))
            
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
    def update(self):
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
        pygame.draw.rect(intermediate,RED,pygame.Rect(self.rect.x+tile_size,self.rect.y,self.least-self.rect.x-tile_size,tile_size//2))
        intermediate.blit(end_bg,(self.least-tile_size,self.rect.y))
                
        self.move_counter+=1
        if self.move_counter==self.move_speed:
            self.rect.y-=self.move_direction*3
            self.move_counter=0
                
class App():
    def __init__(self):
        global grass_tile,dirt_tile
        self.running = True
        self.size = (screen_width,screen_width)
        # self.display_surf = pygame.display.set_mode(self.size)
        self.player = character(50, screen_height-200)
        self.change=False
        

    def on_init(self):
        self.running = True
        self.bg_img = pygame.transform.scale(get_image('bg.jpg'),(screen_width,screen_height))
        self.bg_img.set_alpha(150)

    def draw_grid(self):
        for i in range(cols):
            pygame.draw.line(intermediate, WHITE, (
                0+i*tile_size, 0), (0+i*tile_size,screen_height))
        for i in range(rows):
            pygame.draw.line(intermediate, WHITE, (
                0, 0+i*tile_size), (screen_width, 0+i*tile_size))

    def on_render(self):
        global page,game_over
        if page == 2 :
            if game_over==-1 :
                screen.fill(BLACK)
                intermediate.blit(self.bg_img, (0, 0))
                world.draw_world(intermediate)
                self.player.draw_char(intermediate,world)
                self.draw_grid()
                blob_group.update()
                blob_group.draw(intermediate)
                shooter_group.update()
                shooter_group.draw(intermediate)
                bullet_group.update()
                bullet_group.draw(intermediate)
                laser_group.update()
                laser_group.draw(intermediate)
                ninja_group.update()
                ninja_group.draw(intermediate)
                screen.blit(intermediate,(0,-y_scroll))
            elif game_over==1:
                screen.fill(BLACK)
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
                        game_over=-1
                        page=2 
                        load(level)  
            else:
                self.change=True  
                time.sleep(0.2)

        if page == 0 :
            my_img = get_image('first_page.jpg')
            my_img = pygame.transform.scale(my_img,(1000,1000))
            screen.blit(my_img,my_img.get_rect())
            
            start_btn.draw_btn()
            if start_btn.update():
                page=1
        pygame.display.flip()
        clock.tick(30)

    def on_execute(self):
        global y_scroll
        if self.on_init() == False:
            self.running = False

        while self.running:
            ev=None
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
    
