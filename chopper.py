#!/bin/python3
import pygame as pg
from pygame.locals import *
import sys
# from icecream import ic 
import random
import math

class Chopper():
	def __init__(self):
		# define a surface w/ alpha & get its rect
		self.width = 66
		self.height = 31
		self.surf = pg.Surface((self.width, self.height), pg.SRCALPHA)
		self.rect = self.surf.get_rect()
		self.crash = False
		# rotor animation attributes
		self.rotor_pos = list(range(5, 70, 5))
		self.count = 0
		# tail animation - pivot
		self.startpoint = pg.math.Vector2(3, 12)
		# frc from start - so, + 3 along x
		self.endpoint = pg.math.Vector2(3, 0)
		self.rotor_angle = 0
		# movement
		self.climb_speed = -0.2 * frc
		self.fall_speed = 0.1 * frc
		self.momentum = 0
		self.is_climbing = False

	def draw(self):
		# rotor 
		pg.draw.polygon(self.surf, col_grey, ((5, 0), (65, 0), (65, 1), (37, 1), 
											 (37, 5), (35, 5), (35, 1), (5, 1)))
		# boom
		chopper_boom = pg.Rect(5, 10, 30, 5)
		pg.draw.rect(self.surf, col_grey, chopper_boom, 2)
		# tail
		pg.draw.polygon(self.surf, col_green, ((0,4), (6,11), (6,13), (0,20)))
		# body
		chopper_cab = pg.Rect(40, 9, 14, 14)
		chopper_body = pg.Rect(28, 6, 14, 17)
		pg.draw.rect(self.surf, col_purple, chopper_cab, 2, border_top_right_radius=7, border_bottom_right_radius=7)
		pg.draw.rect(self.surf, col_green, chopper_body, border_bottom_left_radius=8)
		# sled
		pg.draw.line(self.surf, col_grey, (34,23), (34, 29), 2)
		pg.draw.line(self.surf, col_grey, (48,23), (48, 29), 2)
		pg.draw.line(self.surf, col_green, (28,29), (50, 29), 2)
		pg.draw.line(self.surf, col_green, (50,29), (54, 27), 2)

	def animate(self):
		# % len() keeps count between 0 and len
		self.count = (self.count + 1) % len(self.rotor_pos)
		pos = self.rotor_pos[self.count]
		pg.draw.line(self.surf, col_white, (pos, 0), (pos+5, 0), 2)
		# % 360 to keep the angle between 0 and 360
		self.rotor_angle = (self.rotor_angle+20) % 360
		# the current endpoint is the startpoint vector + the rotated original endpoint vector.
		self.current_endpoint = self.startpoint + self.endpoint.rotate(self.rotor_angle)
		pg.draw.line(self.surf, 'black', self.startpoint, self.current_endpoint, 1)
		# make an opposing blade
		self.current_endpoint = self.startpoint - self.endpoint.rotate(self.rotor_angle)
		pg.draw.line(self.surf, 'black', self.startpoint, self.current_endpoint, 1)

	def explode(self):
		if random.randint(0, 1) == 1: col = col_yellow
		else: col = col_orange
		radius = random.randint(5, 10)
		x = random.randint(radius, self.width-radius)
		y = random.randint(radius, self.height-radius)
		pg.draw.circle(self.surf, col, (x, y), radius)

