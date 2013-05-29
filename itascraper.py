import json
import requests
import urllib
import webbrowser
import datetime
from GChartWrapper import *
from scraper_engine import *


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
ENGINE = "ITA Matrix"


DEFAULT_JSON=json.loads('{"slices":[{"origins":["PDX"],"originPreferCity":false,"commandLine":"airlines AA DL AS","destinations":["SEA"],"destinationPreferCity":false,"date":"2013-06-07","isArrivalDate":false,"dateModifier":{"minus":0,"plus":0}},{"destinations":["PDX"],"destinationPreferCity":false,"origins":["SEA"],"originPreferCity":false,"commandLine":"airlines AA DL AS","date":"2013-06-09","isArrivalDate":false,"dateModifier":{"minus":0,"plus":0}}],"pax":{"adults":1},"cabin":"COACH","maxStopCount":0,"changeOfAirport":false,"checkAvailability":true,"page":{"size":2000},"sorts":"default"}')

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

    dep_date_obj = datetime.datetime.strptime(DEPART_DATE, '%Y-%m-%d')
    return_date_obj = datetime.datetime.strptime(RETURN_DATE,'%Y-%m-%d')
    solution_query = SolutionQuery(engine=ENGINE, origin=ORIGIN, destination=DEST, depart_date=dep_date_obj, return_date=return_date_obj)

    for sol in j['result']['solutionList']['solutions']:

        origin_flight_airline = sol['itinerary']['slices'][0]['flights'][0][:2]
        origin_flight_number = int(sol['itinerary']['slices'][0]['flights'][0][2:])
        dep_time = datetime.datetime.strptime(sol['itinerary']['slices'][0]['departure'][:-6], "%Y-%m-%dT%H:%M")
        arr_time = datetime.datetime.strptime(sol['itinerary']['slices'][0]['arrival'][:-6], "%Y-%m-%dT%H:%M")
        arr_city = sol['itinerary']['slices'][0]['destination']['code']
        dep_city = sol['itinerary']['slices'][0]['origin']['code']

        origin_flight = Flight(airline=origin_flight_airline, fno=origin_flight_number, dep_city=dep_city, arr_city=arr_city, dep_time=dep_time, arr_time=arr_time)

        return_flight_airline = sol['itinerary']['slices'][1]['flights'][0][:2]
        return_flight_number = int(sol['itinerary']['slices'][1]['flights'][0][2:])
        dep_time = datetime.datetime.strptime(sol['itinerary']['slices'][1]['departure'][:-6], "%Y-%m-%dT%H:%M")
        arr_time = datetime.datetime.strptime(sol['itinerary']['slices'][1]['arrival'][:-6], "%Y-%m-%dT%H:%M")
        arr_city = sol['itinerary']['slices'][1]['destination']['code']
        dep_city = sol['itinerary']['slices'][1]['origin']['code']

        return_flight = Flight(airline=return_flight_airline, fno=return_flight_number, dep_city=dep_city, arr_city=arr_city, dep_time=dep_time, arr_time=arr_time)

        flight_list = [origin_flight, return_flight]
        price = sol['displayTotal']
        solution = Solution(flights=flight_list, price=price)
        solution_query.solutions.append(solution)

    solution_query.save()
    return solution_query

def show_graph(solutions, filename):
    prices = list()
    for s in solutions:
        prices.append(float(s.price[3:]))

    G = GChart('lc', prices, chds='a')
    G.size(500,500)
    G.save(filename)

if __name__ == '__main__':
    connectDB()
    flights = build_solutions()
