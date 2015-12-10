import edge_connects, math, random, collections, heapq, re, sys, time, os, datetime
from journey import Journey
from a_star_search import AStarSearch


RISK_WEIGHT = 4
LENGTH_WEIGHT = 1


class OracleSearch(AStarSearch):

	def __init__(self):
		AStarSearch.__init__(self) # call super __init__ function

	def getStreetCost(self, street, newNode, end, startTime):

		#returns true if any times in the given list of times fall within the range of 
		#of the given time t
		distance = math.sqrt((end[0] - newNode [0])*(end[0] - newNode [0]) + (end[1] - newNode [1])*(end[1] - newNode [1]))
		if street.knownCrimeScore(startTime) != 0:
			risk = 10**12
		else:
			risk = 1

		cost = (risk)*street.st_length**LENGTH_WEIGHT + distance**LENGTH_WEIGHT
		print ('edge: ' + str(street.edgeID) + ' cost: ' + str(cost))
		return cost

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



