import urllib
import json
import datetime
import logging

from selenium import webdriver
from flight_scraper.solution_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    'queryTime' : '2',
    'excludeConnectionCodes' : '',
    'cabinCode' : 'A',
    'numOfSeats' : '1',
    'queryType' : 'D',
    'fareClassCodes' : ''
}

ORIGIN = 'SEA'
DEST = 'JFK'
DEPART_DATE = '2013-10-11'
DRIVER = None

def init():
    global DRIVER
    logger.debug("Starting PhantomJS Selenium Driver")
    DRIVER = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs", service_log_path="/Users/mayanez/Library/Logs/ghostdriver.log")

def set_origin(origin_code):
    global ORIGIN
    ORIGIN = origin_code
    PARAMS['departure'] = ORIGIN
    return origin_code

def set_destination(dest_code):
    global DEST
    DEST = dest_code
    PARAMS['arrival'] = DEST
    return dest_code

def set_dep_date(date):
    global DEPART_DATE
    DEPART_DATE = date
    PARAMS['queryDate'] = DEPART_DATE
    return date

def extract_flights_with_seats(json_obj):

    flight_list = list()
    logger.info('Extracting flights with seats')
    for k, results in json_obj.iteritems():
        for k2, flights in results['flights'].iteritems():
            airline = flights['airline']
            fno = flights['flightNumber']
            dep_city = flights['depCode']
            arr_city = flights['arrCode']
            flight = Flight(dep_city=dep_city, arr_city=arr_city, airline=airline, fno=fno, dep_time=datetime.datetime.strptime(DEPART_DATE, "%Y-%m-%d"))
            seats = list()

            for k3, cabin in flights['cabins'].iteritems():
                cabin_code = cabin['code']

                for fare_class, seat_availability in cabin['fares'].iteritems():
                    if seat_availability == "":
                        seat_availability = 0
                    else:
                        seat_availability = int(seat_availability)

                    seat = Seat(cabin_code=cabin_code, fare_class=fare_class, availability=seat_availability)
                    seats.append(seat)

            flight.seats = seats
            flight_list.append(flight)

    return flight_list

def get_seat_availability():
    global DRIVER
    params = urllib.urlencode(PARAMS)
    request_url = BASE_URL+REQUEST_URI+("?%s" % params)
    logger.info('Requesting URL: %s' % (request_url))
    DRIVER.get(request_url)
    logger.info('Running Javascript to retrieve available routes')
    result = DRIVER.execute_script('return JSON.stringify(availRoutes)')
    j = json.loads(unicode(result))

    flight_list = extract_flights_with_seats(j)
    logger.info('Saving SeatQuery to Database')
    seat_query = SeatQuery(flights=flight_list)
    seat_query.save()
    logger.info('Quiting the Web Driver')
    DRIVER.quit

    return flight_list

