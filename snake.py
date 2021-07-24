#!/bin/python3
import pygame
import random
from pygame.math import Vector2
import sys

class Snake:
	def __init__(self):
		# starting position, with 3 blocks
		self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
		# starting direction - move to right
		self.direction = Vector2(1,0)
		self.grow = False

	def draw_snake(self):
		# radius originally used for the head, but later everything
		head_rad = int(cell_size*0.9)
		# determine head & tail relations, so that we can orient them
		head_relation = self.body[1] - self.body[0]
		# -1 being the last, -2 the penultimate...
		tail_relation = self.body[-2] - self.body[-1]
		# enumerate provides an index that lets us check more than the current block
		# this allows for vector comparisons between multiple blocks
		for index,block in enumerate(self.body):
			# alternate colours
			if index % 2: colour = body_colour 
			else: colour = head_colour
			# set position & size of each block
			x_pos = block.x*cell_size + cell_size*0.1
			y_pos = block.y*cell_size + cell_size*0.1
			block_rect = pygame.Rect(x_pos, y_pos, cell_size*0.8, cell_size*0.8)
			# the head is the 1st element, let's rotate it according to position
			# note that simply using 'self.direction' turns head too quickly.
			if index == 0:
				if head_relation == Vector2(0,1):
					pygame.draw.rect(canvas, head_colour, block_rect, border_top_left_radius=head_rad, border_top_right_radius=head_rad)
				elif head_relation == Vector2(0,-1):
					pygame.draw.rect(canvas, head_colour, block_rect, border_bottom_left_radius=head_rad, border_bottom_right_radius=head_rad)
				elif head_relation == Vector2(1,0):
					pygame.draw.rect(canvas, head_colour, block_rect, border_top_left_radius=head_rad, border_bottom_left_radius=head_rad)
				elif head_relation == Vector2(-1,0):
					pygame.draw.rect(canvas, head_colour, block_rect, border_top_right_radius=head_rad, border_bottom_right_radius=head_rad)
			# now for the tail
			elif index == len(self.body) - 1:
				if tail_relation == Vector2(0,1):
					pygame.draw.rect(canvas, colour, block_rect, border_top_left_radius=head_rad, border_top_right_radius=head_rad)
				elif tail_relation == Vector2(0,-1):
					pygame.draw.rect(canvas, colour, block_rect, border_bottom_left_radius=head_rad, border_bottom_right_radius=head_rad)
				elif tail_relation == Vector2(1,0):
					pygame.draw.rect(canvas, colour, block_rect, border_top_left_radius=head_rad, border_bottom_left_radius=head_rad)
				elif tail_relation == Vector2(-1,0):
					pygame.draw.rect(canvas, colour, block_rect, border_top_right_radius=head_rad, border_bottom_right_radius=head_rad)
			# body bends
			else:
				# set the relationship between the current block & those either side
				last_blk_rel = self.body[index + 1] - block
				next_blk_rel = self.body[index - 1] - block
				# if no change in direction - draw straight rect
				if last_blk_rel.x == next_blk_rel.x or last_blk_rel.y == next_blk_rel.y:
					pygame.draw.rect(canvas, colour, block_rect)
				# if turned from going right to up - radius on bottom right
				elif last_blk_rel.x == -1 and next_blk_rel.y == -1:
					pygame.draw.rect(canvas, colour, block_rect, border_bottom_right_radius=head_rad)
				# if turned from going right to down  - radius on top right
				elif last_blk_rel.x == -1 and next_blk_rel.y == 1:
					pygame.draw.rect(canvas, colour, block_rect, border_top_right_radius=head_rad)
				# if turned from going left to up - radius on bottom left
				elif last_blk_rel.x == 1 and next_blk_rel.y == -1:
					pygame.draw.rect(canvas, colour, block_rect, border_bottom_left_radius=head_rad)
				# if turned from going left to down  - radius on top left
				elif last_blk_rel.x == 1 and next_blk_rel.y == 1:
					pygame.draw.rect(canvas, colour, block_rect, border_top_left_radius=head_rad)
				# if turned from going up to right - radius on top left
				elif last_blk_rel.y == 1 and next_blk_rel.x == 1:
					pygame.draw.rect(canvas, colour, block_rect, border_top_left_radius=head_rad)
				# if turned from going up to left  - radius on top right
				elif last_blk_rel.y == 1 and next_blk_rel.x == -1:
					pygame.draw.rect(canvas, colour, block_rect, border_top_right_radius=head_rad)
				# if turned from going down to right - radius on bottom left
				elif last_blk_rel.y == -1 and next_blk_rel.x == 1:
					pygame.draw.rect(canvas, colour, block_rect, border_bottom_left_radius=head_rad)
				# if turned from going down to left - radius on bottom right
				elif last_blk_rel.y == -1 and next_blk_rel.x == -1:
					pygame.draw.rect(canvas, colour, block_rect, border_bottom_right_radius=head_rad)

	def move_snake(self):
		# if we're growing, we keep every element
		if self.grow == True:
			body_copy = self.body
			self.grow = False
		else:
		# if we're not growing, we drop the last element
			body_copy = self.body[:-1]
		# and add an element at first index corresponding to player input
		body_copy.insert(0, body_copy[0] + self.direction)
		self.body = body_copy

	def add_block(self):
		self.grow = True

