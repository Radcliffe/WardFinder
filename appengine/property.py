import lxml.html
import urllib
import urllib2

# Get property info from City of Minneapolis website.

URL="http://apps.ci.minneapolis.mn.us/AddressPortalApp/Search/SearchPOST?AppID=PIApp"

def get_ward(street):
    values = {'Address': street}
    data = urllib.urlencode(values)
    property_info = {}
    req = urllib2.Request(URL, data)
    try:      
        response = urllib2.urlopen(req)
        html = response.read()
        doc = lxml.html.fromstring(html)
        extra = doc.get_element_by_id('extra')
        return extra[0][1][2][0].text.split()[1]
    except:
        return 'NA'
 
        
if __name__ == "__main__":
    ward = get_ward_from_property("1519 Fremont Ave")
    print ward        
