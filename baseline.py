import edge_connects, math, random, collections, re, sys, time, os, random, datetime
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
