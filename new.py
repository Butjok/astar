from heapq import heappush, heappop
from sys import maxint
import grid as g


F, H, ID, G, POS, PARENT_POS, OPEN, VALID = xrange(8)
X, Y = 0, 1


# TODO: use LEVEL's internal grid for A* calculations
# TODO: particularly for NODES map


def astar(grid, start_pos, goal, heuristic, max_g=maxint):

	def neighbors(pos):
		return g.neighbours(grid, pos)

	def cost(pos):
		return grid[pos[Y]][pos[X]]

	def node(g, pos, parent_pos):
		return [g + heuristic(pos, goal), heuristic(pos, goal), ids.next(), g, pos, parent_pos, True, True]

	ids = iter(xrange(maxint))

	start = node(0, start_pos, None)
	# todo: use level's tiles table
	nodes = {start_pos: start}
	heap = [start]

	while heap:
		current = heappop(heap)
		current[OPEN] = False

		if goal == current[POS]:
			path = []
			while current[PARENT_POS] is not None:
				path.append(current[POS])
				current = nodes[current[PARENT_POS]]
			path.reverse()

			return path

		for neighbor_pos in neighbors(current[POS]):
			neighbor_g = current[G] + cost(neighbor_pos)
			neighbor = nodes.get(neighbor_pos)

			# todo: move G <= max_g on top?
			if neighbor is None or (neighbor and neighbor[OPEN] and neighbor_g < neighbor[G] <= max_g):
				if neighbor:
					neighbor[VALID] = False

				# todo: dont recalculate already calculated heuristics
				nodes[neighbor_pos] = neighbor = node(neighbor_g, neighbor_pos, current[POS])
				heappush(heap, neighbor)

		while heap and not heap[0][VALID]:
			heappop(heap)

	return None
