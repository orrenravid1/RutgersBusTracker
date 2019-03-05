import requests
import xml.etree.ElementTree as ET
import datetime

'''
How to get nextbus info:
1. All commands start with:
"http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command="
2. To get all routes and stops:
"http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=routeConfig"
3. To get a prediction for a particular route and stop where <route> is the
route name and <stop> is the stop name:
"http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=predictions&r=<route>&s=<stop>"
3. cont. Alternatively, you can use stopId instead:
"http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=predictions&r=<route>&stopId=<stopId>"
3. cont. Optionally, you can add d=<dir> where <dir> is the direction
"http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=predictions&r=wknd2&s=quads&d=<dir>"
3. If instead you have a situation where there are multiple stops to be
predicted or the same stop has multiple stopIDs as is the case for Hill Center,
you can do this with predictionsForMultiStops. (dirTag can be null)
"http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=predictionsForMultiStops&stops=<routeTag1>|<dirTag1>|<stop1>&stops=<routeTag1>|<dirTag1>|<stop2>&etc..."
'''
'''
All route tags:
a : A
b : B
c : C
ee : EE
f : F
h : H
lx : LX
rexb : REXB
rexl : REXL
wknd1 : Weekend 1
wknd2 : Weekend 2
w1 : New Brunsquick 1 Shuttle
w2 : New Brunsquick 2 Shuttle
'''

r = requests.get("http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=routeConfig")
# Gets all route tags
try:
    root = ET.fromstring(r.text)
    routes = root.findall('route')
except Exception as e:
	print("Issue getting route configuration:")
	raise(e)


route_tags = ['a','b','c','ee','f','lx','rexb','rexb', 'rexl', 'wknd1', 'wknd2', 'w1', 'w2']
stop_ids = {}
route_root = ET.Element("routes")
for route in routes:
	if route.attrib['tag'] in route_tags:
		elements_to_remove = []
		for c in route:
			if not c.tag == 'stop':
				elements_to_remove.append(c)
		for e in elements_to_remove:
			route.remove(e)
		route_root.append(route)

route_predictions_root = ET.Element("route_predictions")
for route in route_root:
	request_string = "http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=predictionsForMultiStops"
	for stop in route:
			request_string += "&stops=" + route.attrib['tag'] + "|" + stop.attrib['tag']
	request = requests.get(request_string)
	predictions = ET.fromstring(request.text)
	currtime = datetime.datetime.now()
	for c in predictions:
		if c.tag == "Error":
			raise Exception("Request returned error: " + c.text)
	route_prediction = ET.Element("route_prediction")
	route_prediction.attrib["route"] = route.attrib["title"]
	route_prediction.attrib["time"] = str(currtime)
	for c in predictions:
		route_prediction.append(c)
	route_predictions_root.append(route_prediction)
	
tree = ET.ElementTree(route_predictions_root)
tree.write("route_predictions.xml")

	

