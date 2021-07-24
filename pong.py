#!/bin/python3
import pygame
import sys
import random
import math
# from icecream import ic

# setup
pygame.init()
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()
# screen setup
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
# global vars
ball_diameter = 20
speed = 10 
# acceptable angles for ball_direction
# note that rects can only move by whole ints - you can't draw half a pixel...
# therefore, ball.x/y is an int. Subsequently, trig positions are rounded to nearest.
# lower velocity (i.e. 'speed') makes the rounding more noticeable.
# minimum vel/spd of 10 and only using distinct angles is a simple mitigation.
anglelist = list(range(10, 360, 10))
blacklist = [80, 90, 100, 180, 260, 270, 280]
whitelist = [element for element in anglelist if element not in blacklist]
ball_direction = math.radians(random.choice(whitelist))
# collision stuff
first_collide = True
paddle_width = 10
paddle_height = 120
player_speed = 0 # default w/o keypress
score = [0,0]
player_return = True
game_font = pygame.font.SysFont("hack.ttf", 120)
# dracula colours
background_colour = (40,42,54)
font_colour = (98,114,164)
ball_colour = (241,250,140)
player_colour = (255,121,198)
opponent_colour = (139,233,253)
edge_colour =  (248, 248, 242)
# game rects
ball = pygame.Rect(screen_width*0.5 - ball_diameter*0.5, screen_height*0.5 - ball_diameter*0.5, ball_diameter, ball_diameter)
player = pygame.Rect(screen_width - paddle_width*2, screen_height*0.5 - paddle_height*0.5, paddle_width, paddle_height)
opponent = pygame.Rect(paddle_width, screen_height*0.5 - paddle_height*0.5, paddle_width, paddle_height)

def reset_ball():
	global ball_direction, player_return
	ball_direction = (math.radians(random.choice(whitelist)))
	ball.x = screen_width*0.5 - ball_diameter*0.5
	ball.y = screen_height*0.5 - ball_diameter*0.5
	if math.pi*0.5 < ball_direction < math.pi*1.5:
		player_return = True
	else:
		player_return = False
	# ic(round(math.degrees(ball_direction)))

def paddle_deflect():
	global ball_direction, first_collide
	# prevent angles above or below 360deg for easy checking
	if ball_direction > math.pi:
		ball_direction = (math.pi*3 - ball_direction)
	else: 
		ball_direction = math.pi - ball_direction
	first_collide = False

def animate_ball():
	global ball_direction, speed, first_collide, score, player_return
	# move ball - round required, else decimal places ignored
	ball.x += round(speed*math.cos(ball_direction))
	ball.y += round(speed*math.sin(ball_direction))  
	# screen bounce
	if ball.top <= 0 or ball.bottom >= screen_height:
		# mirror angle/direction
		ball_direction = math.pi*2 - ball_direction
	if ball.right <= 0: 
		score[1] += 1
		reset_ball()
	if ball.left >= screen_width: 
		score[0] += 1
		reset_ball()
	# check to see if we're already colliding to avoid weird behaviour
	if ball.left > opponent.right and ball.right < player.left:
		first_collide = True
	# paddle collision 
	if ball.colliderect(opponent) and first_collide:
		paddle_deflect()
		player_return = False
	if ball.colliderect(player) and first_collide:
		paddle_deflect()
		player_return = True

def animate_player():
	player.y += player_speed
	# keep paddles on screen
	if player.top <= 0: player.top = 0
	if player.bottom >= screen_height: player.bottom = screen_height

def animate_opponent():
	if player_return:
		# move toward ball
		if opponent.top < ball.y:
			opponent.top += 10
		if opponent.bottom > ball.y:
			opponent.bottom -= 10
		# stay on screen
		if opponent.top <= 0: opponent.top = 0
		if opponent.bottom >= screen_height: opponent.bottom = screen_height   
	else:
		# wait at center
		if opponent.centery > screen_height*0.5: 
			opponent.centery -= 5
		elif opponent.centery < screen_height*0.5:
			opponent.centery += 5

# game loop
while True:
	# handle user input
	# get list of held keys
	held = pygame.key.get_pressed()
	# control combos:
	if held[pygame.K_LCTRL] and held[pygame.K_q] or held[pygame.K_LCTRL] and held[pygame.K_c]:
		pygame.quit()
		sys.exit()
	# respond to input
	for event in pygame.event.get():
		# move on KEYDOWN
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				player_speed += 10
			elif event.key == pygame.K_UP:
				player_speed -= 10
			# add a ball reset:
			elif event.key == pygame.K_r:
				reset_ball()
		# or keyup - i.e. if prior key wasn't released
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				player_speed -= 10
			elif event.key == pygame.K_UP:
				player_speed += 10    
		elif event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		# stop moving with no input
		else: player_speed = 0
	
	# draw & colour visuals
	screen.fill(background_colour)

	# add a border to better define the screen edge
	border_rect = pygame.Rect(0, 0, screen_width, screen_height)
	pygame.draw.rect(screen, edge_colour, border_rect, 1)
	# and a divide
	pygame.draw.line(screen, edge_colour, (screen_width*0.5,0), (screen_width*0.5,screen_height))
	# draw scores
	player_score = game_font.render(str(score[1]), True, font_colour)
	screen.blit(player_score, (928, 320))
	opponent_score = game_font.render(str(score[0]), True, font_colour)
	screen.blit(opponent_score, (288, 320))
	# draw game rects
	pygame.draw.rect(screen, player_colour, player)
	pygame.draw.rect(screen, opponent_colour, opponent)
	pygame.draw.ellipse(screen, ball_colour, ball)   

	animate_ball()
	animate_player()
	animate_opponent()

	# update screen
	pygame.display.update()
	clock.tick(100)
