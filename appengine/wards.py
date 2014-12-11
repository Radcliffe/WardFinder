import urllib
import urllib2
import lxml.html
import re
from google.appengine.api import memcache

URL = "http://apps.ci.minneapolis.mn.us/AddressPortalApp/Search/SearchPOST?AppID=WardFinderApp"

# Look up the ward for a Minneapolis street address.

def lookup_address(street_address):
    values = {'Address': street_address}
    data = urllib.urlencode(values)
    result = memcache.get(street_address)
    if result is not None:
        return result
    result = 'NA, NA'
    try:
        req = urllib2.Request(URL, data)
        response = urllib2.urlopen(req)
        html = response.read()
        doc = lxml.html.fromstring(html)
    except:
        return result
    title = doc.find('head/title')
    if title is not None:
        text = title.text.strip()
        match = re.match("Ward (\d+) - (.*) - City of Minneapolis", text)
        if match:
            result = ', '.join(match.groups())
    memcache.set(street_address, result)
    return result
