from heapq import heappush, heappop
from sys import maxint
import grid as g


F, G, H, ID, POS, PARENT, OPEN, VALID = xrange(8)
X, Y = 0, 1


def astar(grid, start_pos, goal, heuristic, max_g=maxint):

	def neighbors(pos):
		return g.neighbours(grid, pos)

	def cost(pos):
		return grid[pos[Y]][pos[X]]

	ids = iter(xrange(maxint))

	start_h = heuristic(start_pos, goal)
	start = [start_h, 0, start_h, ids.next(), start_pos, None, True, True]
	nodes = {start_pos: start}
	heap = [start]

	while heap:

		current = heappop(heap)
		current[OPEN] = False

		if goal == current[POS]:

			path = []
			while current[PARENT] is not None:
				path.append(current[POS])
				current = nodes[current[PARENT]]
			path.reverse()

			return path

		for neighbor_pos in neighbors(current[POS]):

			neighbor_g = current[G] + cost(neighbor_pos)
			neighbor = nodes.get(neighbor_pos)

			if neighbor is None:
				neighbor_h = heuristic(neighbor_pos, goal)
				neighbor = [neighbor_g + neighbor_h, neighbor_g, neighbor_h, ids.next(), neighbor_pos, current[POS], True, True]
				nodes[neighbor_pos] = neighbor
				heappush(heap, neighbor)

			elif neighbor[OPEN] and neighbor_g < neighbor[G] <= max_g:
				neighbor[VALID] = False

				nodes[neighbor_pos] = neighbor = neighbor[:]
				neighbor[F] = neighbor_g + neighbor[H]
				neighbor[ID] = ids.next()
				neighbor[G] = neighbor_g
				neighbor[VALID] = True
				neighbor[PARENT] = current[POS]

				heappush(heap, neighbor)

		while heap and not heap[0][VALID]:
			heappop(heap)

	return []
