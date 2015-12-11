from a_star_search import AStarSearch
from ast import literal_eval as make_tuple
import edge_connects, datetime, time
from baseline import BaselineSearch
from oracle import OracleSearch
from standard import StandardSearch

def simulateJourney(journey):
	"""
	Given a journey, returns pair (tuple) (time, crimes)
	time is the time elapsed on the jouney
	crimes is an list of crimes the journey would encounter (same time, same place)
	"""
	crimes = []
	tm = journey.getStartTime()
	endTime = tm + datetime.timedelta(hours=1)
	for street in journey.getPath():
		# need to calculate the bounds of time that journier is on this street
		# time (defined outside of loop) currently equals the starting time
		# 

		#endTime = tm + street.length / walkingSpeed
		# loop through to check which crimes lie within the time bounds
		for crime in street.crimeList :
			ct = time.strptime(crime[1], "%A,%m/%d/%y,%H:%M")
			crimeTime = datetime.datetime.fromtimestamp(time.mktime(ct))
			if tm <= crimeTime and crimeTime <= endTime:
				crimes += crime
		# time = endTime

	return (0, crimes) # eventually first argument should be the distance traveled


def getJourneys(filename, algorithm):
	"""
	@param filename: name of text file with the following format (space separated) - one journey per line
	<lat> <long> <startTime>
	@param algorithm: should given, start and end node and time, returns a journey
	@return: list of journeys

	startTime should be time in same format as time in crime data
	"""
	journeys = []
	with open(filename) as f:
		lines = f.readlines()
	for line in lines:
		triple = line.split()
		sT = time.strptime(triple[2], "%A,%m/%d/%Y,%H:%M")
		startTime = datetime.datetime.fromtimestamp(time.mktime(sT))
		journey = algorithm(make_tuple(triple[0]), make_tuple(triple[1]), startTime)
		journeys.append(journey)
	return journeys



def simulate(journeys):
	"""
	Given an list of journeys, simulates each journey and prints statistics
	"""
	print "----------------Simulating journeys----------------"

	numJourneys = len(journeys)
	numSafeJouneys = 0
	totalDistance = 0
	totalCrimeScore = 0
	for journey in journeys :
		pair = simulateJourney(journey)
		totalDistance += pair[0]
		if len(pair[1]) == 0 : # no crime
			numSafeJouneys += 1
		totalCrimeScore += journey.getTotalCrimeScore()

	print "Number of journeys: " + str(numJourneys)
	print "Number of safe journeys: " + str(numSafeJouneys)
	print "Cumulative crime score: " + str(totalCrimeScore)
	print "---------------------------------------------------"

def main():	
	solver = StandardSearch()
	algorithm = solver.getAlgorithm()
	simulate(getJourneys("journeys.txt", algorithm))

if __name__ == '__main__':
	main()

