import requests
import xml.etree.ElementTree as ET

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
"http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=predictionsForMultiStops&s=wknd2&s=routeTag|dirTag|stopId"
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
    for route in routes:
        print(route.attrib['tag'])
except Exception as e:
	print("Issue getting route configuration:")
	raise(e)

route_tags = ['a','b','c','ee','f','lx','rexb','rexb', 'rexl', 'wknd1', 'wknd2', 'w1', 'w2']
stop_ids = {}
for route in routes:
	if route.attrib['tag'] in route_tags:
		print(route.attrib['tag'])
		for c in route:
		# Accounts for stops that may have more than one stopId
			if c.tag == 'stop':
				if not c.attrib['title'] in stop_ids:
					stop_ids[c.attrib['title']] = []
				if c.attrib['stopId'] not in stop_ids[c.attrib['title']]:
					stop_ids[c.attrib['title']].append(c.attrib['stopId'])
print(stop_ids)				

r = requests.get("http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=predictions&r=a&stopId=1055")		
print(r.text)
					
	

	

