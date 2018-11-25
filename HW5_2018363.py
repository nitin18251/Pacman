import pygame,time,pygame_textinput
from pygame.locals import *
from numpy import loadtxt
from random import randint

#Constants for the game
WIDTH, HEIGHT = (60, 60)
WALL_COLOR = pygame.Color(96,92,36,255) 
COIN_COLOR = pygame.Color(255, 255, 0, 255) 
black =      pygame.Color(0,0,0,255)
white =      pygame.Color(255,255,255,255)
green =      pygame.Color(0,255,0,255)
darkgreen=   pygame.Color(0,150,0,255)
red   =      pygame.Color(255,0,0,255)
darkred=     pygame.Color(150,0,0,255)
DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)
directions=[DOWN,RIGHT,TOP,LEFT]#required for generating random directions
pacman_img=pygame.image.load("pacman.png")#loading the image of our pacman
pacman_img=pygame.transform.scale(pacman_img,(int(WIDTH/2),int(HEIGHT/2)))#scaling it to get fit for our game

#Utility functions
def add_to_pos(pos, pos2):
	pos_pixels =pixels_from_points(pos)#for getting the  actual coordinates from the screen
	pos2_pixels=pixels_from_points(pos2)

	if screen.get_at((pos_pixels[0]+pos2_pixels[0],pos_pixels[1]+pos2_pixels[1]))==WALL_COLOR:#for getting the pixel color at that location
		if screen.get_at((pos_pixels[0]-pos2_pixels[0],pos_pixels[1]-pos2_pixels[1]))==WALL_COLOR:#if its between two walls and the user tries to move into wall then it wil stop right at that position 
			return pos,pos2
		return (pos[0]-pos2[0],pos[1]-pos2[1]),(-pos2[0],-pos2[1])#for bouncing from walls
	else:
		return (pos[0]+pos2[0],pos[1]+pos2[1]),pos2#for changing positon of pacman

def pixels_from_points(pos,temp=0):
	if temp:#pixel getting requires different approach for circles i.e coins
		return (pos[0]*int(WIDTH/2)+int(WIDTH/4),pos[1]*int(WIDTH/2)+int(WIDTH/4))
	return (pos[0]*int(WIDTH/2), pos[1]*int(HEIGHT/2))

def draw_wall(screen, pos):#for drawing walls 
	pixels = pixels_from_points(pos)
	pygame.draw.rect(screen, WALL_COLOR, [pixels[0],pixels[1], WIDTH/2, HEIGHT/2])

def draw_coin(screen, pos):#for making coins
	pixels = pixels_from_points(pos,1)
	pygame.draw.circle(screen, COIN_COLOR, pixels,int(WIDTH/4))

def draw_black_hole(screen,pos):#for making black holes
	pixels = pixels_from_points(pos,1)
	pygame.draw.circle(screen, black, pixels,int(WIDTH/4))

def draw_pacman(screen, pos): #for making pacman
	pixels = pixels_from_points(pos)
	screen.blit(pacman_img,pixels)

def message_display(text,position=((WIDTH*5),(HEIGHT*5)),size=40,color=red):#for displaying various messages
    text_font = pygame.font.Font('freesansbold.ttf',size)
    TextSurface = text_font.render(text, True, color)
    TextRect=TextSurface.get_rect()
    TextRect.center = position
    screen.blit(TextSurface, TextRect)
    pygame.display.update()
    
def score(count,Start_time,user="Sandeep"):#for displaying various details like score,time ,user
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: "+str(count), True, (0,0,0))
    user=font.render("User:"+user, True, (0,0,0))
    Time=font.render("Time spent "+str(round((time.time()-Start_time)/60,2))+" mins",True,(0,0,0))
    screen.blit(Time,(400,0))
    screen.blit(user,(0, 0))
    screen.blit(text,(0,15))

def write_to_file(score,user,Start_time):
	details=open('details.txt','a+')
	det=user+'		'+str(score)+'		'+str(Start_time)+'\n'
	details.write(det)
	details.close()

def game_over(count,Start_time,user):#game over dialog. It happens in two conditions either user passes black hole twice or all the coins gets erased
	message_display('GAME OVER!!',((WIDTH*5),(HEIGHT*5-20)))
	message_display('Final score~ '+str(count),((WIDTH*5),(HEIGHT*5+20)),color=green)
	message_display('Time spent~ '+str(round((time.time()-Start_time)/60,2))+' mins',position=((WIDTH*5),(HEIGHT*5+60)),color=green)
	write_to_file(count,user,Start_time)
	while 1:#for pausing the game until user exits or resets it
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_q):
				pygame.quit()	
				quit()
			elif event.type == pygame.KEYDOWN and event.key==pygame.K_r:
				pacman_intro()
				break

