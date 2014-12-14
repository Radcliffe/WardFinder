import json
import urllib
import urllib2

address="1600+Amphitheatre+Parkway,+Mountain+View,+CA"
geocode_url="https://maps.googleapis.com/maps/api/geocode/json?address=%s"

response = urllib2.urlopen(url)
jsongeocode = response.read()


FILENAME = "City_Council_Wards.json"

def load_polygons(filename=FILENAME):
    polygons = {}
    with open(filename, "rt") as f:
        jsdata = '\n'.join(f.readlines())
        wards = json.loads(jsdata)
        for feature in wards['features']:
            ward = feature["properties"]["BDNUM"]
            coordinates = feature["geometry"]["coordinates"][0]
            polygons[ward] = coordinates
    return polygons


def point_in_polygon(x, y, poly):
    p = [(x1 - x, y1 - y) for x1, y1 in poly] 
    x2, y2 = p[0]
    crossings = 0
    for i in xrange(1, len(p)):
        x1, y1 = x2, y2
        x2, y2 = p[i]
        s = sgn(y1)
        if s != sgn(y2) and (x1>=0 or x2>=0) and sgn(x2*y1-x1*y2) == s:
            crossings += s
    return abs(crossings) == 1


def get_ward(street, polygons):
    location = geolocator.geocode(street + ", Minneapolis, MN")
    if location:
        x, y = location.longitude, location.latitude
        for ward, poly in polygons.iteritems():
            if point_in_polygon(x, y, poly):
                return str(x) + "," + str(y) + "," + ward
        return str(x) + "," + str(y) + ",NA"
    return "NA,NA,NA"
            
def geocode(address):
    querystring = urllib.urlencode({'address' : address})
    url = "https://maps.googleapis.com/maps/api/geocode/json?" + querystring
    response = urllib2.urlopen(url)
    jsongeocode = json.loads(response.read())
    location = geodata['results'][0]['geometry']['location']
    x = location['lng']
    y = location['lat']

def sgn(x):
    if x < 0:
        return -1
    return 1

       
if __name__ == "__main__":
    polygons = load_polygons()
    with open("training.csv", "rt") as f:
        for line in f.readlines():
            addr, actual = line.strip().split(',')
            predicted = get_ward(addr, polygons)
            print (addr, actual, predicted)     
