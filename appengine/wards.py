import urllib
import urllib2
import lxml.html
import re
from google.appengine.api import memcache

URL = "http://apps.ci.minneapolis.mn.us/AddressPortalApp/Search/SearchPOST?AppID=WardFinderApp"

pattern = re.compile(r"/ward([0-9]+)/")

# Look up the ward for a Minneapolis street address.

def get_ward(street_address):
    street_address = normalize(street_address)
    ward = memcache.get(street_address)
    if ward is not None:
        return ward
    
    values = {'Address': street_address}
    data = urllib.urlencode(values)
    ward = 'NA'
    
    try:
        req = urllib2.Request(URL, data)
        response = urllib2.urlopen(req)
        url = response.geturl()
        match = re.search(pattern, url)
        if match:
            ward = match.group(1)
    except:
        return 'NA'

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
        
