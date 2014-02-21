import json
import logging
import urllib
from scrapers.solution_model import Seat, Flight, SeatQuery
from selenium import webdriver

logging.basicConfig(level=logging.INFO)

class FlightStatsDriver(webdriver.PhantomJS):
    __logger = logging.getLogger(__name__)
    __base_url = "http://www.flightstats.com"
    __request_uri = "/go/FlightAvailability/flightAvailability.do"
    __http_header = {
            'Host' : 'www.flightstats.com',
            'Content-Type' : 'text/html'}
    __params = {
        'departure' : '',
        'airline' : '',
        'arrival' : '',
        'connection' : '',
        'queryDate' : '', #yyyy-mm-dd
        'queryTime' : '2',
        'excludeConnectionCodes' : '',
        'cabinCode' : 'A',
        'numOfSeats' : '1',
        'queryType' : 'D',
        'fareClassCodes' : ''}

    @property
    def origin(self):
        return self.__origin

    @origin.setter
    def origin(self, origin):
        self.__origin = origin

    @property
    def destination(self):
        return self.__destination

    @destination.setter
    def destination(self, destination):
        self.__destination = destination

    @property
    def depart_date(self):
        return self.__depart_date

    @depart_date.setter
    def depart_date(self, depart_date):
        self.__depart_date = depart_date

    @property
    def return_date(self):
        return self.__return_date

    @return_date.setter
    def return_date(self, return_date):
        self.__return_date = return_date

    def __init__(self, executable_path, service_log_path):
       webdriver.PhantomJS(executable_path=executable_path, service_log_path=service_log_path)

    def __extract_flights_with_seats(self, json_obj):

        flight_list = list()
        self.__logger.info('Extracting flights with seats')
        for k, results in json_obj.iteritems():
            for k2, flights in results['flights'].iteritems():
                airline = flights['airline']
                fno = flights['flightNumber']
                dep_city = flights['depCode']
                arr_city = flights['arrCode']
                flight = Flight(dep_city=dep_city, arr_city=arr_city, airline=airline, fno=fno, dep_time=self.depart_date)
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

    def get_seat_availability(self):
        params = urllib.urlencode(self.__params)
        request_url = self.__base_url + self.__request_uri +("?%s" % params)
        self.__logger.info('Requesting URL: %s' % (self.__request_url))
        self.get(request_url)
        self.__logger.info('Running Javascript to retrieve available routes')
        result = self.execute_script('return JSON.stringify(availRoutes)')
        j = json.loads(unicode(result))

        flight_list = self.__extract_flights_with_seats(j)
        self.__logger.info('Saving SeatQuery to Database')
        seat_query = SeatQuery(flights=flight_list)
        seat_query.save()
        self.__logger.info('Quiting the Web Driver')
        self.quit

        return flight_list