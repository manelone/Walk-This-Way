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

 	def printPath(self):
 		path = ""
 		if len(self.path) > 0:
 			p = self.path[0]
 			path += str(p.start) + ' '
 		for p in self.path:
 			path += str(p.edgeID) + ' to '
 		path += str(p.end)
 		print path
