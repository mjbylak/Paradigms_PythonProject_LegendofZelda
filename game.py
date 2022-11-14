from tkinter import Image, image_names
from wsgiref.util import request_uri
import pygame
import time

from pygame.locals import*
from time import sleep

class Model():

	def __init__(self):
		self.sprites = []
		self.link = Link(100, 100, 45, 45)
		self.sprites.append(self.link)
		self.sprites.append(Brick(0, 0, 50, 50))
		self.sprites.append(Brick(-50, 0, 50, 50))
		self.sprites.append(Brick(0, -50, 50, 50))
		self.sprites.append(Brick(-50, -50, 50, 50))
		self.sprites.append(Pot(300, 300, 50, 50))
		
		for i in range(20):
			self.sprites.append(Brick(50*i, 0, 50, 50))
			self.sprites.append(Brick(0, 50*i, 50, 50))
			self.sprites.append(Brick(950, 50*i, 50, 50))
			self.sprites.append(Brick(50*i, 950, 50, 50))
		
		for i in range(10):
			self.sprites.append( Brick(9*50, 50*i, 50, 50))
			self.sprites.append( Brick(10*50, 50*i, 50, 50))
		
		for i in range(7):
			self.sprites.append( Brick(50*i, 9*50, 50, 50))
			self.sprites.append( Brick(50*i, 10*50, 50, 50))
			self.sprites.append( Brick(10*50, 50*i+500, 50, 50))
			self.sprites.append( Brick(9*50, 50*i+500, 50, 50))
			
		for i in range(5):
			self.sprites.append( Pot(150*i + 100, 150, 50, 50))
			self.sprites.append( Pot(150, 300*i/2+100, 50, 50))
			self.sprites.append( Brick(50*i+550, 500, 50, 50))
			self.sprites.append( Brick(50*i+550, 450, 50, 50))
		

	def checkCollision(self, sprite, sprite2):
		if ((sprite2.x + sprite2.w <= sprite.x 
			or sprite2.x >= sprite.x + sprite.w) 
			or (sprite2.y + sprite2.h <= sprite.y 
			or sprite2.y >= sprite.y + sprite.h)):
				return False
		return True

	def update(self):
		for sprite in self.sprites:
			for sprite2 in self.sprites:
				if sprite.isPot() and ((sprite2.isBrick() or sprite2.isBoomerang()) and self.checkCollision(sprite, sprite2)):
					sprite.potBreak()
					if sprite2.isBoomerang():
						sprite2.isActive = False

				if sprite.isBoomerang() and (sprite != sprite2):
					if self.checkCollision(sprite, sprite2) and sprite2.isLink() == False:
						sprite.isActive = False

			if sprite.update() == False: sprite.isActive = False
			if sprite.isActive == False:
				self.sprites.remove(sprite)
				break

			if (sprite.isLink() == False):
				if (self.checkCollision(sprite, self.link)):
					self.link.repelLink(sprite)
					if(sprite.isPot()):
						sprite.potMovement(self.sprites[0])
			sprite.update()

class View():
	def __init__(self, model):
		screen_size = (500,500)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model
		self.room_x = 0
		self.room_y = 0
		# self.model.rect = self.sprites.get_rect()

	def update(self):
		self.screen.fill([120,38,132])
		for sprite in self.model.sprites:
			self.screen.blit(sprite.images[sprite.currImage], (sprite.x- self.room_x, sprite.y - self.room_y)) #, (sprite.w, sprite.h)
			#print(sprite.currImage)
		pygame.display.flip()
		
class Controller():
	def __init__(self, model, view): #potentially add view
		self.view = view
		self.model = model
		self.keyRight = False
		self.keyLeft = False
		self.key_Up = False
		self.key_Down = False
		self.boomeranging = False
		self.moving = 0
		self.keep_going = True

	def update(self):

		self.model.link.getPrevious()

		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
				if event.key == K_RIGHT:
					self.keyRight = True
				if event.key == K_LEFT:
					self.keyLeft = True
				if event.key == K_UP:
					self.key_Up = True
				if event.key == K_DOWN:
					self.key_Down = True
				if event.key == K_LCTRL:
					self.boomeranging = True
					
			if event.type == KEYUP:
				if event.key == K_RIGHT:
					self.keyRight = False
				if event.key == K_LEFT:
					self.keyLeft = False
				if event.key == K_UP:
					self.key_Up = False
				if event.key == K_DOWN:
					self.key_Down = False
				if event.key == K_LCTRL:
					self.boomeranging = False
				
		# Boomerang stuff
		if(self.boomeranging):
			self.model.sprites.append(Boomerang(self.model.link.x + self.model.link.w / 2, self.model.link.y + self.model.link.h / 2, 10, 10, self.model.link.dir))
			self.boomeranging  = False

		#MOVING RIGHT
		if(self.keyRight):
			if(self.moving >= 10): self.moving = 0

			self.model.link.x += self.model.link.speed
			self.key_Up = False
			self.key_Down = False
			self.model.sprites[0].currImage = self.moving + 29
			self.moving+=1

			if self.model.link.x >= -5 and self.model.link.x <= 5: 
				self.view.room_x = 0
			if self.model.link.x >= 495 and self.model.link.x <= 505: 
				self.view.room_x = 500
			if self.model.link.x >= 995 and self.model.link.x <= 1005: 
				self.view.room_x = 1000
			self.model.link.dir = 1
		
		
		#MOVING LEFT
		if(self.keyLeft):
			if(self.moving >= 10): 
				self.moving = 0
			
			self.model.link.x -= self.model.link.speed
			self.key_Up = False
			self.key_Down = False
			self.model.link.currImage = self.moving + 13
			self.moving+=1
			
			if self.model.link.x >= -5 and self.model.link.x <= 5:
				self.view.room_x =-500
			if self.model.link.x >= 495 and self.model.link.x <= 505:
				self.view.room_x=0
			if self.model.link.x >= 995 and self.model.link.x <= 1005:
				self.view.room_x=500
			self.model.link.dir = 3
		
		
		#MOVING UP
		if(self.key_Up):
			if(self.moving >= 11):
				self.moving = 0
			
				
			self.model.link.y -= self.model.link.speed
			self.keyLeft = False
			self.keyRight = False
			self.model.link.currImage = self.moving + 39
			self.moving += 1
			
			if (self.model.link.y >= -5 and self.model.link.y <= 5):
				self.view.room_y =-500
			if (self.model.link.y >= 495 and self.model.link.y <= 505):
				self.view.room_y=0
			self.model.link.dir = 0
		
		
		#MOVING DOWN
		if(self.key_Down):
			if(self.moving >= 10):
				self.moving = 0

			self.model.link.y+= self.model.link.speed
			self.keyLeft = False
			self.keyRight = False
			self.model.link.currImage = self.moving + 3
			self.moving+=1
			self.model.link.dir = 2

			if (self.model.link.y >= -5 and self.model.link.y <= 5):
				self.view.room_y =0
			if (self.model.link.y >= 495 and self.model.link.y <= 505):
				self.view.room_y = 500

	def setView(self, v):
		self.view = v

