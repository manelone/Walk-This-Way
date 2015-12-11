from pandas import pandas as pd
import collections, math, random, sys, time, datetime
from copy import deepcopy
from street import CrimeStreet

#weights of different types of crimes
CRIME_TYPE_WEIGHTS = {'ROBBERY':5, 'SEX OFFENSES, FORCIBLE':6,'DRUG/NARCOTIC':2, 'KIDNAPPING':7, 'SEX OFFENSES, NON FORCIBLE':3, 'ASSAULT':9}

#number of regions to divide the city into for k-means clustering
NUM_REGIONS = 10

edges = pd.read_csv("trimmed_edges.csv")
#crimes = pd.read_csv("crimes_with_streets.csv")
crimes = pd.read_csv("mini_crimes_set.csv")
testCrimes = pd.read_csv("test_crime_data.csv")

#a dictionary from edgeIDs to CrimeStreetObjects
streets = {}

#a dictionary from crimeStreets to a list of known crimes read in from testCrimes (crime type, time)
knownCrimes = {}

def getDistance(a,b):
	return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**(.5)

def kmeans(crimes, K, maxIters):
	'''
    crimes: list of crime location and closest street pairs, ((lat, long), closestEdge)
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    maxIters: maximum number of iterations to run for (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments, (i.e. if crimes[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''

    #returns the index of the closest centroid to the given crime's location
	def closestCentroid (centroids, example):
		minDistance = sys.maxint
		closest = 0
		for i in range(K):
			dist = getDistance(centroids[i], example[0])
			if dist < minDistance:
				closest = i
				minDistance = dist
		return closest

	numCrimes = len(crimes)

    #initialize random centroids and assingment list
	#c = random.sample(crimes, K)
	c = [crimes[1],crimes[10],crimes[20],crimes[21],crimes[90],crimes[101],crimes[8],crimes[33],crimes[12],crimes[87] ]
	centroids = [0]*K
	for i in range(K):
		centroids[i] = deepcopy(c[i][0])
	assignments = [0] * numCrimes

    #run k-means clustering 
	for iteration in range(maxIters):
    	#keep track of original assignments
		oldAssignments = list(assignments)
    	
    	#update assignments
		for i in range(numCrimes):
			assignments[i] = closestCentroid(centroids, crimes[i])

    	#check for convergence
		if assignments == oldAssignments:
			break

    	#clear centroid values:
		for i in range(K):
			centroids [i] = (0,0)

    	#update centroids through addition:
		for j in range(numCrimes):
			oldValue = centroids[assignments[j]]
			newValue = (oldValue[0]+crimes[j][0][0], oldValue[1]+crimes[j][0][1])
			centroids[assignments[j]] = newValue

    	#update centroids through division
		for k in range(K):
			oldValue = centroids[k]
			newValue = oldValue
			if assignments.count(k) != 0:
				newValue = (oldValue[0]/(assignments.count(k)*1.0), oldValue[1]/(assignments.count(k)*1.0))
			centroids[k] = newValue

	return (centroids, assignments)


#establishes the crimeStreets (and populates the streets dictionary) by reading
#through the various data files
def estStreets():
	for edge in edges.iterrows():
	    e = edge[1]
	    curr = CrimeStreet(e['EdgeID'], eval(e['startCoords']), eval(e['endCoords']), float(e['distance']))
	    streets[e['EdgeID']] = curr
	print 'established streets as CrimeStreet vars'
	
	crimesList = []

	for i, crime in crimes.iterrows():
		e = crime['StreetMatch']
		timeString = crime['DayOfWeek']+ ',' + crime['Date']+ ',' +crime['Time']
		streets[e].addCrime((crime['Category'],timeString))
		crimesList.append((eval(crime['Location']),crime['Category']))
	
	print 'added crimes to streets and established crimesList for k-means clustering'

	hotspots, assignments = kmeans(crimesList, NUM_REGIONS, 10)
	
	print 'established 10 crime hotspot assignments using k-means clustering'
	
	hotspotCrimeScores = collections.Counter()
	for i in range(len(assignments)):
		hotspot = hotspots[assignments[i]]
		crime = crimesList[i][1]
		crimeLoc = crimesList[i][0]
		hotspotCrimeScores[hotspot] += (CRIME_TYPE_WEIGHTS[crime]/(getDistance(hotspot, crimeLoc)+1))

	for i in range(len(hotspots)):
		if assignments.count(i) > 0:
			hotspotCrimeScores[hotspots[i]] /= (assignments.count(i)*1.0)

	print 'updated hotspot scores'

	for edge in streets:
		streets[edge].setRegionScore(hotspotCrimeScores)
		streets[edge].getCrimeScore()

	print 'updated crimeRegionScore for each crimeStreet'

	#return streets


# returns map from node (intersection) to set of incident edges (street)
def nodeDict():
	node_dict = {}
	estStreets()
	for st in streets:
		edge = streets[st]
		startCoords = edge.start #eval(edge['startCoords'])
		endCoords = edge.end #eval(edge['endCoords'])
		if startCoords[1] > -122.35  or startCoords[1] < -122.52: 
			continue
		if startCoords[0] > 37.835 or startCoords[0] < 37.7:
			continue
		if endCoords[1] > -122.35  or endCoords[1] < -122.52:
			continue
		if endCoords[0] > 37.835 or endCoords[0] < 37.7:
			continue
		if startCoords not in node_dict:
			node_dict[startCoords] = set([edge])
		else:
			node_dict[startCoords].add(edge)
		if endCoords not in node_dict:
			node_dict[endCoords] = set([edge])
		else:
			node_dict[endCoords].add(edge)

	readKnownCrimes()
	return node_dict


#creates a dictionary from CrimeStreets to a list of crime type/datetimes tuples
#that represent crimes and the times they were committed on that street
#{CrimeStreet:(Type, Datetime)}
def readKnownCrimes():
	
	for i, crime in testCrimes.iterrows():
		e = crime['StreetMatch']
		timeString = crime['DayOfWeek']+ ',' + crime['Date']+ ',' +crime['Time']
		street = streets[e]
		if street not in knownCrimes.keys():
			knownCrimes[street] = []
		tm = time.strptime(timeString, "%A,%m/%d/%y,%H:%M")
		formattedTm = datetime.datetime.fromtimestamp(time.mktime(tm))
		knownCrimes[street].append((crime['Category'],formattedTm))

	print 'finished reading crime_test_data'
	#return knownCrimes


#edge_dict = nodeDict()
#knownCrimes = readKnownCrimes()
#print sum(1.0*len(edge_dict[node]) for node in edge_dict) / len(edge_dict.keys())

# streets = estStreets()
# for st in streets:
# 	print streets[st].crimes

