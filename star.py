import time
import grid


X, Y = 0, 1


def manhattan(p1, p2):
	return abs(p1[X] - p2[X]) + abs(p1[Y] - p2[Y])


width = 100
height = 100


import astar as a
import new as a2





def main():
	start = (0, 0)
	goal = (width - 1, height - 1)
	g = grid.generate(10, width, height)

	_goal = lambda p: p == goal
	_neigh = lambda pos: grid.neighbours(g, pos)
	_cost2 = lambda _, pos: g[pos[Y]][pos[X]]

	zero = lambda a, b: 0

	_manhattan = lambda p: manhattan(p, goal)

	t1=time.time()
	path = a.astar(start, _neigh, _goal, 0, _cost2, _manhattan)
	t2 = time.time()
	path2 = a2.astar(
		g,
		start,
		goal,
		manhattan
	)
	t3 = time.time()

	print(t2-t1)
	print(t3 - t2)

	if path != path2:
		print('!!!!!different!!!!!!')
	else:
		print('good')


if __name__ == '__main__':
	main()