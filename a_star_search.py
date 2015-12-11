import edge_connects, math, random, collections, heapq, re, sys, time, os, random
from priority_queue import PriorityQueue
from journey import Journey

class AStarSearch():


	def __init__(self):
		self.nodeDict = edge_connects.nodeDict()

	def createPath(self, start, end, parentage, startTime):
		currPath = []
		currNode = end
		while (currNode != start):
			street = parentage[currNode]
			currPath.insert(0, street)
			if currNode == street.start:
				currNode = street.end
			else:
				currNode = street.start
		return Journey(currPath, startTime)

		#self.createPath = createPath

	#Heuristic: manhattan distance from currNode to endNode
	def getStreetCost(self, street, newNode, end, startTime):
		distance = math.sqrt((end[0] - newNode [0])*(end[0] - newNode [0]) + (end[1] - newNode [1])*(end[1] - newNode [1]))
		return street.st_length + (distance)

	"""
	@param start: (lat, long) coordinates of starting location
	@param end: (lat, long) coordinates of ending location
	@param startTime: the start time of the journey
	
	@return: the quickest and safest possible journey that get you from start to end

	startTime should be time in same format as time in crime data
	"""
	def algorithm(self, start, end, startTime): 
		visitedNodes = []
		pq = PriorityQueue()
		pq.update(start, 0)
		parentage = {}

		while (True):
			node = pq.removeMin()[0]
			#if we've searched the entire tree
			if node == None:
				break
			#if we've found a cycle
			if node in visitedNodes:
				continue
			#if we've found a solution, return a Journey containing that path
			elif node == end:

				return self.createPath(start, end, parentage, startTime)
			#keep exploring
			else:

				for street in self.nodeDict[node]:
					if node == street.start:
						newNode = street.end
					else:
						newNode = street.start
					
					cost = self.getStreetCost(street, newNode, end, startTime)

					#print street.getCrimeScore()
					if pq.update(newNode, cost):
						parentage[newNode] = street
		
					visitedNodes.append(node)
		return None


	def getAlgorithm(self):
		return self.algorithm



