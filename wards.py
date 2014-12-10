import sys
import time
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
    return doc.find('head/title').text or 'NA'

# Look up a list of addresses and write the results to a file.

def lookup(input_file_name, output_file_name, delay_ms):
    delay_s = .001 * delay_ms
    with open(input_file_name, "rt") as f:
        addresses = [address.strip() for address in f.readlines()]
    wards = [lookup_address(address) for address in addresses]
    with open(output_file_name, "wt") as f:
        f.writelines("%s, %s\n  " % (x, y) for x, y in zip(addresses, wards))
        

if __name__ == "__main__":
    num_args = len(sys.argv)
    if num_args > 4 or num_args < 3:
        print "Usage: python wards.py inputfile.txt outputfile.txt delay"
        print "Delay is the number of milliseconds to pause between requests."
        print "(Default delay is 500)"
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    delay_ms = 500
    if num_args == 4:
        delay_ms = int(sys.argv[3])
    lookup(input_file_name, output_file_name, delay_ms)

