import edge_connects, math, random, collections, heapq, re, sys, time, os, datetime
from journey import Journey
from a_star_search import AStarSearch



<<<<<<< HEAD
=======
nodeDict = edge_connects.nodeDict()

#dictionary from crimeStreets to list of times of known crimes (crime type, time) at that edge
#knownCrimes = edge_connects.readKnownCrimes()

>>>>>>> 08f60ddf70c7c095a79254bd5005440dccbc1618
RISK_WEIGHT = 4
LENGTH_WEIGHT = 1


#returns true if any times in the given list of times fall within the range of 
#of the given time t
# def inRange(t, times):
# 	start = t - datetime.timedelta(minutes=30)
# 	end = t + datetime.timedelta(minutes=60)
# 	for tm in times:
# 		if tm[1] >= start and tm[1] <= end:
# 			return True
# 	return False

<<<<<<< HEAD
=======
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
 			numCrimes += street.numCrimes
 		return numCrimes

 	def getTotalCrimeScore(self):
 		crimeScore = 0
 		for street in self.path:
 			crimeScore += street.getCrimeScore()
 		return crimeScore
 	
 	def getKnownCrimeScore(self):
 		crimeScore = 0
 		for street in self.path:
 			crimeScore += street.knownCrimeScore(self.startTime)
 		return crimeScore

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
>>>>>>> 08f60ddf70c7c095a79254bd5005440dccbc1618

class OracleSearch(AStarSearch):

	def __init__(self):
		AStarSearch.__init__(self) # call super __init__ function
		#dictionary from edges to list of times of known crimes (crime type, time) at that edge
		self.knownCrimes = edge_connects.readKnownCrimes()

	def getStreetCost(self, street, newNode, end, startTime):
		if street in self.knownCrimes and inRange(startTime, self.knownCrimes[street]):
			crimeScore = 100
		else:
<<<<<<< HEAD
			crimeScore = 0
		distance = math.sqrt((end[0] - newNode [0])*(end[0] - newNode [0]) + (end[1] - newNode [1])*(end[1] - newNode [1]))
		print ('edge: ' + str(street.edgeID) + ' score: ' + str(crimeScore))
		return math.e**(crimeScore * RISK_WEIGHT)*street.st_length**LENGTH_WEIGHT + distance**LENGTH_WEIGHT

def main():

	search = OracleSearch().getAlgorithm()

	startTime = time.strptime('Friday,10/16/2015,22:00', "%A,%m/%d/%Y,%H:%M")
	formattedStartTime = datetime.datetime.fromtimestamp(time.mktime(startTime))
	journey = search((37.796028, -122.44310800000001),(37.781566999999995, -122.41133899999998), formattedStartTime)
	print ('here\'s our path')
	journey.printPath()
	# print(journey.path)
	print('length: '+ str(journey.getLength()))
	print('total crimes: '+ str(journey.getNumCrimes()))
	print('total crime score: '+ str(journey.getTotalCrimeScore()))

if __name__ == '__main__':
	main()
=======

			for street in nodeDict[node]:
				if node == street.start:
					newNode = street.end
				else:
					newNode = street.start
				#Heuristic: manhattan distance from currNode to endNode
				distance = math.sqrt((end[0] - newNode [0])*(end[0] - newNode [0]) + (end[1] - newNode [1])*(end[1] - newNode [1]))
				
				if street.knownCrimeScore(startTime) != 0:
					risk = 10**12
				else:
					risk = 1

				
				cost = (risk)*street.st_length**LENGTH_WEIGHT + distance**LENGTH_WEIGHT
				#cost = risk
				print ('edge: ' + str(street.edgeID) + ' cost: ' + str(cost))
				if pq.update(newNode, cost):
					parentage[newNode] = street
	
				visitedNodes.append(node)
	return None


startTime = time.strptime('Friday,10/31/2014,23:30', "%A,%m/%d/%Y,%H:%M")
formattedStartTime = datetime.datetime.fromtimestamp(time.mktime(startTime))
journey = aStarSearch((37.796028, -122.44310800000001),(37.781566999999995, -122.41133899999998), formattedStartTime)
print ('here\'s our path')
journey.printPath()
# print(journey.path)
print('length: '+ str(journey.getLength()))
print('total crimes: '+ str(journey.getNumCrimes()))
print('total crime score: '+ str(journey.getKnownCrimeScore()))
>>>>>>> 08f60ddf70c7c095a79254bd5005440dccbc1618


