import edge_connects, math, random, collections, heapq, re, sys, time, os, random

# streetSet = edge_connects.estStreets()
nodeDict = edge_connects.nodeDict()


class Journey():
	def __init__(self, path, startTime) :
		self.path = path # list of CrimeStreet objects
		self.startTime = startTime # time of the beginning of the journey 

	def getPath(self) :
		return self.path

	def getStartTime(self) :
		return self.startTime

	def getLength(self):
		length = 0
		for street in self.path:
			length += street.st_length
		return length


 	def getNumCrimes(self):
 		numCrimes = 0
 		for street in self.path:
 			numCrimes += street.getCrimeScore()
 		return numCrimes

 	def printPath(self):
 		path = ""
 		if len(self.path) > 0:
 			p = self.path[0]
 			path += str(p.start) + ' '
 		for p in self.path:
 			path += str(p.edgeID) + ' to '
 		path += str(p.end)
 		print path


#From CS221 starter code 
#Data structure for supporting A* search.
class PriorityQueue:
    def  __init__(self):
        self.DONE = -100000
        self.heap = []
        self.priorities = {}  # Map from state to priority

    # Insert |state| into the heap with priority |newPriority| if
    # |state| isn't in the heap or |newPriority| is smaller than the existing
    # priority.
    # Return whether the priority queue was updated.
    def update(self, state, newPriority):
        oldPriority = self.priorities.get(state)
        if oldPriority == None or newPriority < oldPriority:
            self.priorities[state] = newPriority
            heapq.heappush(self.heap, (newPriority, state))
            return True
        return False

    # Returns (state with minimum priority, priority)
    # or (None, None) if the priority queue is empty.
    def removeMin(self):
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.DONE: continue  # Outdated priority, skip
            self.priorities[state] = self.DONE
            return (state, priority)
        return (None, None) # Nothing left...







def aStarSearch(start, end, startTime):
	"""
	@param start: (lat, long) coordinates of starting location
	@param end: (lat, long) coordinates of ending location
	@param startTime: the start time of the journey
	
	@return: the quickest and safest possible journey that get you from start to end

	startTime should be time in same format as time in crime data
	"""

	def createPath(start, end):
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

			return createPath(start, end)
		#keep exploring
		else:

			for street in nodeDict[node]:
				if node == street.start:
					newNode = street.end
				else:
					newNode = street.start
				#Heuristic: manhattan distance from currNode to endNode
				distance = (end[0] - newNode [0])*(end[0] - newNode [0]) + (end[1] - newNode [1])*(end[1] - newNode [1])
				cost = street.st_length + street.getCrimeScore() * street.st_length + (distance)

				#print street.getCrimeScore()
				if pq.update(newNode, cost):
					parentage[newNode] = street
	
				visitedNodes.append(node)
	return None



journey = aStarSearch((37.796028, -122.44310800000001),(37.781566999999995, -122.41133899999998), 0)
print ('here\'s our path')
journey.printPath()
# print(journey.path)
print('length: '+ str(journey.getLength()))
print('total crimes: '+ str(journey.getNumCrimes()))


