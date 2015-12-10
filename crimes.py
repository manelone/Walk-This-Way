from pandas import pandas as pd
import collections, math, random

# # Read in the data file
# df = pd.read_csv("crimes.csv")

# # Show the list of unique crime categories
# print df['Category'].unique()

# Filter to a set of crimes
# crime_type_whitelist = [
#     'ROBBERY','SEX OFFENSES, FORCIBLE','DRUG/NARCOTIC',
#     'KIDNAPPING', 'SEX OFFENSES, NON FORCIBLE',
#     'ASSAULT'
# ]

# print crime_type_whitelist

# # Subset the data
# df_subset = df[df['Category'].isin(crime_type_whitelist)]

# # Export the Subset
# df_subset.to_csv("crimes_sub2.csv")


class CrimeStreet():
    def __init__(self, edgeID, start, end, length):
        self.edgeID = edgeID
        self.start = start
        self.end = end
        self.st_length = length
        self.crimes = collections.Counter()

    def addCrime(self, type):
    	self.crimes[type] += 1

    def distFromStreet(self, loc):
    	slope = (self.end[0]-self.start[0]) / (self.end[1]-self.start[1])
    	perp_slope = -1/slope
    	b = self.start[1] - slope*self.start[0]
    	b2 = loc[1] - perp_slope*loc[0]
    	dist_lat = (b2 + b) / (slope - perp_slope)
    	dist_long = dist_lat * slope + b
    	# print dist_lat, dist_long
    	dist = math.sqrt((dist_lat-loc[0])**2 + (dist_long-loc[1])**2)
    	return dist

street = CrimeStreet(1,(1.0,1.0),(2.0,2.0),math.sqrt(2))
print street.distFromStreet((2,1))


df = pd.read_csv("crimes_sub2.csv")
print df.columns

edges = pd.read_csv("edgeLocs.csv")

# prune the edges outside of the bounds 37.5-38.5N, -122.729 & -121.888
trimmed_edges = []
fail_count = [0 for _ in range(4)]
for edge in edges.iterrows():
    e = edge[1]
    start = eval(e['startCoords'])
    end = eval(e['endCoords'])
    if start[1] > -121.888 or start[1] < -122.729: 
        fail_count[0] += 1
        continue
    if start[0] > 38.5 or start[0] < 37.5: 
        fail_count[1] += 1
        continue
    if end[1] > -121.888 or end[1] < -122.729: 
        fail_count[2] += 1
        continue
    if end[0] > 38.5 or end[0] < 37.5: 
        fail_count[3] += 1
        continue
    trimmed_edges.append(e)
print fail_count
print len(trimmed_edges)
# print trimmed_edges

edgeIDs = pd.Series([edge['EdgeID'] for edge in trimmed_edges])
starts = pd.Series([edge['startCoords'] for edge in trimmed_edges])
ends = pd.Series([edge['endCoords'] for edge in trimmed_edges])
dists = pd.Series([edge['distance'] for edge in trimmed_edges])

trimmed_df = pd.concat([edgeIDs, starts, ends, dists], axis=1, keys=['EdgeID', 'startCoords', 'endCoords', 'distance'])
# trimmed_df = pd.concat(trimmed_edges, axis=0, keys = [edge['EdgeID'] for edge in trimmed_edges])
#print trimmed_df

trimmed_df.to_csv("trimmed_edges.csv")

# cats = df['Category']
# print type(cats).__name__
# print len(cats)

# for i, crime in df.iterrows():
	# find the minimum (distFromStreet, CrimeStreet) pair
	# add the crime to that street