class Food:
	def __init__(self):
		self.randomise()

	def randomise(self):
		self.x = random.randrange(0, cell_number)
		self.y = random.randrange(0, cell_number)
		self.pos = Vector2(self.x, self.y)

	def draw_food(self):
		x_pos = self.pos.x*cell_size + cell_size*0.1
		y_pos = self.pos.y*cell_size + cell_size*0.1
		food_rect = pygame.Rect(x_pos, y_pos, cell_size*0.8, cell_size*0.8)
		pygame.draw.ellipse(canvas, food_colour, food_rect)
		# we could have left it at that, but I wanted a leaf:
		# leaf_width = cell_size*0.8*0.25
		# leaf_height = cell_size*0.8*0.5
		# leaf_surf = pygame.Surface((leaf_width, leaf_height), pygame.SRCALPHA)
		# leaf_rect = pygame.Rect(0, 0, leaf_width, leaf_height)
		# pygame.draw.ellipse(leaf_surf, leaf_colour, leaf_rect)
		# canvas.blit(pygame.transform.rotate(leaf_surf, -45), (x_pos + leaf_width*2, y_pos - leaf_width*0.5))
class Main:
	def __init__(self):
		# create our objects
		self.food = Food()
		self.snake = Snake()
		self.score = 0
		self.over = False

	def update(self):
		# slither
		self.snake.move_snake()
		# eat
		self.check_collide()

	def draw_objects(self):
		self.food.draw_food()
		self.snake.draw_snake()

	def check_collide(self):
		# food with head
		if self.food.pos == self.snake.body[0]: 
			self.food.randomise()
			self.snake.add_block()
			self.score += 1	
		# head or food with body
		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				print("HIT SELF")
				self.over = True
			elif block == self.food.pos:
				self.food.randomise()
		# head with wall
		# cell_number should be gt head which should be gt 0
		if not 0 <= self.snake.body[0].x < cell_number \
				or not 0 <= self.snake.body[0].y < cell_number: 
			print("HIT WALL")
			self.over = True

	def reset(self):
		# reset our objects
		self.__init__()

# global vars
pygame.init()
pygame.display.set_caption('Snake')
cell_size = 72
cell_number = 20
half_canvas = int(cell_number*cell_size*0.5)
# the screen is for final output only - I want to smooth out some jaggies, 
# so I'll draw on the canvas surface and scale down to match the screen later
screen = pygame.display.set_mode((half_canvas, half_canvas))
canvas = pygame.Surface((cell_number*cell_size, cell_number*cell_size))
clock = pygame.time.Clock()
main_game = Main()
game_font = pygame.font.SysFont("hack.ttf", 32)
# colours
background =  ( 40,  42,  54)
font_colour = ( 98, 114, 164)
head_colour = (241, 250, 140)
food_colour = (255, 121, 198)
edge_colour = (189, 147, 249)
body_colour = (239, 175, 107)
leaf_colour = ( 80, 250, 123)
blue_colour = (139, 233, 253)
dark_white =  (248, 248, 242)
# create timer for n milliseconds - used to update game
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 200)
# bypass issue where quick succession of key-presses caused collision
# input is released with the main update event.
handled = False
# game loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN and not handled:
			if event.key == pygame.K_UP and main_game.snake.direction.y <= 0:
				main_game.snake.direction = Vector2(0,-1)
				handled = True
			elif event.key == pygame.K_DOWN and main_game.snake.direction.y >= 0:
				main_game.snake.direction = Vector2(0,1)
				handled = True		
			elif event.key == pygame.K_RIGHT and main_game.snake.direction.x >= 0:
				main_game.snake.direction = Vector2(1,0)
				handled = True
			elif event.key == pygame.K_LEFT and main_game.snake.direction.x <= 0:
				main_game.snake.direction = Vector2(-1,0)
				handled = True
		if event.type == pygame.KEYDOWN and main_game.over:
			if event.key == pygame.K_r: 
				main_game.reset()
			elif event.key == pygame.K_q: 
				pygame.quit()
				sys.exit()
		if event.type == SCREEN_UPDATE:
			if not main_game.over:
				handled = False
				main_game.update()
				# build the scene
				canvas.fill(background)
				main_game.draw_objects()
				# add a border to better define the screen edge
				border_rect = pygame.Rect(0, 0, cell_number*cell_size, cell_number*cell_size)
				pygame.draw.rect(canvas, edge_colour, border_rect, 1)
				# scale canvas and overlay it on screen
				# blit stands for 'block transfer' and basically means 'draw overlay' as far as I can gather..
				screen.blit(pygame.transform.smoothscale(canvas, (half_canvas, half_canvas)), (0, 0))
				player_score = game_font.render(str(main_game.score), True, dark_white)
				screen.blit(player_score, (660, 690))
			else:
				# display a retry/quit screen with last score
				quit_surf = pygame.Surface((cell_number*cell_size, cell_number*cell_size))
				quit_surf.fill(background)
				quit_text = game_font.render("You scored: " + str(main_game.score), True, head_colour)
				quit_surf.blit(quit_text, (270,270))
				quit_text = game_font.render("[R]eplay or [Q]uit?", True, body_colour)
				quit_surf.blit(quit_text, (270,300))
				screen.blit(quit_surf, (0,0))
			pygame.display.update()
	# check for events this many times per sec	
	# set 10x higher than UPDATE as to provide responsive controls
	clock.tick(50)
