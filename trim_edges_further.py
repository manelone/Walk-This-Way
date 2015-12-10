import fileinput
from pandas import pandas as pd

filename = "trimmed_edges.csv"

edges = pd.read_csv(filename)

i = 0
for line in fileinput.input(filename, inplace=True):
	e = edges[i][1]
	startCoords = eval(e['startCoords'])
	endCoords = eval(e['endCoords'])
	i += 1
	if startCoords[1] > -122.35 or startCoords[1] < -122.52: 
		continue
	if startCoords[0] > 37.835 or startCoords[0] < 37.7: # changing these numbers to be more refined to SF
		continue
	if endCoords[1] > -122.35 or endCoords[1] < -122.52:
		continue
	if endCoords[0] > 37.835 or endCoords[0] < 37.7:
		continue
	print line,