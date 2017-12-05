import pygame
from pygame import *
import time
import random
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
done = False
screen_width = 800
screen_hieght = 600
lead_x = 0
delta_x = 0
mouse_x = 0
mouse_y = 0
block_pass = 1
block_keep = 0 
stop_x_left = False
stop_x_right = False
game_exit = False
score = 0
window = pygame.display.set_mode([screen_width, screen_hieght])
clock = pygame.time.Clock()

class Menu:
	def draw_quit():
		pygame.draw.circle(window, red, [200, 300], 100)
	def draw_play():
		pygame.draw.circle(window, blue, [600, 300], 100)


class Block(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([20, 20])
		self.image.fill(red)
		self.rect = self.image.get_rect()
	def update(self):
		self.rect.y += 5


class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([20, 20])
		self.image.fill(black)
		self.rect = self.image.get_rect()


block_list = pygame.sprite.Group()
player_list = pygame.sprite.GroupSingle()
player = Player()
player_list.add(player)

while game_exit == False:
	for event in pygame.event.get():
		if pygame.mouse.get_pressed():
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = list(pygame.mouse.get_pos(mouse_x, mouse_y))
				if pos[0] < screen_width/2:
					exit()
				elif pos[0] > screen_width/2:
					done = False
	Menu.draw_quit()
	Menu.draw_play()
	pygame.display.update()

	while not done:
		if block_pass > block_keep:
			block = Block()
			block.rect.x = random.randrange(0, screen_width-20)
			block.rect.y = random.randrange(-150, 0)
			block_list.add(block)
			block_keep += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == K_RIGHT:
					stop_x_right = True
					lead_x = 5
				if event.key == K_LEFT:
					stop_x_left = True
					lead_x = -5

				
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					if stop_x_left == True and stop_x_right == False:
						lead_x = 0
						stop_x_left = False
					if stop_x_left == True and stop_x_right == True:
						stop_x_left = False
				if event.key == pygame.K_RIGHT:
					if stop_x_right == True and stop_x_left == False:
						lead_x = 0
						stop_x_right = False
					if stop_x_right == True and stop_x_left == True:
						stop_x_right = False
	
		if player.rect.x >= screen_width-20:
			if stop_x_right == True and stop_x_left == False:
				lead_x = 0 
				stop_x_right = False
			if stop_x_left == True and stop_x_right == True:
				stop_x_right = False
				lead_x = 0

		if player.rect.x <= 0:
			if stop_x_left == True and stop_x_right == False:
				lead_x = 0 
				stop_x_left = False
			if stop_x_left == True and stop_x_right == True:
				stop_x_left = False
				lead_x = 0


		for block in block_list:
			player_hit_list = pygame.sprite.spritecollide(block, player_list, False)
			for player in player_hit_list:
				for block in block_list:
					block_list.remove(block)
				
				block_pass = 1
				block_keep = 0
				print(score)
				done = True

			if block.rect.y > screen_hieght:
				block.rect.y = random.randrange(-150, 0)
				block.rect.x = random.randrange(0, screen_width)
				score += 1
				if block_pass < 32:
					block_pass += 1

		player.rect.x += lead_x
		player.rect.y = screen_hieght - 50
		player_list.update()
		block_list.update()
		window.fill(white)
		player_list.draw(window)
		block_list.draw(window)
		pygame.display.update()
		clock.tick(60)