def username_input():#creating a window in pygame to take input from user
	pygame.display.set_caption('Enter Username: (press up arrow key to start game)')
	textinput = pygame_textinput.TextInput()
	while True:
		screen.fill(white)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key==pygame.K_UP:
					return textinput.get_text()
		textinput.update(events)
		screen.blit(textinput.get_surface(), (10, 10))
		pygame.display.update()
		clock.tick(30)

def gameloop(user):
	#Default values
	pygame.display.set_caption('Pacman Pro ;} 2018363')
	Start_time=time.time()
	pacman_position = (1,1)
	for i in range(10):
		x,y=(randint(1,18),randint(1,18))
		if layout[x][y]!='w':
			pacman_position = (x,y)#for generating random starting posiition of pacman
			break

	dir_change=directions[randint(0,3)]#for generating random initial movement of pacman
	count=0
	black_count=0
	coin_pos=[]# randomly genrated coin positions
	for i in range(20):
		coin_pos.append((randint(1,18),randint(1,18)))
	black_pos=[]# randomly genrated black hole positions
	for i in range(5):
		black_pos.append((randint(1,18),randint(1,18)))
	
	while True:
		screen.blit(background, (0,0))
		for col in range(cols):
			for row in range(rows):
				value = layout[row][col]
				pos = (col, row)
				if value == 'w':
					draw_wall(screen, pos)
					if pos in coin_pos:#removal of coin positons which coincides with wall
						coin_pos.remove(pos)
				elif pos in coin_pos:
					draw_coin(screen, pos)
				elif pos in black_pos:
					draw_black_hole(screen,pos)

		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_q):#quit game either by pressing 'q' or by closing the game
				pygame.quit()
				write_to_file(score,user,Start_time)
				exit()
			elif event.type == pygame.KEYDOWN:
				if event.key==pygame.K_r:#reset button
					write_to_file(score,user,Start_time)
					pacman_intro()
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
		if pacman_position in coin_pos:#removal of coins if pacman passes through it
			coin_pos.remove(pacman_position)
			count+=1
		elif pacman_position in black_pos:#reduction of score if passes through black hole
			count-=1
			black_count+=1
			if black_count>=2:#game over if passed through black hole more than 2 times 
				game_over(count,Start_time,user)

		score(count,Start_time,user)#updating of score and time
		pygame.display.update()
		time.sleep(0.1)
		if len(coin_pos)==0:#if all the coins are over then game over
			game_over(count,Start_time,user)

def pacman_intro():
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_q):#exits game if 'q' is pressed
				pygame.quit()
				quit()
			elif event.type==pygame.KEYDOWN and event.key==pygame.K_s:#start the game as soon as key 's' is pressed
				user=username_input()#taking the input from user
				gameloop(user)
                
		screen.fill(WALL_COLOR)
		message_display("Pacman-2018363",color=black)
		mouse_pos=pygame.mouse.get_pos()
		if int(WIDTH-10)*4 > mouse_pos[0] > int(WIDTH-10)*2 and int(WIDTH-10)*10 > mouse_pos[1] > int(15*WIDTH/2):#for drawing start button
			pygame.draw.rect(screen, darkgreen,(int(3*WIDTH/2),int(15*WIDTH/2),int(WIDTH*2+10),int(WIDTH-10)))#this is for changing the colour of button fro green to dark green to make it look like 
			click = pygame.mouse.get_pressed()
			if click[0]==1:#if clicked on button then start the game 
				user=username_input()#taking the input from user
				gameloop(user)
				break
		else:
			pygame.draw.rect(screen, green,(int(3*WIDTH/2),int(15*WIDTH/2),int(WIDTH*2+10),int(WIDTH-10)))#else let the button remain in green as it

		if int(WIDTH-10)*10 > mouse_pos[0] > int(WIDTH-20)*10 and int(WIDTH-10)*10> mouse_pos[1] > int(15*WIDTH/2):#same as above button but for exit 
			pygame.draw.rect(screen, darkred,(int(13*WIDTH/2),int(15*HEIGHT/2),int(WIDTH*2+10),int(HEIGHT-10)))
			click = pygame.mouse.get_pressed()
			if click[0]==1:
				pygame.quit()
				quit()
	            
		else:
			pygame.draw.rect(screen, red,(390,450,130,50))

		message_display("Start",((int(5*WIDTH/2)),(int(16*HEIGHT/2))),color=red)#displaying text on buttons
		message_display("Exit",((int(15*WIDTH/2)),(int(16*HEIGHT/2))),color=green)
		pygame.display.update()
		clock.tick(15)

#Initializing pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH*10,HEIGHT*10))
background = pygame.Surface((WIDTH*10,HEIGHT*10)).convert()
clock=pygame.time.Clock()
layout = loadtxt('layout.txt', dtype=str)#for loading the layout from layout.txt
rows, cols = layout.shape
background.fill((0,0,255))
pacman_intro()