class Terrain():
	def __init__(self,):
		self.distance = 0
		self.frequency = 0.5
		self.amplitude = screen_height*0.25 - 1
		self.axis = screen_height*0.75
		self.lower_level = 0
		self.upper_level = 0
		self.surf = pg.Surface((screen_width,screen_height), pg.SRCALPHA)

	def draw(self):
		self.distance += frc
		self.lower_level = int(math.sin(self.distance/screen_width * 2 * self.frequency * math.pi) * self.amplitude + self.axis) 
		self.upper_level = self.lower_level - 2*(screen_height - self.axis)
		self.surf.scroll(-frc,0)
		
		if potato:
			# draw a coloured line & make transparent between upper & lower levels to a make tunnel
			pg.draw.line(self.surf, col_orange,  (screen_width - 1, screen_height), (screen_width - 1, 0), frc*2-1)
			pg.draw.line(self.surf, (0,0,0,0),  (screen_width - 1, self.lower_level), (screen_width - 1, self.upper_level), frc*2-1)
		else:
			# add gradient to terrain - very costly!
			# inspired by Wireframe, issue 22, page 41, (https://wireframe.raspberrypi.org/issues/22)
			a = col_orange
			b = col_yellow
			l = screen_height - self.lower_level + 100
			u = self.upper_level + 100
			# steps required for each colour value to change by 'l' or 'u' above
			lower_rate = (float(b[0]-a[0])/l, float(b[1]-a[1])/l, float(b[2]-a[2])/l)
			upper_rate = (float(a[0]-b[0])/u, float(a[1]-b[1])/u, float(a[2]-b[2])/u)
			for i in range(0, screen_height):
				c = (0,0,0,0)
				if i > self.lower_level:
					c = (
						limit(a[0]+(lower_rate[0]*(i-self.lower_level)),0,255),
						limit(a[1]+(lower_rate[1]*(i-self.lower_level)),0,255),
						limit(a[2]+(lower_rate[2]*(i-self.lower_level)),0,255)
					)
				elif i < self.upper_level:
					c = (
						limit(a[0]+(upper_rate[0]*(i-self.upper_level)),0,255),
						limit(a[1]+(upper_rate[1]*(i-self.upper_level)),0,255),
						limit(a[2]+(upper_rate[2]*(i-self.upper_level)),0,255)
					)
				self.surf.set_at((screen_width - 1, i), c)
			
