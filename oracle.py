import edge_connects, math, random, collections, heapq, re, sys, time, os, datetime
from journey import Journey
from a_star_search import AStarSearch



RISK_WEIGHT = 4
LENGTH_WEIGHT = 1


#returns true if any times in the given list of times fall within the range of 
#of the given time t
def inRange(t, times):
	start = t - datetime.timedelta(minutes=30)
	end = t + datetime.timedelta(minutes=60)
	for tm in times:
		if tm[1] >= start and tm[1] <= end:
			return True
	return False


class OracleSearch(AStarSearch):

	def __init__(self):
		AStarSearch.__init__(self) # call super __init__ function
		#dictionary from edges to list of times of known crimes (crime type, time) at that edge
		self.knownCrimes = edge_connects.readKnownCrimes()

	def getStreetCost(self, street, newNode, end, startTime):
		if street in self.knownCrimes and inRange(startTime, self.knownCrimes[street]):
			crimeScore = 100
		else:
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


