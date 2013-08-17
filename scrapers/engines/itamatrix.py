import json
import requests
import urllib
import webbrowser
import datetime
from ..solution_model import *


BASE_URL="http://matrix.itasoftware.com"
REQUEST_URL = "/xhr/shop/search?"

HTTP_HEADER= {
        'Host' : 'matrix.itasoftware.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control' : 'no-cache',
        'Content-Length' : '0'
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


DEFAULT_JSON=json.loads('{"slices":[{"origins":["PDX"],"originPreferCity":false,"commandLine":"airlines AA DL AS UA","destinations":["SEA"],"destinationPreferCity":false,"date":"2013-06-07","isArrivalDate":false,"dateModifier":{"minus":0,"plus":0}},{"destinations":["PDX"],"destinationPreferCity":false,"origins":["SEA"],"originPreferCity":false,"commandLine":"airlines AA DL AS","date":"2013-06-09","isArrivalDate":false,"dateModifier":{"minus":0,"plus":0}}],"pax":{"adults":1},"cabin":"COACH","maxStopCount":0,"changeOfAirport":false,"checkAvailability":true,"page":{"size":2000},"sorts":"default"}')

def set_origin(origin_code):
    global ORIGIN
    DEFAULT_JSON['slices'][0]['origins'][0] = origin_code
    DEFAULT_JSON['slices'][1]['destinations'][0] = origin_code
    ORIGIN = origin_code
    return origin_code

def set_destination(dest_code):
    global DEST
    DEFAULT_JSON['slices'][0]['destinations'][0] = dest_code
    DEFAULT_JSON['slices'][1]['origins'][0] = dest_code
    DEST = dest_code
    return dest_code

def set_dep_date(date):
    global DEPART_DATE
    DEFAULT_JSON['slices'][0]['date'] = date
    DEPART_DATE = date
    return date

def set_return_date(date):
    global RETURN_DATE
    DEFAULT_JSON['slices'][1]['date'] = date
    RETURN_DATE = date
    return date

def build_solutions():
    """
        Builds search solution. Adds to MongoDB and returns the Solution object.
    """
    
    data = BASE_REQUEST+json.dumps(DEFAULT_JSON)
    resp =  requests.post(BASE_URL+REQUEST_URL+data, headers=HTTP_HEADER)
    j = json.loads(resp.text[4:])

    dep_date_obj = datetime.datetime.strptime(DEPART_DATE, '%Y-%m-%d')
    return_date_obj = datetime.datetime.strptime(RETURN_DATE,'%Y-%m-%d')
    min_price = j['result']['solutionList']['minPrice']

    solution = Solution(engine=ENGINE, origin=ORIGIN, destination=DEST, depart_date=dep_date_obj, return_date=return_date_obj)
    solution.min_price = min_price
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
        itinerary = Itinerary(flights=flight_list, price=price)
        solution.itineraries.append(itinerary)

    solution.save()
    return solution

