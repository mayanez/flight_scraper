import json
import requests


BASE_URL="http://matrix.itasoftware.com"
REQUEST_URL = "/xhr/shop/search?"

HTTP_HEADER= {
        'Host' : 'matrix.itasoftware.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control' : 'no-cache'
}

BASE_REQUEST="name=specificDates&summarizers=carrierStopMatrix\
%2CcurrencyNotice%2CsolutionList%2CitineraryPriceSlider%2C\
itineraryCarrierList%2CitineraryDepartureTimeRanges%2CitineraryArrivalTimeRanges\
%2CdurationSliderItinerary%2CitineraryOrigins%2CitineraryDestinations%2C\
itineraryStopCountList%2CwarningsItinerary&format=JSON&inputs="

ORIGIN = "PDX"
ORIGIN_DATE = "2013-06-07"
DEST = "SEA"
DEST_DATE = "2013-06-09"


DEFAULT_JSON=json.loads('{"slices":[{"origins":["PDX"],"originPreferCity":false,"commandLine":"airlines AA DL AS","destinations":["SEA"],"destinationPreferCity":false,"date":"2013-06-07","isArrivalDate":false,"dateModifier":{"minus":0,"plus":0}},{"destinations":["PDX"],"destinationPreferCity":false,"origins":["SEA"],"originPreferCity":false,"commandLine":"airlines AA DL AS","date":"2013-06-09","isArrivalDate":false,"dateModifier":{"minus":0,"plus":0}}],"pax":{"adults":1},"cabin":"COACH","changeOfAirport":true,"checkAvailability":true,"page":{"size":2000},"sorts":"default"}')

def set_origin(origin_code):
    DEFAULT_JSON['slices'][0]['origins'][0] = origin_code
    DEFAULT_JSON['slices'][1]['destinations'][0] = origin_code
    ORIGIN = origin_code
    return origin_code

def set_destination(dest_code):
    DEFAULT_JSON['slices'][0]['destinations'][0] = dest_code
    DEFAULT_JSON['slices'][0]['origins'][0] = dest_code
    DEST = dest_code
    return dest_code

def set_dept_date(date):
    DEFAULT_JSON['slices'][0]['date'] = date
    DEST_DATE = date
    return date

def set_arr_date(date):
    DEFAULT_JSON['slices'][1]['date'] = date
    ORIGIN_DATE = date
    return date

def find_flights():
    data = BASE_REQUEST+json.dumps(DEFAULT_JSON)
    resp =  requests.post(BASE_URL+REQUEST_URL+data, headers=HTTP_HEADER)
    return json.loads(resp.text[4:])

def find_lowest_price(json):
    return json['result']['solutionList']['minPrice']

def find_solutions(json):
    for sol in json['result']['solutionList']['solutions']:
        
        dep_flight = sol['itinerary']['slices'][0]['flights'][0]
        dep_time = sol['itinerary']['slices'][0]['departure']
        arr_flight = sol['itinerary']['slices'][1]['flights'][0]
        arr_time = sol['itinerary']['slices'][1]['departure']
        print "Flights: %s , %s" % (dep_flight, arr_flight)
        print "Depart Times: %s , %s" % (dep_time, arr_time)
        print sol['displayTotal']
        print "\n"




if __name__ == '__main__':

    print "Finding flights...%s to %s...%s / %s" % (ORIGIN, DEST, ORIGIN_DATE, DEST_DATE)
    flights = find_flights()
    find_solutions(flights)