class Sprite():
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.isActive = True
		self.currImage = 0
	
	def isLink(self):
		return False

	def isBrick(self):
		return False

	def isPot(self):
		return False

	def isBoomerang(self):
		return False

class Link(Sprite):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h)
		self.w = 45
		self.h = 45
		self.pX = 100
		self.pY = 100
		self.currImage = 0
		self.dir = 2
		self.speed = 15

		#link images
		self.images = []
		for i in range(50):
			name = "link_images/link ("; name = name + str(i+1); name += ").png"
			self.image1 = pygame.image.load(name)
			self.image1 = pygame.transform.scale(self.image1, (50, 50))
			self.images.append(self.image1)

	def getPrevious(self):
		self.pX = self.x
		self.pY = self.y

	def isLink(self):
		super().isLink()
		return True

	def update(self):
		return True

	def repelLink(self, sprite):
		if(self.x + self.w >= sprite.x and self.pX <= sprite.x):
			self.x=self.pX 
		
		if(self.x <= sprite.x + 50 and self.pX >= sprite.x + 50):
			self.x=self.pX
		
		if(self.y >= sprite.y - 50 and self.pY <= sprite.y - 50):
			self.y=self.pY
		
		if(self.y-self.h <= sprite.y and self.pY >= sprite.y + 50):
			self.y=self.pY
		
class Brick(Sprite):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h)
		# self.w = 45
		# self.h = 45
		self.pX = 0
		self.pY = 0
		self.currImage = 0
		
		self.images = []
		self.image1 = pygame.image.load("brick.png")
		self.images.append(self.image1)
	
	def update(self):
		return True

	def isBrick(self):
		super().isBrick()
		return True

class Pot(Sprite):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h)
		self.w = 50
		self.h = 50
		self.pX = 0
		self.pY = 0
		self.currImage = 0
		self.delay = 100
		self.isBroke = False
		self.isSchmovin = False
		self.dir = 0
		self.slideSpeed = 3
		
		self.images = []
		self.image1 = pygame.image.load("pot.png")
		self.images.append(self.image1)
		self.image1 = pygame.image.load("pot_broken.png")
		self.images.append(self.image1)

	def potBreak(self):
		self.currImage = 1
		self.isBroke = True
	
	
	def potMovement(self, link):
		if self.isBroke == False:
			self.dir = link.dir
			self.isSchmovin = True
		
	
	
	def update(self):
		if (self.isSchmovin):
			if (self.dir == 0):
				self.y -= self.slideSpeed
			elif(self.dir == 1):
				self.x += self.slideSpeed
			elif (self.dir == 2):
				self.y += self.slideSpeed
			elif (self.dir == 3):
				self.x -= self.slideSpeed
		
		if (self.isBroke):
			self.isSchmovin = False
			self.delay-=1
		
		if(self.delay <= 0):
			return False
		
		return True
	
	
	def isPot(self):
		super().isPot()
		return True
	
class Boomerang(Sprite):
	def __init__(self, x, y, w, h, dir):
		super().__init__(x, y, w, h)
		self.w = w
		self.h = h
		self.dir = dir
		self.currImage = self.dir
		self.speed = 5
		self.count = 0

		self.images = []
		self.image1 = pygame.image.load("boomerang0.png")
		self.images.append(self.image1)
		self.image1 = pygame.image.load("boomerang1.png")
		self.images.append(self.image1)
		self.image1 = pygame.image.load("boomerang2.png")
		self.images.append(self.image1)
		self.image1 = pygame.image.load("boomerang3.png")
		self.images.append(self.image1)
	
	def update(self):
		if(self.dir == 0):
			self.y-=self.speed
		elif(self.dir == 1):
			self.x+=self.speed
		elif(self.dir == 2):
			self.y+=self.speed
		elif(self.dir == 3):
			self.x-=self.speed
		
		#making the boomerang pictures change slower
		if(self.count == 10):
			self.currImage += 1	
			self.count = 0
		else:
			self.count += 1
		if (self.currImage == 3):
			self.currImage = 0
		return True

	def isBoomerang(self):
		super().isBoomerang()
		return True


# print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
model = Model()
view = View(model)
controller = Controller(model, view)

while controller.keep_going:
	controller.update()
	model.update()
	view.update()
	sleep(0.02)
	
# print("Goodbye")