import json
import requests
import urllib
import webbrowser
from GChartWrapper import *


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
DEPART_DATE = "2013-06-07"
DEST = "SEA"
RETURN_DATE = "2013-06-09"


DEFAULT_JSON=json.loads('{"slices":[{"origins":["PDX"],"originPreferCity":false,"commandLine":"airlines AA DL AS","destinations":["SEA"],"destinationPreferCity":false,"date":"2013-06-07","isArrivalDate":false,"dateModifier":{"minus":0,"plus":0}},{"destinations":["PDX"],"destinationPreferCity":false,"origins":["SEA"],"originPreferCity":false,"commandLine":"airlines AA DL AS","date":"2013-06-09","isArrivalDate":false,"dateModifier":{"minus":0,"plus":0}}],"pax":{"adults":1},"cabin":"COACH","maxStopCount":0,"changeOfAirport":false,"checkAvailability":true,"page":{"size":2000},"sorts":"default"}')

class Solution(object):
    def __init__(self, flights, price, dep_city, arr_city):
        self.flights = flights
        self.price = price
        self.dep_city = dep_city
        self.arr_city = arr_city

    def set_stop(conn_flight):
        self.flights.append(conn_flight)

    def __str__(self):
        result = "Solution: %s\n" % (self.price)
        for f in self.flights:
            result += str(f)
            result += "\n"
        return result

class Flight(object):
    def __init__(self,airline,fno, dep_city, arr_city, dep_time, arr_time):
        self.airline = airline
        self.fno = fno
        self.dep_city = dep_city
        self.arr_city = arr_city
        self.dep_time = dep_time
        self.arr_time = arr_time

    def __str__(self):
        return "Flight: %s %s \n%s-%s\n%s  -  %s" % (self.airline, self.fno, self.dep_city, self.arr_city, self.dep_time, self.arr_time)

    def show_seat_map(self):
        url = "http://www.seatguru.com/findseatmap/findseatmap.php?"
        params = { 'carrier':self.airline,
                    'flightno':self.flightno }
        url = url + urllib.urlencode(params)
        webbrowser.open_new(url)

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

def set_dep_date(date):
    DEFAULT_JSON['slices'][0]['date'] = date
    RETURN_DATE = date
    return date

def set_return_date(date):
    DEFAULT_JSON['slices'][1]['date'] = date
    DEPART_DATE = date
    return date

def search_flights():
    print "Finding flights...%s to %s...%s / %s" % (ORIGIN, DEST, DEPART_DATE, RETURN_DATE)
    return build_solutions()


def build_solutions():
    """Returns a list of Solutions"""

    data = BASE_REQUEST+json.dumps(DEFAULT_JSON)
    resp =  requests.post(BASE_URL+REQUEST_URL+data, headers=HTTP_HEADER)
    j = json.loads(resp.text[4:])

    solution_list = list()

    for sol in j['result']['solutionList']['solutions']:

        origin_flight_airline = sol['itinerary']['slices'][0]['flights'][0][:2]
        origin_flight_number = sol['itinerary']['slices'][0]['flights'][0][2:]
        dep_time = sol['itinerary']['slices'][0]['departure']
        arr_time = sol['itinerary']['slices'][0]['arrival']
        arr_city = sol['itinerary']['slices'][0]['destination']['code']
        dep_city = sol['itinerary']['slices'][0]['origin']['code']

        origin_flight = Flight(origin_flight_airline, origin_flight_number, dep_city, arr_city, dep_time, arr_time)


        return_flight_airline = sol['itinerary']['slices'][1]['flights'][0][:2]
        return_flight_number = sol['itinerary']['slices'][1]['flights'][0][2:]
        dep_time = sol['itinerary']['slices'][1]['departure']
        arr_time = sol['itinerary']['slices'][1]['arrival']
        arr_city = sol['itinerary']['slices'][1]['destination']['code']
        dep_city = sol['itinerary']['slices'][1]['origin']['code']

        return_flight = Flight(return_flight_airline, return_flight_number, dep_city, arr_city, dep_time, arr_time)

        #Build Flight List and create Solution Object.
        flight_list = [origin_flight, return_flight]
        price = sol['displayTotal']
        solution = Solution(flight_list, price, ORIGIN, DEST)
        solution_list.append(solution)

    return solution_list

def show_graph(solutions, filename):
    prices = list()
    for s in solutions:
        prices.append(float(s.price[3:]))

    G = GChart('lc', prices, chds='a')
    G.size(500,500)
    G.save(filename)

if __name__ == '__main__':

    flights = build_solutions()
    for s in flights:
        print s
