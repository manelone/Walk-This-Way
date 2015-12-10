import edge_connects, math, random, collections, heapq, re, sys, time, os, random, datetime
from journey import Journey
from a_star_search import AStarSearch

class BaselineSearch(AStarSearch):

	def __init__(self):
		AStarSearch.__init__(self) # call super __init__ function
		#dictionary from edges to list of times of known crimes (crime type, time) at that edge
		self.knownCrimes = edge_connects.readKnownCrimes()

	def getStreetCost(self, street, newNode, end, startTime):
		#Heuristic: manhattan distance from currNode to endNode
		distance = math.sqrt((end[0] - newNode [0])*(end[0] - newNode [0]) + (end[1] - newNode [1])*(end[1] - newNode [1]))
		return street.st_length + street.numCrimes * street.st_length + (distance)

def main():

	search = BaselineSearch().getAlgorithm()

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



