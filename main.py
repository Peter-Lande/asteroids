import pygame, sys, objects
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.key.set_repeat(100, 50)

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Asteroids')
screenx = screen.get_width()
screeny = screen.get_height()

background = pygame.Surface((screen.get_size()))
background.fill((255, 255, 255))
background.convert()

playerObjects = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

player = objects.Player(screenx / 2, screeny / 2, screen)

playerObjects.add(player)

for x in range(0,2):
	asteroids.add(objects.LargeAsteroid(screen))

clock = pygame.time.Clock()

while player.isAlive:
	if (pygame.time.get_ticks() % 20000) == 0:
		asteroids.add(objects.LargeAsteroid(screen))
	for sprite in playerObjects:
		collision = pygame.sprite.spritecollide(sprite, asteroids, False)
		if sprite is player and collision and pygame.time.get_ticks() > 1000:
			player.isAlive = False
		for item in collision:
			item.death(asteroids)
		if not sprite.isAlive:
			playerObjects.remove(sprite)

	keys = pygame.key.get_pressed()
	if keys[K_w]:
		player.accelerate(.5)
	if keys[K_s]:
		player.accelerate(-.5)
	if keys[K_a]:
		player.angle += 4
	if keys[K_d]:
		player.angle -= 4
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			player.isAlive = False
		elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
			player.fire(playerObjects)
	playerObjects.update()
	asteroids.update()
	screen.blit(background, (0,0))
	playerObjects.draw(screen)
	asteroids.draw(screen)
	pygame.display.update()
	clock.tick(40)
pygame.quit()
