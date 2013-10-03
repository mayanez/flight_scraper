import requests
import urllib
import webbrowser
import BeautifulSoup
import re
from ghost import Ghost

BASE_URL="http://www.flightstats.com"
REQUEST_URI="/go/FlightAvailability/flightAvailability.do"

HTTP_HEADER={
    'Host' : 'www.flightstats.com',
    'Content-Type' : 'text/html'
}

PARAMS={
    'departure' : 'SEA',
    'airline' : '',
    'arrival' : 'JFK',
    'connection' : '',
    'queryDate' : '2013-10-11',
    'queryTime' : 'C',
    'excludeConnectionCodes' : '',
    'cabinCode' : 'A',
    'numOfSeats' : '1',
    'queryType' : 'D',
    'fareClassCodes' : ''
}

ORIGIN = 'SEA'
DEST = 'JFK'
DEPART_DATE = '2013-09-27'

def set_origin(origin_code):
    global ORIGIN
    PARAMS['departure'] = ORIGIN
    return origin_code

def set_destination(dest_code):
    global DEST
    PARAMS['arrival'] = DEST
    return dest_code

def set_dep_date(date):
    global DEPART_DATE
    PARAMS['queryDate'] = DEPART_DATE
    return date

def get_content():
    ghost = Ghost(wait_timeout=40)
    params = urllib.urlencode(PARAMS)
    request_url = BASE_URL+REQUEST_URI+("?%s" % params)
    page, resources = ghost.open(request_url)
    result, response = ghost.evaluate('JSON.stringify(availRoutes);')
    print str(result)

if __name__ == '__main__':
    get_content()


