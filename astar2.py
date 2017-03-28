from heapq import heappush, heappop
from sys import maxint
import grid as g


# looks like NUM is used to generate unique ids for new lists to prevent python from caching them
F, H, ID, G, POS, OPEN, VALID, PARENT = xrange(8)


X, Y = 0, 1

ids = iter(xrange(maxint))


def astar(grid, start_pos, goal, heuristic, max_g=maxint):

	class Node:
		def __init__(self, g, pos, parent_pos=None, is_open=True, is_valid=True):
			self.pos = pos
			self.h = heuristic(self.pos, goal)
			self.g = g
			self.f = self.g + self.h
			self.parent_pos = parent_pos
			self.is_open = is_open

			# when this is false, it means that node's G value was updated
			# this means that all entries of heap pointing to this node should be ignored
			# new entries pointing to the new node with actual G, H, F values are enqueued to heap
			self.is_valid = is_valid

	def neighbors(pos):
		return g.neighbours(grid, pos)

	def cost(pos):
		return grid[pos[Y]][pos[X]]

	# ids = iter(xrange(maxint))
	# start_h = heuristic(start_pos, goal)
	# start = [start_h, start_h, ids.next(), 0, start_pos, True, True, None]
	# # start = Node(0, start_pos)
	#
	# # Track all nodes seen so far.
	# nodes = {start_pos: start}
	#
	# # Maintain a heap of nodes.
	# heap = [start]

	start = Node(0, start_pos)
	nodes = {start_pos: start}
	heap = [(start.f, start)]

	while heap:

		# Pop the next node from the heap.
		# current = heappop(heap)
		# current[OPEN] = False

		f, current = heappop(heap)
		current.is_open = False

		# Have we reached the goal?
		# if goal == current[POS]:
		if goal == current.pos:

			# print(nodes[current[POS]][G])
			#
			# path = []
			# while current[PARENT] is not None:
			#	 path.append(current[POS])
			#	 current = nodes[current[PARENT]]
			# path.reverse()
			# return path

			print(nodes[current.pos].g)

			path = []
			while current.parent_pos is not None:
				path.append(current.pos)
				current = nodes[current.parent_pos]
			path.reverse()
			return path
			
		# Visit the neighbors of the current node.
		for neighbor_pos in neighbors(current.pos):
			new_g = current.g + cost(neighbor_pos)
			neighbor = nodes.get(neighbor_pos)
			if neighbor is None:

				neighbor = Node(new_g, neighbor_pos)
				heappush(heap, (neighbor.f, neighbor))
				nodes[neighbor_pos] = neighbor

			elif new_g <= max_g and new_g < neighbor.g and neighbor.is_open:

				neighbor.is_valid = False

				nodes[neighbor_pos] = neighbor = Node(new_g, neighbor_pos, current.pos)

				heappush(heap, (neighbor.f, neighbor))

		while heap and not heap[0][1].is_valid:
			heappop(heap)

		# # Visit the neighbors of the current node.
		# for neighbor_pos in neighbors(current[POS]):
		#	 neighbor_g = current[G] + cost(neighbor_pos)
		#	 neighbor = nodes.get(neighbor_pos)
		#	 if neighbor is None:
		#
		#		 neighbor_h = heuristic(neighbor_pos, goal)
		#		 neighbor = [neighbor_g + neighbor_h, neighbor_h, ids.next(),
		#					 neighbor_g, neighbor_pos, True, True, current[POS]]
		#		 heappush(heap, neighbor)
		#		 nodes[neighbor_pos] = neighbor
		#
		#	 elif neighbor_g <= max_g and neighbor_g < neighbor[G] and neighbor[OPEN]:
		#
		#		 neighbor[VALID] = False
		#
		#		 nodes[neighbor_pos] = neighbor = neighbor[:]
		#
		#		 neighbor[F] = neighbor_g + neighbor[H]
		#		 neighbor[ID] = ids.next()
		#		 neighbor[G] = neighbor_g
		#		 neighbor[VALID] = True
		#		 neighbor[PARENT] = current[POS]
		#
		#		 heappush(heap, neighbor)
		#
		# while heap and not heap[0][VALID]:
		#	 heappop(heap)
