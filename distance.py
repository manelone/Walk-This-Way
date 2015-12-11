LATCONV = 1.112 # this is number of KM per .01 degree latitude
LONGCONV = 0.8791 # this is number of KM per .01 degree longitude

def getDistance(latlong1, latlong2):
	'''
	@params: pairs (lat, long) where each coordinate is a float
	NOTE: Only accurate locally (in SF bay area)
	'''
	latDif = latlong1[0] - latlong2[0]
	longDif = latlong1[1] - latlong2[1]
	return ((latDif * 100 * LATCONV)**2 + (longDif * 100 * LONGCONV)**2)**(0.5)
