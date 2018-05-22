import random, pygame
class Object(pygame.sprite.Sprite):
	def __init__(self, x, y, screen):
		pygame.sprite.Sprite.__init__(self)
		self.screen = screen
		self.angle = 0
		self.vel = pygame.math.Vector2() #velocity vector
		self.pos = pygame.math.Vector2(x, y) #pos vector
		self.accel = pygame.math.Vector2() #acceleration vector
		self.height = 0
		self.width = 0
		self.image = pygame.Surface((self.height, self.width))
		self.original = self.image
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.isAlive = True
	def move(self):
		self.pos += self.vel
	def checkBounds(self):
		while 1:
			if self.pos[0] > self.screen.get_width():
				self.pos = pygame.math.Vector2(10 , self.pos[1])
			elif self.pos[0] < 0:
				self.pos = pygame.math.Vector2(self.screen.get_width() - 10, self.pos[1])
			elif self.pos[1] > self.screen.get_height():
				self.pos = pygame.math.Vector2(self.pos[0], 10)
			elif self.pos[1] < 0:
				self.pos = pygame.math.Vector2(self.pos[0], self.screen.get_height() - 10)
			else:
				break
	def rotate(self):
		self.image = self.original
		self.image = pygame.transform.rotate(self.image, self.angle)
	def update(self):
		pass
	def death(self, group):
		pass

class Player(Object):
	def __init__(self, x, y, screen):
		Object.__init__(self, x, y, screen)
		self.height = 20
		self.width = 10
		self.image = pygame.Surface((self.height, self.width * 2))
		self.image.fill((255, 255, 255))
		self.original = self.image
		self.rect = self.image.get_rect()
		pygame.draw.polygon(self.image, (255, 0, 0), [(self.width, 0), (0, self.height), (self.width * 2, self.height)])
	def move(self):
		if self.vel.length() < 6:
			self.vel += self.accel
			self.vel *= .95
		else:
			self.vel *= .8
		self.pos += self.vel
	def accelerate(self, mag):
		self.accel = pygame.math.Vector2(0, -mag)
		self.accel.rotate_ip(-self.angle)
	def fire(self, group):
		group.add(Bullet(self.pos, self.angle, self.screen))
	def update(self):
		self.rotate()
		self.move()
		self.checkBounds()
		self.rect.center = self.pos
		self.accel = pygame.math.Vector2()

class Bullet(Object):
	def __init__(self, pos, angle, screen):#pos is a position vector and player is a player object
		Object.__init__(self, pos[0], pos[1], screen)
		self.radius = 3
		self.vel = pygame.math.Vector2(0, -8)
		self.vel.rotate_ip(-angle)
		self.image = pygame.Surface((2 * self.radius, 2 * self.radius))
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()
		pygame.draw.circle(self.image, (0, 0, 0), (int(self.radius), int(self.radius)), self.radius)
	def checkBounds(self):
		if self.pos[0] > self.screen.get_width() or self.pos[0] < 0 or self.pos[1] > self.screen.get_height() or self.pos[1] < 0:
			self.isAlive = False
	def update(self):
		self.move()
		self.checkBounds()
		self.rect.center = self.pos

class Asteriod(Object):
	def __init__(self, screen, height, width, pos):
		Object.__init__(self, pos[0], pos[1], screen)
		self.height = height
		self.width = width
		self.image = pygame.Surface((self.width, self.height))
		self.original = self.image
		self.image.fill((255, 255, 0))
		self.rect = self.image.get_rect()
		self.vel = pygame.math.Vector2(random.randint(1, 4), random.randint(1, 4))
	def update(self):
		self.angle += 1
		self.rotate()
		self.move()
		self.checkBounds()
		self.rect.center = self.pos

class LargeAsteriod(Asteriod):
	def __init__(self, screen):
		while 1:
			self.pos = pygame.math.Vector2(random.randint(10, screen.get_width() - 10 ), random.randint(10, screen.get_height() - 10))
			if self.pos[0] < (screen.get_width() / 2) - 80 or self.pos[0] > (screen.get_width() / 2) + 80 or self.pos[1] < (screen.get_height() / 2) - 80 or self.pos[1] > (screen.get_height() / 2) + 80:
				break
		self.height = 40
		self.width = 40
		Asteriod.__init__(self, screen, self.height, self.width, self.pos)
	def death(self, group):
		group.remove(self)
		group.add(LargeAsteriod(self.screen))
		group.add(MediumAsteriod(self.screen, self.pos))
		group.add(MediumAsteriod(self.screen, self.pos))

class MediumAsteriod(Asteriod):
	def __init__(self, screen, pos):
		self.pos = pos
		self.height = 20
		self.width = 20
		Asteriod.__init__(self, screen, self.height, self.width, self.pos)
	def death(self, group):
		group.remove(self)
		group.add(SmallAsteriod(self.screen, self.pos))
		group.add(SmallAsteriod(self.screen, self.pos))

class SmallAsteriod(Asteriod):
	def __init__(self, screen, pos):
		self.pos = pos
		self.height = 10
		self.width = 10
		Asteriod.__init__(self, screen, self.height, self.width, self.pos)
	def death(self, group):
		group.remove(self)
