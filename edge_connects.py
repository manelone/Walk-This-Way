from pandas import pandas as pd
import collections, math, random

edges = pd.read_csv("trimmed_edges.csv")
crimes = pd.read_csv("crimes_with_streets.csv")


class CrimeStreet():
    def __init__(self, edgeID, start, end, length):
        self.edgeID = edgeID
        self.start = start
        self.end = end
        self.st_length = length
        self.crimes = collections.Counter()

    def getCrimeScore(self):
        if len(self.crimes) == 0: return 0
        return sum(self.crimes[c] for c in self.crimes)

    def addCrime(self, type):
    	self.crimes[type] += 1

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
	for i, crime in crimes.iterrows():
		e = crime['StreetMatch']
		streets[e].addCrime(crime['Category'])
	print 'added crimes to streets'
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
print sum(1.0*len(edge_dict[node]) for node in edge_dict) / len(edge_dict.keys())

# streets = estStreets()
# for st in streets:
# 	print streets[st].crimes

