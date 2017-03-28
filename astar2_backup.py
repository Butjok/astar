# Copyright (c) 2008 Mikael Lind
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from heapq import heappush, heappop
from sys import maxint
import grid as g


# Represent each node as a list, ordering the elements so that a heap of nodes
# is ordered by f = g + h, with h as a first, greedy tie-breaker and num as a
# second, definite tie-breaker. Store the redundant g for fast and accurate
# calculations.

F, H, NUM, G, POS, OPEN, VALID, PARENT = xrange(8)
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

	def make_node(g, pos, parent_pos):
		return [g + heuristic(pos, goal), heuristic(pos, goal), nums.next(), g, pos, True, True, parent_pos]

	def neighbors(pos):
		return g.neighbours(grid, pos)

	def cost(pos):
		return grid[pos[Y]][pos[X]]

	# Create the start node.
	nums = iter(xrange(maxint))
	start = make_node(0, start_pos, None)

	# Track all nodes seen so far.
	nodes = {start_pos: start}

	# Maintain a heap of nodes.
	heap = [(start[F], start)]

	while heap:

		# Pop the next node from the heap.
		f, current = heappop(heap)
		current[OPEN] = False

		# Have we reached the goal?
		if goal == current[POS]:
			print(nodes[current[POS]][G])

			# Return the best path as a list.
			path = []
			while current[PARENT] is not None:
				path.append(current[POS])
				current = nodes[current[PARENT]]
			path.reverse()
			return path

		# Visit the neighbors of the current node.
		for neighbor_pos in neighbors(current[POS]):
			neighbor_g = current[G] + cost(neighbor_pos)
			neighbor = nodes.get(neighbor_pos)

			if neighbor is None or (neighbor[OPEN] and neighbor_g < neighbor[G]):
				if neighbor and neighbor_g < neighbor[G] and neighbor[OPEN]:
					neighbor[VALID] = False
				nodes[neighbor_pos] = neighbor = make_node(neighbor_g, neighbor_pos, current[POS])
				heappush(heap, (neighbor[F], neighbor))

		# Discard leading invalid nodes from the heap.
		while heap and not heap[0][1][VALID]:
			heappop(heap)


	return []