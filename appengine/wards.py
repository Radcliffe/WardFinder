PROPERTY_SEARCH = True
MEMCACHE = True

import urllib
import urllib2
import re
from google.appengine.api import memcache
if PROPERTY_SEARCH:
    import property

URL = "http://apps.ci.minneapolis.mn.us/AddressPortalApp/Search/SearchPOST?AppID=WardFinderApp"

pattern = re.compile(r"/ward([0-9]+)/")

# Look up the ward for a Minneapolis street address.

def get_ward(street_address):
    street_address = normalize(street_address)
    if MEMCACHE:
        ward = memcache.get(street_address)
        if ward is not None:
            return ward
    
    values = {'Address': street_address}
    data = urllib.urlencode(values)
    ward = 'NA'
    req = urllib2.Request(URL, data)
    
    try:    
        response = urllib2.urlopen(req)
        url = response.geturl()     
    except:
        if PROPERTY_SEARCH:
            return property.get_ward(street_address)
        
    match = re.search(pattern, url)
    if match:
        ward = match.group(1)
    elif PROPERTY_SEARCH:
        ward = property.get_ward(street_address)
           
    if MEMCACHE:
        memcache.set(street_address, ward)
    return ward
    
def normalize(street):
    street = street.strip().upper()
    for stopword in (' MINNEAPOLIS', ' MPLS', ' APT ', ' APT.', ' ROOM ', 
                     ' UNIT ', '#', ' NO '): 
        if stopword in street:
            index = street.index(stopword)
            street = street[:index].strip()
    return street

if __name__ == "__main__":
    print get_ward("2617 Fremont Ave S")
