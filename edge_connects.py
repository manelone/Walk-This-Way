from pandas import pandas as pd
import collections, math, random, sys
from copy import deepcopy


ROBBERY = 5
SEX OFFENSES, FORCIBLE = 6
DRUG/NARCOTIC = 2
KIDNAPPING = 7
SEX OFFENSES, NON FORCIBLE = 3
ASSAULT = 9


edges = pd.read_csv("trimmed_edges.csv")
crimes = pd.read_csv("crimes_with_streets.csv")



def kmeans(crimes, K, maxIters):
	'''
    crimes: list of crime location and closest street pairs, ((lat, long), closestEdge)
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    maxIters: maximum number of iterations to run for (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments, (i.e. if crimes[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''

    #returns manhattan distance between two points (a, b) and (x, y)
	def getDistance(a, b):
		return (a[0] - b[0])*(a[0] - b[0]) + (a[1] - b[1])*(a[1] - b[1])

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
   		
	reconstructionLoss = 0
	for i in range(numCrimes):
	    reconstructionLoss += getDistance(crimes[i][0], centroids[assignments[i]])

	return (centroids, assignments, reconstructionLoss)


class CrimeStreet():
    def __init__(self, edgeID, start, end, length):
        self.edgeID = edgeID
        self.start = start
        self.end = end
        self.st_length = length
       	self.crimes = collections.Counter()
       	self.crimeList = []
       	self.regionCrimeScore = 0

    #region score is crime score of nearest crime hotspot weighted by the distance to that hotspot
    #region crimeScores is a dictionary of locations to their scores
    def setRegionScore(self, regionCrimeScores):
    	#find closest centroid
		minDistance = sys.maxint
		closest = 0
		for centroid in regionCrimesScores.keys():
			dist = self.distanceFromStreet(centroid)
			if dist < minDistance:
				closest = centroid
				minDistance = dist
		#TO-DO: properly weight regionCrimeScore against distance from region
		regionCrimeScore = regionCrimeScores[closest] / minDistance 
		self.regionCrimeScore = regionCrimeScore

    def getCrimeRegionScore(self):
    	return self.regionCrimeScore

	def getCrimeScore(self):
		if len(self.crimes) == 0: return 0
		return sum(self.crimes[c] for c in self.crimes)

    def addCrime(self, crimeOccurence):
    	self.crimes[crimeOccurence[0]] += 1
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
	
	print len(streets)

	crimesList = []

	for i, crime in crimes.iterrows():
		e = crime['StreetMatch']
		streets[e].addCrime((crime['Category'],crime['Time']))

		crimesList.append((eval(crime['Location']),e))
	print 'added crimes to streets and established crimesList for k-means clustering'
	print len(crimesList)

	hotspots, assignments, reconstructionLoss = kmeans(crimesList, 10, 10)
	print 'established 10 crime hotspot assignments using k-means clustering'
	
	#TO-DO: write the function below
	#regionCrimeScores = establishRegionCrimeScore(assingments)
		#something along the lines of sum of weighted crimes / number of of crimes in cluster

	for edge in streets:
		streets[edge].setRegionScore(regionCrimeScores)

	return streets

def nodeDict():
	# stEdges = pd.read_csv("cal.cedge.csv")
	# stNodes = pd.read_csv("cal.cnode.csv")

	# nodes = stNodes.as_matrix()
	edge_dict = {}
	streets = estStreets()
	# for i, edge in edges.iterrows():
	for st in streets:
		edge = streets[st]
		# start = int(edge['startID'])
		# end = int(edge['endID'])
		# startCoords = (float(nodes[start][2]), float(nodes[start][1]))
		# endCoords = (float(nodes[end][2]), float(nodes[end][1]))
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
		#edgeSt = CrimeStreet(edge['EdgeID'], eval(edge['startCoords']), eval(edge['endCoords']), float(edge['distance']))
		if startCoords not in edge_dict:
			edge_dict[startCoords] = set([edge])
		else:
			edge_dict[startCoords].add(edge)
		if endCoords not in edge_dict:
			edge_dict[endCoords] = set([edge])
		else:
			edge_dict[endCoords].add(edge)
	return edge_dict

edge_dict = nodeDict()
#print sum(1.0*len(edge_dict[node]) for node in edge_dict) / len(edge_dict.keys())

# streets = estStreets()
# for st in streets:
# 	print streets[st].crimes

