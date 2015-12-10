from pandas import pandas as pd
import collections, math, random

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

# street = CrimeStreet(1,(1.0,1.0),(2.0,2.0),math.sqrt(2))
# print street.distFromStreet((2,1))
# st1 = CrimeStreet(8889, (37.707062, -121.93736299999999), (37.707069, -121.928421), 0.008942)
# st2 = CrimeStreet(8834, (37.735077000000004, -122.400658), (37.727768, -122.40138999999999), 0.007346)
# print 'FOR STREET 8889'
# print st1.distFromStreet((37.7783276318163, -122.426642472038))
# print 'FOR STREET 8834'
# print st2.distFromStreet((37.7783276318163, -122.426642472038))

edges = pd.read_csv("trimmed_edges.csv")
print 'finished reading trimmed_edges.csv'

streets = {}
for edge in edges.iterrows():
    e = edge[1]
    curr = CrimeStreet(e['EdgeID'], eval(e['startCoords']), eval(e['endCoords']), float(e['distance']))
    streets[e['EdgeID']] = curr

crime_data = pd.read_csv("crimes_sub2.csv")
print 'finished reading crimes_sub2.csv'

# print "COLUMNS FOR NODES: ", crime_data.columns
print crime_data.axes

cats = crime_data['Category']
days = crime_data['DayOfWeek']
dates = crime_data['Date']
times = crime_data['Time']
locs = crime_data['Location']

# incNums = []
crime_to_st = []
crime_dist = []
for i, crime in crime_data.iterrows():
    #print crime[1]['Category']
    loc = eval(crime['Location'])
    # get the location of the crime (lat, long)
    st_of_crime = min([(streets[st].distFromStreet(loc), st) for st in streets])
    # min((CrimeStreet.dist(crime loc), CrimeStreet) for st in streets)
    streets[st_of_crime[1]].addCrime(crime['Category'])
    crime_to_st.append(st_of_crime[1])
    crime_dist.append(st_of_crime[0])
    # CS.addCrime(crime type)
    # print crime[1]['Category']
    # print crime
    # incNums.append(crime['IncidntNum'])


# starts = pd.Series([edge['startCoords'] for edge in trimmed_edges])
# ends = pd.Series([edge['endCoords'] for edge in trimmed_edges])
# dists = pd.Series([edge['distance'] for edge in trimmed_edges])
keys = ['Category', 'DayOfWeek', 'Date', 'Time', 'Location', 'StreetMatch', 'Distance']
crime_df = pd.concat([pd.Series(cats), pd.Series(days), pd.Series(dates), \
    pd.Series(times), pd.Series(locs), pd.Series(crime_to_st), pd.Series(crime_dist)], axis=1, keys=keys)
# crime_df.to_csv("crimes_with_streets.csv")

print 'finished matching crimes to streets'



