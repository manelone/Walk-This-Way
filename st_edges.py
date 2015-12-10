from pandas import pandas as pd

stEdges = pd.read_csv("cal.cedge.csv")
stNodes = pd.read_csv("cal.cnode.csv")

print "COLUMNS FOR EDGES: ", stEdges.columns
print "COLUMNS FOR NODES: ", stNodes.columns

startCoords = []
endCoords = []

nodes = stNodes.as_matrix()

for i, edge in stEdges.iterrows():
	# print edge
	# print edge['startID'], edge['endID']
	start = int(edge['startID'])
	end = int(edge['endID'])

	startCoords.append((float(nodes[start][2]), float(nodes[start][1])))
	endCoords.append((float(nodes[end][2]), float(nodes[end][1])))
	#print edge['NodeID']
	# which st['NodeID'] == startID

startCoords = pd.Series(startCoords, name='startCoords')
endCoords = pd.Series(endCoords, name='endCoords')
#print startCoords

df = pd.concat([stEdges['EdgeID'], startCoords, endCoords, stEdges['distance']], axis=1)
# print df

df.to_csv("edgeLocs.csv")