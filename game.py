import pygame
from pygame.locals import *
import pickle
from os import path
import os

pygame.init()
dirt_tile=None
grass_tile=None
tile_size = 50
rows=40
cols=20
blob_group = pygame.sprite.Group()
clock = pygame.time.Clock()
_image_library = {}
level=3
screen_width=cols*tile_size
screen_height=rows*tile_size
screen=pygame.display.set_mode((1000,1000))
intermediate=pygame.display.set_mode((screen_width,screen_height))
max_down=screen_height-1050
y_scroll=max_down

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

def get_image(path, color=BLACK):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert()
        _image_library[path] = image
    return image


class World():
    def __init__(self, data):
        global dirt_tile,grass_tile
        self.tile_list = []
        dirt_img = pygame.transform.scale(
            get_image('dirt.png'), (tile_size, tile_size))
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
                col_pos += 1
            row_pos += 1

    def draw_world(self, surface):
        for tile in self.tile_list:
            surface.blit(tile[0], tile[1])
            # pygame.draw.rect(surface,tile[1])


class character():
    def __init__(self, x, y):
        self.images_r = []
        self.images_l = []
        self.index = 0
        self.counter = 0
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

    def draw_char(self, surface,world):
        walk_limit = 8
        key = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if key[pygame.K_SPACE] and not self.in_air:
            self.vel_y = -15
            self.in_air = True
        elif not key[pygame.K_SPACE]:
            self.in_air = False

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

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
            
class Gate(pygame.sprite.Sprite):
    def __init__(self,x,y,link):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('gate.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.link=link
        
class App():
    def __init__(self):
        global grass_tile,dirt_tile
        self.running = True
        self.size = (screen_width,screen_width)
        # self.display_surf = pygame.display.set_mode(self.size)
        self.player = character(50, screen_height-200)

    def on_init(self):
        self.running = True
        self.world = world
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
        screen.fill(BLACK)
        intermediate.blit(self.bg_img, (0, 0))
        self.world.draw_world(intermediate)
        self.player.draw_char(intermediate,self.world)
        self.draw_grid()
        blob_group.update()
        blob_group.draw(intermediate)
        screen.blit(intermediate,(0,-y_scroll))
        pygame.display.flip()
        clock.tick(30)

    def on_execute(self):
        global y_scroll
        if self.on_init() == False:
            self.running = False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:
                        y_scroll=max(0,y_scroll-30)
                        
                    elif event.button == 5:
                        y_scroll=min(max_down,30+y_scroll)
            self.on_render()

        pygame.quit()

theApp = App()
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world = World(world_data)
theApp.on_execute()
    
