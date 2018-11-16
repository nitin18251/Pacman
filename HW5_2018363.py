import pygame
from pygame.locals import *
from numpy import loadtxt
import time
from random import randint

#Constants for the game
WIDTH, HEIGHT = (60, 60)
WALL_COLOR = pygame.Color(96,92,36,255) 
COIN_COLOR = pygame.Color(255, 255, 0, 255) 
black=pygame.Color(0,0,0,255)
white=pygame.Color(255,255,255,255)
green=pygame.Color(0,255,0,255)
darkgreen=pygame.Color(0,150,0,255)
red=pygame.Color(255,0,0,255)
darkred=pygame.Color(150,0,0,255)
DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)
pacman_img=pygame.image.load("pacman.png")
pacman_img=pygame.transform.scale(pacman_img,(int(WIDTH/2),int(HEIGHT/2)))

#Utility functions
def add_to_pos(pos, pos2):
	pos_pixels=pixels_from_points(pos)#for getting the  actual coordinates from the screen
	pos2_pixels=pixels_from_points(pos2)

	if screen.get_at((pos_pixels[0]+pos2_pixels[0],pos_pixels[1]+pos2_pixels[1]))==WALL_COLOR:#for getting the pixel color at that location
		if screen.get_at((pos_pixels[0]-pos2_pixels[0],pos_pixels[1]-pos2_pixels[1]))==WALL_COLOR:#if its between two walls and the user tries to move into wall then it wil stop right at that position 
			return pos,pos2
		return (pos[0]-pos2[0],pos[1]-pos2[1]),(-pos2[0],-pos2[1])
	else:
		return (pos[0]+pos2[0],pos[1]+pos2[1]),pos2#for changing positon of pacman

def pixels_from_points(pos):
	return (pos[0]*int(WIDTH/2), pos[1]*int(HEIGHT/2))

def pixels_from_points_c(pos):#pixel getting requires different approach for circles i.e coins
	return (pos[0]*int(WIDTH/2)+int(WIDTH/4),pos[1]*int(WIDTH/2)+int(WIDTH/4))

def draw_wall(screen, pos):
	pixels = pixels_from_points(pos)
	pygame.draw.rect(screen, WALL_COLOR, [pixels[0],pixels[1], WIDTH/2, HEIGHT/2])

def draw_coin(screen, pos):
	pixels = pixels_from_points_c(pos)
	pygame.draw.circle(screen, COIN_COLOR, pixels,int(WIDTH/4))

def draw_pacman(screen, pos): 
	pixels = pixels_from_points(pos)
	screen.blit(pacman_img,pixels)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def score(count,user="Sandeep"):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: "+str(count), True, (0,0,0))
    user=font.render("User:"+user, True, (0,0,0))
    time=font.render("Time spent"+str(pygame.time.get_ticks()),True,(0,0,0))
    screen.blit(time,(0,500))
    screen.blit(user,(0, 0))
    screen.blit(text,(0,15))

def gameloop():
	#Default values
	pacman_position = (1,1)
	dir_change=RIGHT
	count=0

	while True:
		print(1)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			print(event)
		screen.blit(background, (0,0))

		for col in range(cols):
			for row in range(rows):
				value = layout[row][col]
				pos = (col, row)
				if value == 'w':
					draw_wall(screen, pos)
				elif value=='.' and pos in coin_pos:
					draw_coin(screen, pos)
	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				dir_change =LEFT 
			elif event.key == pygame.K_RIGHT:
				dir_change = RIGHT
			elif event.key == pygame.K_DOWN:
				dir_change = DOWN
			elif event.key == pygame.K_UP:
				dir_change = TOP
		
		#Update player position based on movement.
		pacman_position,dir_change = add_to_pos(pacman_position, dir_change)
		draw_pacman(screen, pacman_position)
		if pacman_position in coin_pos:
			coin_pos.remove(pacman_position)
			count+=1
		score(count)

		#Update the display
		pygame.display.update()
		clock.tick(30)
		#Wait for a while, computers are very fast.
		time.sleep(0.3)
		'''if len(coin_pos)==0:
			screen.fill(white)
	        font_style = pygame.font.Font('freesansbold.ttf',50)
	        TextSurf, TextRect = text_objects("Pacman-2018363",font_style)
	        TextRect.center = ((WIDTH*5),(HEIGHT*5))
	        screen.blit(TextSurf, TextRect)'''



def pacman_intro():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill(white)
        font_style = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Pacman-2018363",font_style)
        TextRect.center = ((WIDTH*5),(HEIGHT*5))
        screen.blit(TextSurf, TextRect)
        mouse=pygame.mouse.get_pos()
        if 200 > mouse[0] > 100 and 500 > mouse[1] > 450:
            pygame.draw.rect(screen, darkgreen,(100,450,130,50))
            gameloop()
            break
        else:
            pygame.draw.rect(screen, green,(100,450,130,50))

        if 500 > mouse[0] > 400 and 500 > mouse[1] > 450:
            pygame.draw.rect(screen, darkred,(400,450,130,50))
            pygame.quit()
            quit()
            break
        else:
            pygame.draw.rect(screen, red,(400,450,130,50))

        option1 = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Start",font_style)
        TextRect.center = ((150),(475))
        screen.blit(TextSurf, TextRect)

        option2 = pygame.font.Font('freesansbold.ttf',20)
        TextSurf, TextRect = text_objects("Exit",font_style)
        TextRect.center = ((450),(475))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)

#Initializing pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH*10,HEIGHT*10))
pygame.display.set_caption('Pacman Pro ;} 2018363')
background = pygame.Surface((WIDTH*10,HEIGHT*10)).convert()

clock= pygame.time.Clock()

layout = loadtxt('layout.txt', dtype=str)
rows, cols = layout.shape
background.fill((0,0,255))

coin_pos=[]# randomly genrated coin positions
for i in range(20):
	coin_pos.append((randint(1,18),randint(1,18)))
pacman_intro()
