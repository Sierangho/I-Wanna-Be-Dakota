#IMPORTS AND GLOBALS
import os
import pygame, sys
from pygame.locals import *

import display
import world

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

GRID_X = 50
GRID_Y = 50

#RESOURCE HANDLING (LOADING IMGS, SAVES, ETC)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert() #surface
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

	
#GAME CLASSES
class Face(pygame.sprite.Sprite):
	"""face that is the player"""
	def __init__(self, rect=None):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('face.bmp')
		screen = pygame.display.get_surface()
		self.area = screen.get_rect() #screen rect
		if rect != None:
			self.rect = rect
		self.state = (0,0)
		
	
	def move(self, key_event):
		"""move the face with a key event"""
		xMove = 0
		yMove = 0
		if (key_event == K_RIGHT):
			xMove = GRID_X
		elif (key_event == K_LEFT):
			xMove = -GRID_X
		elif (key_event == K_UP):
			yMove = -GRID_Y
		elif (key_event == K_DOWN):
			yMove = GRID_Y
			
		#check that new location is in the screen area
		new_rect = self.rect.move((xMove,yMove))
		if not self.area.contains(new_rect):
			if new_rect.left < self.area.left or new_rect.right > self.area.right:
				new_rect.move_ip((-xMove,0))
			if new_rect.top < self.area.top or new_rect.bottom > self.area.bottom:
				new_rect.move_ip((0,-yMove))
		self.rect = new_rect

#OTHER FUNCTIONS


#MAIN GAME STUFF	
def main():
	#INIT THINGS
	pygame.init()
	screen = pygame.display.set_mode((400,600))
	pygame.display.set_caption('Testing')

	background = pygame.Surface(screen.get_size())
	background = background.convert() #makes stuff faster?
	background.fill((250,250,250))

	grid = display.GridSurface(6,6,50,50)
	grid.convert()
	grid.fill((100,100,100))
	grid.fill_cell((1,2),(0,0,0))
	background.blit(grid, (50,100))

	screen.blit(background, (0,0)) #display background while loading rest
	pygame.display.flip()
		

	#make game objects
	face = Face()
	allsprites = pygame.sprite.RenderUpdates(face)
	clock = pygame.time.Clock()
	
	#EVENT LOOP
	while 1:
		clock.tick(60) # cap the frame rate at 60 fps
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == KEYDOWN:
				face.move(event.key)
		allsprites.clear(screen,background)		
		dirty_rects = allsprites.draw(screen)
		pygame.display.update(dirty_rects)
		
if __name__ == '__main__': main()
