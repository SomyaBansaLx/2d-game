import pygame
from pygame.locals import *
import pickle
from os import path


pygame.init()

main_page  = 0 
clock = pygame.time.Clock()
fps = 60
y_scroll=0
#game window
tile_size = 50
cols = 20
rows=40
margin = 200
screen_width = tile_size * cols
screen_height = (tile_size * rows) + margin

screen = pygame.display.set_mode((1000, 1000))
intermediate=pygame.display.set_mode((1000,2200))
pygame.display.set_caption('Level Editor')


#load images
bg_img = pygame.image.load('bg.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
dirt_img = pygame.image.load('dirt.png')
grass_img = pygame.image.load('grass.png')
blob_img = pygame.image.load('blob.png')
lava_img = pygame.image.load('lava.png')
exit_img = pygame.image.load('exit.png')
save_img = pygame.image.load('save_btn.png')
load_img = pygame.image.load('load_btn.png')
shooter_img = pygame.image.load('shooter.png')
shooter_left= pygame.transform.flip(shooter_img, True, False)

#define game variables
clicked = False
level = 1

#define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []
for row in range(rows):
    r = [0] * cols
    world_data.append(r)

#create boundary
for tile in range(0, cols):
    world_data[rows-1][tile] = 2
    world_data[0][tile] = 1
for tile in range(0,rows):
    world_data[tile][0] = 1
    world_data[tile][cols-1] = 1

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    intermediate.blit(img, (x, y))

def draw_grid():
    for c in range(cols+1):
        #vertical lines
        pygame.draw.line(intermediate, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
    for c in range(rows+1):
        #horizontal lines
        pygame.draw.line(intermediate, white, (0, c * tile_size), (screen_width, c * tile_size))


def draw_world():
    for row in range(rows):
        for col in range(cols):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    #dirt blocks
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 2:
                    #grass blocks
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 3:
                    #enemy blocks
                    img = pygame.transform.scale(blob_img, (tile_size, int(tile_size * 0.75)))
                    intermediate.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                if world_data[row][col] == 4:
                    #horizontally moving platform
                    img = pygame.transform.scale(shooter_img, (tile_size, tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 5:
                    #vertically moving platform
                    img = pygame.transform.scale(shooter_left, (tile_size, tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 6:
                    #lava
                    img = pygame.transform.scale(shooter_img, (tile_size, tile_size))
                    intermediate.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
                # if world_data[row][col] == 7:
                    #coin
                    # img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
                    # intermediate.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
                if world_data[row][col] == 8:
                    #exit
                    img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
                    intermediate.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))



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
        pos_new=(pos[0],pos[1]+y_scroll)
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
save_button = Button(screen_width // 2 - 150, screen_height - 80, save_img)
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_img)

#main game loop
run = True
while run:
    
    clock.tick(fps)
    
    #draw background
    screen.fill(green)
    intermediate.blit(bg_img, (0, 0))

    #load and save level
    if save_button.draw():
        #save level data
        pickle_out = open(f'level{level}_data', 'wb')
        pickle.dump(world_data, pickle_out)
        pickle_out.close()
    if load_button.draw():
        #load in level data
        if path.exists(f'level{level}_data'):
            pickle_in = open(f'level{level}_data', 'rb')
            world_data = pickle.load(pickle_in)


    #show the grid and draw the level tiles
    draw_grid()
    draw_world()


    #text showing current level
    draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
    draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #mouseclicks to change tiles
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_size
            y = (pos[1]+y_scroll) // tile_size
            #check that the coordinates are within the tile area
            if x < cols and y < rows:
                #update tile value
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[y][x] += 1
                    if world_data[y][x] > 8:
                        world_data[y][x] = 0
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = 8
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        #up and down key presses to change level number
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            elif event.key == pygame.K_DOWN and level > 1:
                level -= 1
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                y_scroll=max(0,y_scroll-30)
                
            elif event.button == 5:
                y_scroll=min(1150,30+y_scroll)
    screen.blit(intermediate,(0,-y_scroll))
    #update game display window
    pygame.display.flip()

pygame.quit()