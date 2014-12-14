GEOCODE = False # Must be set to False when deploying to Google App Engine
                # Must be set to True when testing locally
import json

FILENAME = "City_Council_Wards.json"

def load_polygons(filename=FILENAME):
    polygons = {}
    with open(filename) as f:
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


def get_ward_by_lng_lat(lng, lat, polygons):
    for ward, poly in polygons.iteritems():
        if point_in_polygon(lng, lat, poly):
            return ward
    return 'NA'

if GEOCODE:
    import geocoder
    def get_ward(street, polygons):
        g = geocoder.google(street + ", MINNEAPOLIS MN")
        if g:
            lat, lng = g.latlng
            ward = get_ward_by_lng_lat(lng, lat, polygons)
            return str(lng) + "," + str(lat) + "," + ward
        return "NA,NA,NA"
            
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
