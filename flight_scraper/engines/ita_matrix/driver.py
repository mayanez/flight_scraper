import json
import logging
import datetime
import requests
from flight_scraper.solution_model import Solution, Flight, Itinerary

logging.basicConfig(level=logging.INFO)

class ItaMatrixDriver(object):
    __logger = logging.getLogger(__name__)
    engine = "ITA Matrix"
    __base_url = "http://matrix.itasoftware.com"
    __request_uri = "/xhr/shop/search?"
    __http_header = {
        'Host': 'matrix.itasoftware.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Content-Length': '0'
    }
    __base_request = "name=specificDates&summarizers=carrierStopMatrix\
%2CcurrencyNotice%2CsolutionList%2CitineraryPriceSlider%2C\
itineraryCarrierList%2CitineraryDepartureTimeRanges%2CitineraryArrivalTimeRanges\
%2CdurationSliderItinerary%2CitineraryOrigins%2CitineraryDestinations%2C\
itineraryStopCountList%2CwarningsItinerary&format=JSON&inputs="
    __json_request = json.loads('{"slices":[{"origins":["PDX"],"originPreferCity":false,"commandLine":"airlines AA DL AS UA","destinations":["SEA"],"destinationPreferCity":false,"date":"2013-06-07","isArrivalDate":false,"dateModifier":{"minus":0,"plus":0}},{"destinations":["PDX"],"destinationPreferCity":false,"origins":["SEA"],"originPreferCity":false,"commandLine":"airlines AA DL AS","date":"2013-06-09","isArrivalDate":false,"dateModifier":{"minus":0,"plus":0}}],"pax":{"adults":1},"cabin":"COACH","maxStopCount":0,"changeOfAirport":false,"checkAvailability":true,"page":{"size":2000},"sorts":"default"}')


    @property
    def origin(self):
        return self.__json_request['slices'][0]['origins'][0]

    @origin.setter
    def origin(self, origin):
        self.__json_request['slices'][0]['origins'][0] = origin
        self.__json_request['slices'][1]['destinations'][0] = origin

    @property
    def destination(self):
        return self.__json_request['slices'][0]['destinations'][0]

    @destination.setter
    def destination(self, destination):
        self.__json_request['slices'][0]['destinations'][0] = destination
        self.__json_request['slices'][1]['origins'][0] = destination

    @property
    def depart_date(self):
        return datetime.datetime.strptime(self.__json_request['slices'][0]['date'], "%Y-%m-%d")

    @depart_date.setter
    def depart_date(self, depart_date):
        self.__json_request['slices'][0]['date'] = depart_date.strftime('%Y-%m-%d')

    @property
    def return_date(self):
        return datetime.datetime.strptime(self.__json_request['slices'][1]['date'], "%Y-%m-%d")

    @return_date.setter
    def return_date(self, return_date):
        self.__json_request['slices'][1]['date'] = return_date.strftime('%Y-%m-%d')

    def __init__(self, origin, destination, depart_date, return_date):
        self.origin = origin
        self.destination = destination
        self.depart_date = depart_date
        self.return_date = return_date

    def build_solutions(self):
        """
            Builds search solution. Adds to MongoDB and returns the Solution object.
        """
        data = self.__base_request + json.dumps(self.__json_request)
        request_url = self.__base_url + self.__request_uri + data

        self.__logger.info('Making request to ITA Matrix: %s', (request_url))
        print 'Making request to ITA Matrix: %s' % (request_url)
        response = requests.post(request_url, headers=self.__http_header)
        response_json = json.loads(response.text[4:])

        print response_json
        self.__logger.info('Creating objects to insert to database')
        solution = Solution(engine=self.engine, origin=self.origin, destination=self.destination, depart_date=self.depart_date, return_date=self.return_date)
        solution.min_price = response_json['result']['solutionList']['minPrice']

        for sol in response_json['result']['solutionList']['solutions']:
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