class Obstacle(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.width = 30
		self.height = random.randint(self.width*2, screen_height*0.5)
		self.sprite_surf = pg.Surface((self.width, self.height))
		self.sprite_surf.fill(col_red) 
		self.rect = self.sprite_surf.get_rect()
		self.passed = False

class PowerUp(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.radius = 10
		self.sprite_surf = pg.Surface((self.radius*2, self.radius*2),pg.SRCALPHA)
		pg.draw.circle(self.sprite_surf, col_cyan, (self.radius, self.radius), self.radius)
		self.rect = self.sprite_surf.get_rect()
		self.collected = False

class HUD():
	def __init__(self):
		self.height = 30
		self.width = screen_width
		self.surf = pg.Surface((self.width, self.height),pg.SRCALPHA)

	def update(self, speed, score):
		self.speed = int(speed)
		self.score = score
		self.surf.fill((0,0,0,0))
		# polygons to render on
		pg.draw.polygon(self.surf, col_night, ((0,0), (160,0), (190,30), (0,30)))
		pg.draw.polygon(self.surf, col_night, ((self.width,0), (self.width-160,0), (self.width-190,30), (self.width,30)))
		self.speed_text = font.render("Speed = " + str(self.speed) + "kn", True, col_orange)
		self.score_text = font.render("Score = " + str(self.score), True, col_orange)
		self.surf.blit(self.speed_text, (20,8))
		self.surf.blit(self.score_text, (self.width-140,8))
		self.surf.set_alpha(127)

class Main():
	def __init__(self):
		# init player & terrain objects
		self.player = Chopper()
		self.tunnel = Terrain()
		self.hud = HUD()
		self.player.rect.x = screen_width*0.33 - self.player.width
		self.player.rect.y = screen_height*0.5 - self.player.height*0.5
		# store obstacles in a group
		self.obstacle_group = pg.sprite.Group()
		# store power-ups in a group - one is automatically removed when one is added
		self.pup_group = pg.sprite.GroupSingle()
		# keep track of game state
		self.speed = 5
		self.score = 0
		self.score_multi = 1
		self.pup_requests = 0
		self.over = False
		# timers
		self.obs_timer = MyTimer(1000)
		self.pup_timer = MyTimer(500, False)
		self.gov_timer = MyTimer(500, False)


	def update(self):
		# process timers
		time_now = pg.time.get_ticks()
		if self.obs_timer.duration <= time_now - self.obs_timer.start_time:
			self.add_obstacle()
			self.obs_timer.reset()
			# enable pup timer
			self.pup_timer.reset()
			self.pup_timer.active = True	
		elif self.pup_timer.active and self.pup_timer.duration <= time_now - self.pup_timer.start_time:
			self.add_pup()
			self.pup_timer.active = False
		elif self.gov_timer.active and self.gov_timer.duration <= time_now - self.gov_timer.start_time:
			self.over = True
			self.gov_timer.active = False
		# trigger explosion & game over timer, or draw player
		if self.player.crash: 
			self.player.explode()
			if not self.gov_timer.active:
				self.gov_timer.reset()
				self.gov_timer.active = True
		else: 
			self.player.draw()
			self.player.animate()
		
		# move player
		self.player.momentum += (self.player.climb_speed if self.player.is_climbing else self.player.fall_speed) 
		# damper - 0.99 at 100fps, 0.98 at 50
		self.player.momentum *= 1 - frc * 0.01
		self.player.rect.y += self.player.momentum * frc
		self.player.rect.y = limit(self.player.rect.y, 1, screen_height - self.player.height - 1)
		
		# draw terrain
		for i in range(math.ceil(self.speed)): 
			self.tunnel.draw()

		# check for chopper crash with terrain by checking if it's over a drawn pixel
		if (   self.tunnel.surf.get_at(self.player.rect.topleft) != (0,0,0,0)
			or self.tunnel.surf.get_at(self.player.rect.midtop) != (0,0,0,0)
			or self.tunnel.surf.get_at(self.player.rect.topright) != (0,0,0,0)
			or self.tunnel.surf.get_at(self.player.rect.midright) != (0,0,0,0)
			or self.tunnel.surf.get_at(self.player.rect.midbottom) != (0,0,0,0)
			or self.tunnel.surf.get_at(self.player.rect.midleft) != (0,0,0,0)   ):
			# note no 'bottomleft' or 'bottomright' as they are not filled
			# should create a mask for pixel perfect collision...
			self.player.crash = True
			# ic(self.player.crash)	
		
		# move, check & remove obstacles
		for obstacle in self.obstacle_group:
			obstacle.rect.x -= self.speed * frc
			screen.blit(obstacle.sprite_surf, obstacle.rect)
			# check obstacle collisions
			if obstacle.passed == False:
				if self.player.rect.colliderect(obstacle.rect):
					self.player.crash = True
					# ic(self.player.crash)	
				# update score
				elif self.player.rect.x > obstacle.rect.x + obstacle.width:
					self.score += int(10 * self.score_multi)
					obstacle.passed = True
					# ic(self.score)
			# remove ones that have passed the screen
			elif obstacle.rect.x + obstacle.width < 0:
				self.obstacle_group.remove(obstacle)
				
		# move pup
		for pup in self.pup_group:
			pup.rect.x -= self.speed * frc
			screen.blit(pup.sprite_surf, pup.rect)
			# check for player pick-up
			if pup.collected == False:
				if self.player.rect.colliderect(pup.rect):
					# award extra points - plucking numbers out of thin air...
					if self.score_multi < 3.5: 
						self.speed += 1
						self.score_multi += 0.5
						#ic(speed)
					self.pup_group.remove(pup)
				# instead of using a cool-down timer:
				elif pup.rect.x + pup.radius * 2 < 0:
					if self.score_multi > 1: 
						self.speed -= 1
						self.score_multi -= 0.5
					self.pup_group.remove(pup)
					#ic(speed)
		
		# update hud elements - speed*20 results in a more meaningful figure
		self.hud.update(self.speed*20, self.score)

	def add_obstacle(self):
		self.obstacle = Obstacle()
		self.obstacle.rect.x = screen_width
		if random.randint(0, 1) == 1:
			self.obstacle.rect.y = self.tunnel.upper_level - (self.obstacle.height * 0.5)
		else:
			self.obstacle.rect.y = self.tunnel.lower_level - (self.obstacle.height * 0.5)
		self.obstacle_group.add(self.obstacle)
		
	def add_pup(self):	
		# every 10th request will give us a pup
		self.pup_requests = (self.pup_requests + 1) % 10
		if self.pup_requests == 0:
			self.pup = PowerUp()
			self.pup.rect.x = screen_width 
			self.pup.rect.y = random.randint(self.tunnel.upper_level, self.tunnel.lower_level - self.pup.radius * 2)
			self.pup_group.add(self.pup)

	def reset(self):
		self.__init__()

class MyTimer():
	# create simple timer objects, because pg.USEREVENT sucks balls
	def __init__(self, duration, active = True):
		self.start_time = pg.time.get_ticks()
		self.duration = duration
		self.active = active
	
	def reset(self):
		self.start_time = pg.time.get_ticks()

# colour scheme (dracula)
col_night	= ( 40,  42,  54)	
col_grey	= ( 68,  71,  90)	
col_white	= (248, 248, 242)	
col_dkblue	= ( 98, 114, 164)	
col_cyan	= (139, 233, 253)	
col_green	= ( 80, 250, 123)	
col_orange	= (255, 184, 108)	
col_pink	= (255, 121, 198)	
col_purple	= (189, 147, 249)	
col_red		= (255,  85,  85)	
col_yellow	= (241, 250, 140)

# init pygame & main vars
pg.init()
pg.event.set_allowed([QUIT, KEYDOWN, KEYUP])
clock = pg.time.Clock()
pg.display.set_caption('Proc-opter')
screen_width = 960
screen_height = 540
screen = pg.display.set_mode((screen_width, screen_height))
font = pg.font.SysFont('freesansbold.ttf', 24)

# toggle intensity - beyond the fps cap, this mainly affects terrain creation
# frc is my attempt at frame rate compensation to keep gameplay consistent...
potato = False
if potato:
	fps = 50
	frc = 2
else:
	fps = 100
	frc = 1

# create & manage the main game objects
main_game = Main()

# clamp values to given range - uses less cpu than numpy.clip()
def limit(n, minn, maxn):
	return max(min(maxn, n), minn)

# game loop
while True:
	for event in pg.event.get():
		if event.type == QUIT:
			pg.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_UP:
				main_game.player.is_climbing = True 
			elif event.key == K_r and main_game.over:
				main_game.reset()
			elif event.key == K_q and main_game.over:
				pg.quit()
				sys.exit()
			elif event.key == K_p: 
				# toggle potato mode
				potato = not potato
		elif event.type == KEYUP:
			if event.key == K_UP:
				main_game.player.is_climbing = False

	# background
	screen.fill(col_night)
	
	# render appropriate screen - game over or main game
	if main_game.over:
		ovr_surf = pg.Surface((screen_width, screen_height))
		ovr_surf.fill(col_red)
		border_rect = pg.Rect(0, 0, screen_width, screen_height)
		pg.draw.rect(ovr_surf, col_yellow, border_rect, 5)
		ovr_text = font.render("You scored: " + str(main_game.score), True, col_white)
		ovr_surf.blit(ovr_text, (400,250))
		ovr_text = font.render("[R]eplay or [Q]uit?", True, col_grey)
		ovr_surf.blit(ovr_text, (400,280))
		screen.blit(ovr_surf, (0,0))
	else:
		main_game.update()
		screen.blit(main_game.tunnel.surf, (0,0))
		screen.blit(main_game.player.surf, main_game.player.rect)
		screen.blit(main_game.hud.surf, (0,screen_height-main_game.hud.height))

	pg.display.flip()
	clock.tick(fps)
