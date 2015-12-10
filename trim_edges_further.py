import fileinput
from pandas import pandas as pd

filename = "trimmed_edges.csv"

edges = pd.read_csv(filename)

lines = tuple(open(filename, 'r'))

fout = open('sf_edges','w')

i = 0
line = lines[i]
fout.write(line)
for edge in edges.iterrows():
	i += 1
	e = edge[1]
	startCoords = eval(e['startCoords'])
	endCoords = eval(e['endCoords'])
	if startCoords[1] > -122.35 or startCoords[1] < -122.52: 
		continue
	if startCoords[0] > 37.835 or startCoords[0] < 37.7: # changing these numbers to be more refined to SF
		continue
	if endCoords[1] > -122.35 or endCoords[1] < -122.52:
		continue
	if endCoords[0] > 37.835 or endCoords[0] < 37.7:
		continue
	line = lines[i]
	fout.write(line)

fout.close()