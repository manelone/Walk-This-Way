import collections, math, datetime, time
from distance import getDistance

#weights of different types of crimes
CRIME_TYPE_WEIGHTS = {'ROBBERY':5, 'SEX OFFENSES, FORCIBLE':6,'DRUG/NARCOTIC':2, 'KIDNAPPING':7, 'SEX OFFENSES, NON FORCIBLE':3, 'ASSAULT':9}

#number of regions to divide the city into for k-means clustering
NUM_REGIONS = 10

class CrimeStreet():
    def __init__(self, edgeID, start, end):
        self.edgeID = edgeID
        self.start = start
        self.end = end
        self.st_length = getDistance(start, end)
       	self.crimes = collections.Counter()
       	self.crimeList = []
       	self.regionCrimeScore = 0
       	self.numCrimes = 0

    #regionScore is avg of crime score of hotspot / distance of street from hotspot over all hotspots^2
    #weighted by the distance to that hotspot
    #regionCrimeScores is a dictionary of locations to their scores
    def setRegionScore(self, regionCrimeScores):
    	regionCrimeScore = 0
    	for centroid in regionCrimeScores.keys():
    		dist = self.distFromStreet(centroid)
    		regionCrimeScore += regionCrimeScores[centroid]/(dist)
		self.regionCrimeScore = regionCrimeScore*1.0/(NUM_REGIONS**2)

    
	#getTimedCrimeScore returns the sum of the regional crimes score as well as the weighted crimes
	#that occur during a given time period surrounding the startTime
    def getTimedCrimeScore(self, startTime):

        def inRange(start, end, timeString):
            t = time.strptime(timeString, "%A,%m/%d/%y,%H:%M")
            formattedTime = datetime.datetime.fromtimestamp(time.mktime(t))
            if formattedTime >= start and formattedTime <= end:
                return True
            return False
            
    	crimeScore = 0
    	for i in range(2003,2014):
    		diff = startTime.year - i
    		numWeeks = diff * 72
    		standardStartTime = startTime - datetime.timedelta(weeks=numWeeks)
    		start = standardStartTime - datetime.timedelta(minutes=30)
    		end = standardStartTime + datetime.timedelta(minutes=60)
    		crimeScore = 0
    		for crime in self.crimeList:
    			if inRange(start, end, crime[1]):
    				crimeScore += CRIME_TYPE_WEIGHTS[crime[0]]
    	crimeScore /= 1.0*11
    	return crimeScore + self.regionCrimeScore

    def knownCrimeScore(self, startTime):
    	crimeScore = 0
    	if self in knownCrimes.keys():
    		crimes = knownCrimes[self]
    		start = startTime - datetime.timedelta(minutes=30)
    		end = startTime + datetime.timedelta(minutes=60)
    		for crime in crimes:
    			crimeType = crime[0]
    			crimeTime = crime[1]
    			if crimeTime>=start and crimeTime <=end:
    				print crime
    				crimeScore += CRIME_TYPE_WEIGHTS[crimeType]
    	return crimeScore


    #returns regional crime score
    def getregionCrimeScore(self):
    	return self.regionCrimeScore

    #returns the sum of the regional crime score and the sum of all crimes (weigthed by type) that have
    #ever occured on that street
    def getCrimeScore(self):
		if self.numCrimes == 0: return 0
		self.streetCrimeScore = sum(self.crimes[c] for c in self.crimes)
		#print('self: ' + str(self.streetCrimeScore) + ' region: '+str(self.regionCrimeScore))
		return self.streetCrimeScore + self.regionCrimeScore

    
	#adds a given crime to the crimes counter, the crimes list, and increments the total
	#number of crimes seen on this street
    def addCrime(self, crimeOccurence):
    	self.numCrimes += 1
    	self.crimes[crimeOccurence[0]] += CRIME_TYPE_WEIGHTS[crimeOccurence[0]]
    	self.crimeList.append(crimeOccurence)

    #calculates the distance from a given location to the street
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
