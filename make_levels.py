import pygame
from pygame.locals import *
import pickle
from os import path
import random

pygame.init()
levels=[{'rows':40,'cols':40},{'rows':60,'cols':20},{'rows':60,'cols':20},{'rows':20,'cols':60}]
level = 3
main_page  = 0 
clock = pygame.time.Clock()
fps = 60
y_scroll=0
x_scroll=0
#game window
tile_size = 50
cols = levels[level-1]['cols']
rows= levels[level-1]['rows']
margin = 200
screen_width = tile_size * cols
screen_height = (tile_size * rows) + margin

screen = pygame.display.set_mode((1000, 1000))
intermediate=pygame.surface.Surface((screen_width,screen_height))
pygame.display.set_caption('Level Editor')



#load images
bg_img = pygame.image.load('bg.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
dirt_img = pygame.image.load('brick1.png')
grass_img = pygame.image.load('brown_wood.png')
blob_img = pygame.image.load('blob.png')
lava_img = pygame.image.load('lava.png')
save_img = pygame.image.load('save_btn.png')
load_img = pygame.image.load('load_btn.png')
bacteria_img =  pygame.image.load('bacteria.jpeg')
shooter_img = pygame.image.load('shooter.png')
mask_img = pygame.image.load('mask.jpeg')
sanitizer_img = pygame.image.load('sanitizer.png')
people_images=['man_1.jpeg','man_2.jpeg','man_3.jpeg']
people_img = pygame.image.load(random.choice(people_images))
shooter_left= pygame.transform.flip(shooter_img, True, False)
ninja=pygame.transform.scale(pygame.image.load('lava.png'),(tile_size,tile_size))
zap_img = pygame.transform.scale(pygame.image.load('zapper.jpg'),(tile_size,tile_size))
gayab_img= pygame.transform.scale(pygame.image.load('white_tile.png'),(tile_size,tile_size))
coin_img= pygame.transform.scale(pygame.image.load('coin.png'),(tile_size,tile_size))
volts_img= pygame.transform.scale(pygame.image.load('volts.jpg'),(tile_size,tile_size))
spike_img= pygame.transform.scale(pygame.image.load('spike.jpg'),(tile_size,tile_size))
sanitizer_gun_img=pygame.transform.scale(pygame.image.load('sanitizer_gun.jpeg'),(tile_size,tile_size))
mask_img=pygame.transform.scale(pygame.image.load('mask.jpeg'),(tile_size,tile_size))
hosp_img=pygame.transform.scale(pygame.image.load('hospital.jpeg'),(2*tile_size,2*tile_size))
sanitizer_img=pygame.transform.scale(pygame.image.load('sanitizer.png'),(tile_size,tile_size))
water_img=pygame.transform.scale(pygame.image.load('water.png'),(2*tile_size,2*tile_size))
gate_img=pygame.transform.scale(pygame.image.load('gate.png'),(tile_size,int(1.5*tile_size)))

clicked = False
click=False
people_images=['man_1.jpeg','man_2.jpeg','man_3.jpeg']

white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []
def load_w():
    global world_data,screen_width,screen_height,bg_img,intermediate
    screen_width = tile_size *levels[level-1]['cols']
    screen_height = (tile_size * levels[level-1]['rows']) + margin
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
    world_data = []
    for row in range(levels[level-1]['rows']):
        r = [0] * levels[level-1]['cols']
        world_data.append(r)

    for tile in range(0, levels[level-1]['cols']):
        world_data[levels[level-1]['rows']-1][tile] = 2
        world_data[0][tile] = 1
    for tile in range(0,levels[level-1]['rows']):
        world_data[tile][0] = 1
        world_data[tile][levels[level-1]['cols']-1] = 1

load_w()
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    intermediate.blit(img, (x, y))

def draw_grid():
    for c in range(levels[level-1]['cols']+1):
        #vertical lines
        pygame.draw.line(intermediate, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
    for c in range(levels[level-1]['rows']+1):
        #horizontal lines
        pygame.draw.line(intermediate, white, (0, c * tile_size), (screen_width, c * tile_size))

def draw_world():
    for row in range(levels[level-1]['rows']):
        for col in range(levels[level-1]['cols']):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    #dirt blocks
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 2:
                    #grass blocks
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 3:
                    #enemy blocks
                    img = pygame.transform.scale(blob_img, (tile_size, int(tile_size * 0.75)))
                    intermediate.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                elif world_data[row][col] == 4:
                    #horizontally moving platform
                    img = pygame.transform.scale(shooter_img, (tile_size, tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 5:
                    #vertically moving platform
                    img = pygame.transform.scale(shooter_left, (tile_size, tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 6:
                    #lava
                    img = pygame.transform.scale(shooter_img, (tile_size, tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
                elif world_data[row][col] == 7:
                    img = pygame.transform.scale(ninja, (tile_size, tile_size))
                    intermediate.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
                elif world_data[row][col] == 8:
                    #exit
                    img = pygame.transform.scale(gayab_img, (tile_size, (tile_size)))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 9:
                    #exit
                    img = pygame.transform.scale(zap_img, (tile_size, (tile_size)))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 10:
                    img = pygame.transform.scale(coin_img, (tile_size, (tile_size)))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 11:
                    img = pygame.transform.scale(volts_img, (tile_size, (tile_size)))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 12:
                    img = pygame.transform.scale(spike_img, (tile_size, (tile_size)))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif  world_data[row][col] == 13:
                    img = pygame.transform.scale(people_img,(50,100))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif  world_data[row][col] == 14:
                    img = pygame.transform.scale(gayab_img,(tile_size,tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif  world_data[row][col] == 15:
                    img = pygame.transform.scale(sanitizer_gun_img,(tile_size,tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif  world_data[row][col] == 16:
                    img = pygame.transform.scale(mask_img,(tile_size,tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif  world_data[row][col] == 17:
                    intermediate.blit(sanitizer_img, (col * tile_size, row * tile_size))
                elif  world_data[row][col] == 18:
                    intermediate.blit(hosp_img, (col * tile_size, row * tile_size))
                elif  world_data[row][col] == 19:
                    img = pygame.transform.scale(bacteria_img,(tile_size,tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                elif  world_data[row][col] == 20:
                    intermediate.blit(water_img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 21:
                    intermediate.blit(gate_img, (col * tile_size, row * tile_size+tile_size//2) )
                    
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        pos_new=(pos[0]+x_scroll,pos[1]+y_scroll)
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos_new):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #draw button
        intermediate.blit(self.image, (self.rect.x, self.rect.y))

        return action

#create load and save buttons
save_button = Button(300, screen_height - 80, save_img)
load_button = Button(500, screen_height - 80, load_img)

#main game loop
run = True
while run:
    max_num=21
    clock.tick(fps)
    #draw background
    screen.fill(green)
    intermediate=pygame.surface.Surface((screen_width,screen_height))
    intermediate.fill((0,0,0))
    intermediate.blit(bg_img, (0, 0))

    draw_grid()
    draw_world()

    if save_button.draw():
        #save level data
        pickle_out = open(f'level{level}_data', 'wb')
        pickle.dump(world_data, pickle_out)
        pickle_out.close()
    if load_button.draw():
        if path.exists(f'level{level}_data'):
            pickle_in = open(f'level{level}_data', 'rb')
            world_data = pickle.load(pickle_in)
            
    draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
    draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #mouseclicks to change tiles
        if event.type == pygame.KEYDOWN and event.key==pygame.K_1 and click==False:
            click=True
            pos = pygame.mouse.get_pos()
            x = (pos[0]+x_scroll) // tile_size
            y = (pos[1]+y_scroll) // tile_size
            #check that the coordinates are within the tile area
            if x <levels[level-1]['cols'] and y <levels[level-1]['rows']:
                world_data[y][x]=min(world_data[y][x]+10,max_num) 
        else:
            click=False
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = (pos[0]+x_scroll) // tile_size
            y = (pos[1]+y_scroll) // tile_size
            #check that the coordinates are within the tile area
            if x <levels[level-1]['cols'] and y <levels[level-1]['rows']:
                #update tile value
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[y][x] += 1
                    if world_data[y][x] > max_num:
                        world_data[y][x] = 0
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = max_num
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
            pos = pygame.mouse.get_pos()
            x = (pos[0]+x_scroll) // tile_size
            y = (pos[1]+y_scroll) // tile_size
            if x <levels[level-1]['cols']  and y < levels[level-1]['rows']:
                world_data[y][x] =0
        
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level =min(level+1,len(levels))
                load_w()
                save_button.rect.topleft=(300,screen_height-80)
                load_button.rect.topleft=(500,screen_height-80)
            elif event.key == pygame.K_DOWN and level > 1:
                level -= 1
                load_w()
                save_button.rect.topleft=(300,screen_height-80)
                load_button.rect.topleft=(500,screen_height-80)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                y_scroll=max(0,y_scroll-30)
            elif event.button == 5:
                y_scroll+=30
        if pygame.key.get_pressed()[K_RIGHT]:
            x_scroll+=50
        if pygame.key.get_pressed()[K_LEFT]:
            x_scroll=max(0,x_scroll-50)
        x_scroll=min(levels[level-1]['cols']*tile_size-1000,x_scroll)
        y_scroll=min(y_scroll,levels[level-1]['rows']*tile_size-800)
    screen.blit(intermediate,(-x_scroll,-y_scroll))
    #update game display window
    pygame.display.flip()

pygame.quit()