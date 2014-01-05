import pygame
class GridSurface(pygame.Surface):
	"""Surface with paramter grid mapping coordinates to subsurfaces"""
	def __init__(self, rows, cols, cell_width, cell_height):
		pygame.Surface.__init__(self,(rows*cell_width,cols*cell_height))
		self.rows = rows
		self.cols = cols
		self.cell_width = cell_width
		self.cell_height = cell_height
		self.grid = {}
		for c in range(cols):
			for r in range(rows):
				self.grid[(r,c)] = self.subsurface(pygame.Rect(c*cell_width, r*cell_height, cell_width, cell_height))
	
	"""helper for blitting a cell location from a source Surface """
	def blit_cell(self, loc, source):
		self.grid[loc].blit(source)
	
	def fill_cell(self,loc, color):
		self.grid[loc].fill(color)
