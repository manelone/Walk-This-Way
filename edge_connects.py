from pandas import pandas as pd
import collections, math, random, sys
from copy import deepcopy

#weights of different types of crimes
CRIME_TYPE_WEIGHTS = {'ROBBERY':5, 'SEX OFFENSES, FORCIBLE':6,'DRUG/NARCOTIC':2, 'KIDNAPPING':7, 'SEX OFFENSES, NON FORCIBLE':3, 'ASSAULT':9}

#number of regions to divide the city into for k-means clustering
NUM_REGIONS = 10

edges = pd.read_csv("trimmed_edges.csv")
crimes = pd.read_csv("crimes_with_streets.csv")

def getDistance(a,b):
	return (a[0] - b[0])*(a[0] - b[0]) + (a[1] - b[1])*(a[1] - b[1])

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
	c = random.sample(crimes, K)
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


class CrimeStreet():
    def __init__(self, edgeID, start, end, length):
        self.edgeID = edgeID
        self.start = start
        self.end = end
        self.st_length = length
       	self.crimes = collections.Counter()
       	self.crimeList = []
       	self.regionCrimeScore = 0

    #regionScore is avg of crime score of hotspot / distance of street from hotspot over all hotspots
    #weighted by the distance to that hotspot
    #regionCrimeScores is a dictionary of locations to their scores
    def setRegionScore(self, regionCrimeScores):
    	regionCrimeScore = 0
    	for centroid in regionCrimeScores.keys():
    		dist = self.distFromStreet(centroid)
    		regionCrimeScore += regionCrimeScores[centroid]/dist
		self.regionCrimeScore = regionCrimeScore/NUM_REGIONS

    def getCrimeRegionScore(self):
    	return self.regionCrimeScore

    def getCrimeScore(self):
		if len(self.crimes) == 0: return 0
		return sum(self.crimes[c] for c in self.crimes)

    def addCrime(self, crimeOccurence):
    	#self.crimes[crimeOccurence[0]] += 1
    	self.crimes[crimeOccurence[0]] += CRIME_TYPE_WEIGHTS[crimeOccurence[0]]
    	self.crimeList.append(crimeOccurence)

    def distFromStreet(self, loc):
    	slope = (self.end[1]-self.start[1]) / (self.end[0]-self.start[0])
    	perp_slope = -1/slope
        #print slope, perp_slope
    	b = self.start[1] - slope*self.start[0]
    	b2 = loc[1] - perp_slope*loc[0]
        #print b, b2
    	dist_lat = (b2 + b) / (slope - perp_slope)
    	dist_long = dist_lat * slope + b
        if dist_lat < min([self.start[0], self.end[0]]) or \
            dist_lat > max([self.start[0], self.end[0]]) or \
            dist_long < min([self.start[1], self.end[1]])or \
            dist_long > max([self.start[1], self.end[1]]): 
            return min([math.sqrt((self.end[0]-loc[0])**2 + (self.end[1]-loc[1])**2), \
                math.sqrt((self.start[0]-loc[0])**2 + (self.start[1]-loc[1])**2)])
        #print dist_lat, dist_long
    	dist = math.sqrt((dist_lat-loc[0])**2 + (dist_long-loc[1])**2)
    	return dist


def estStreets():
	streets = {}
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

	print 'updated crimeRegionScore for each crimeStreet'

	return streets

def nodeDict():
	edge_dict = {}
	streets = estStreets()
	for st in streets:
		edge = streets[st]
		startCoords = edge.start #eval(edge['startCoords'])
		endCoords = edge.end #eval(edge['endCoords'])
		if startCoords[1] > -121.888 or startCoords[1] < -122.729: 
			continue
		if startCoords[0] > 38.5 or startCoords[0] < 37.5:
			continue
		if endCoords[1] > -121.888 or endCoords[1] < -122.729:
			continue
		if endCoords[0] > 38.5 or endCoords[0] < 37.5:
			continue
		if startCoords not in edge_dict:
			edge_dict[startCoords] = set([edge])
		else:
			edge_dict[startCoords].add(edge)
		if endCoords not in edge_dict:
			edge_dict[endCoords] = set([edge])
		else:
			edge_dict[endCoords].add(edge)
	return edge_dict

#edge_dict = nodeDict()
#print sum(1.0*len(edge_dict[node]) for node in edge_dict) / len(edge_dict.keys())

# streets = estStreets()
# for st in streets:
# 	print streets[st].crimes

