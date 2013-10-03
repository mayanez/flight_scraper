import requests
import urllib
import webbrowser
import BeautifulSoup
import re
from ..solution_model import *

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
    'queryDate' : '2013-09-27',
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
    request_url = BASE_URL+REQUEST_URI
    resp = requests.get(request_url, params=PARAMS)
    soup = BeautifulSoup.BeautifulSoup(resp.text)
    scripts_list = [s.extract() for s in soup('script')]
    p = re.compile('availLoadingDiv')
    i=0
    for s in scripts_list:
        print i
        i+=1
        if p.findall(s.text):
            print s

#Now must modify the JS found and then serialize the result into a JSON. This will then be properly inserted into DB

if __name__ == '__main__':
    get_content()


