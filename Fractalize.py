import pygame as pg
import numpy as np
import numpy.random as rd

RADS = np.pi/180

class linesegment():

	def __init__(self, a, b):
		self.start = a
		self.end = b

	def fract(self):
		angle = (60 * rd.rand() - 30) * RADS
		segment = (self.end - self.start) * (rd.rand()*.6 + .2)
		xhat = np.cos(angle)
		yhat = np.sin(angle)
		rotmat = np.array([[xhat, -yhat],[yhat, xhat]])
		segmag = np.sqrt(np.dot(segment,segment))
		rmag = segmag/np.cos(angle)
		seghat = segment / segmag
		rsegment = rmag * np.dot(rotmat,seghat)
		rsegment = np.array(map(round, rsegment))
		return [linesegment(self.start, self.start + rsegment), linesegment(self.start + rsegment, self.end)]

	def __repr__(self):
		return str(self.start) + "  " + str(self.end)
		
		
class Fractalize(pg.sprite.Sprite):

	def __init__(self, edges, center, group):
		#Takes list of edges, line segments, draws them to self.image, iterates a fractal pattern on those segments.
		super(Fractalize, self).__init__(group)
		self.edges = edges
		self.numedges = len(self.edges)
		
		self.draw()
		self.image = self.image.convert_alpha()
		self.rect.center = center

	def define(self):
		xvals = [x.start[0] for x in self.edges]
		yvals = [y.start[1] for y in self.edges]
		self.min = np.array([min(xvals), min(yvals)])
		self.max = np.array([max(xvals), max(yvals)])
		dimensions = self.max - self.min
		dimensions += 50
		return dimensions
	
	def draw(self):
		#Draw edge set
		points = [x.start for x in self.edges]
		points.append(self.edges[-1].end)
		dimensions = self.define()
		self.image = pg.Surface((500, 500))
		self.rect = self.image.get_rect()
		pg.draw.lines(self.image, (0, 0, 255), 0, points, 3)

	def update(self):
		self.fract()
		if len(self.edges) > self.numedges:
			self.numedges = len(self.edges)
			self.draw()

	def fract(self):
		self.edges = [item for edge in self.edges for item in edge.fract()]

if __name__ == "__main__":
	pg.init()
	screen = pg.display.set_mode((800,600))
	bg = pg.Surface(screen.get_size())
	bg.fill((0,0,0))
	scRect = screen.get_rect()
	startingpoints = [np.array([np.random.randint(200,600), np.random.randint(100,500)]) for x in range(2)]
	edges =[linesegment( startingpoints[0], startingpoints[1] ) ]
	fractal = pg.sprite.Group()
	#fractal.add(Fractalize(edges))
	Fractalize(edges, scRect.center, fractal)
	mainloop = True
	clock = pg.time.Clock()
	FPS = 30
	buttonPane = pg.Surface((100, 25))
	buttonRect = buttonPane.get_rect(center = (scRect.centerx, scRect.bottom - 50))
	buttonPane.fill((0, 255, 0))
	buttonFont = pg.font.SysFont("arial", 12)
	buttonPane.blit(buttonFont.render("Fractalize", 0, (255, 255, 255)), (5, 5))
	screen.blit(bg, (0,0))
	screen.blit(buttonPane, buttonRect)

	
	while mainloop:
		sec = clock.tick(FPS)/1000.0

		for event in pg.event.get():
			if event.type == pg.QUIT:
				mainloop = False
			elif event.type == pg.MOUSEBUTTONDOWN:
				if pg.mouse.get_pressed()[0] and buttonRect.collidepoint(pg.mouse.get_pos()):
					fractal.clear(screen, bg)
					fractal.update()
					fractal.draw(screen)
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					mainloop = False
			else:
				pass

		pg.display.flip()
	pg.quit()
	
