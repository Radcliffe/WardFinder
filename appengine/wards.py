import urllib
import urllib2
import lxml.html

URL = "http://apps.ci.minneapolis.mn.us/AddressPortalApp/Search/SearchPOST?AppID=WardFinderApp"

# Look up the ward for a Minneapolis street address.

def lookup_address(street_address):
    values = {'Address': street_address}
    data = urllib.urlencode(values)
    try:
        req = urllib2.Request(URL, data)
        response = urllib2.urlopen(req)
        html = response.read()
        doc = lxml.html.fromstring(html)
    except:
        return 'NA'
    title = doc.find('head/title')
    if title:
        return title.text
    return 'NA'
