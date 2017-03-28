import random


X, Y = 0, 1


def generate(maxval, width, height):
	return [[(random.randrange(1))+1 for x in range(width)] for y in range(height)]


def neighbours(grid, pos):
	height = len(grid)
	assert height > 0
	width = len(grid[0])
	assert width > 0

	def in_bounds(p):
		return 0 <= p[X] < width and 0 <= p[Y] < height

	offsets = ((1, 0), (-1, 0), (0, 1), (0, -1))
	return [(pos[X] + ox, pos[Y] + oy) for ox, oy in offsets if in_bounds((pos[X] + ox, pos[Y] + oy))]


def display(grid, path=None):
	height = len(grid)
	assert height > 0
	width = len(grid[0])
	assert width > 0

	minval = min([min(grid[y]) for y in range(height)])
	maxval = max([max(grid[y]) for y in range(height)])
	magnitude = maxval - minval

	def val_to_char(val):
		chars = '_=#'
		percent = float(val - minval) / magnitude
		return chars[int((len(chars) - 1) * percent)]

	screen = [[''] * width for y in range(height)]

	for y in range(height):
		for x in range(width):
			screen[y][x] = val_to_char(grid[y][x])

	if path:
		for p in path:
			screen[p[Y]][p[X]] = '.'

	for y in range(height):
		print(' '.join(screen[y]))