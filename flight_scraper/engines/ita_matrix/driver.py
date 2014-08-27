import json
import logging
import datetime
import requests
from abc import abstractmethod
from flight_scraper.solution_model import Solution, Flight, Itinerary, CalendarSolution, TripMinimumPrice

logging.basicConfig(level=logging.INFO)

class AbstractItaMatrixDriver(object):
    
    _logger = logging.getLogger(__name__)
    engine = "ITA Matrix"
    _base_url = "http://matrix.itasoftware.com"
    _request_uri = "/xhr/shop/search?"
    _http_header = {
        'Host': 'matrix.itasoftware.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Content-Length': '0'
    }
    
    def __init__(self, origin, destination, depart_date, return_date, max_stops, airlines):
        self.origin = origin
        self.destination = destination
        self.depart_date = depart_date
        self.return_date = return_date
        self.max_stops = max_stops
        self.airlines = airlines
    
    @property
    def origin(self):
        return self._json_request['slices'][0]['origins'][0]

    @origin.setter
    def origin(self, origin):
        self._json_request['slices'][0]['origins'][0] = origin
        self._json_request['slices'][1]['destinations'][0] = origin

    @property
    def destination(self):
        return self._json_request['slices'][0]['destinations'][0]

    @destination.setter
    def destination(self, destination):
        self._json_request['slices'][0]['destinations'][0] = destination
        self._json_request['slices'][1]['origins'][0] = destination
        
    @property
    def max_stops(self):
        return self._json_request['maxStopCount']
    
    @max_stops.setter
    def max_stops(self, stops):
        if stops is None:
            stops = 2
        self._json_request['maxStopCount'] =   stops
        
    @property
    def airlines(self):
        return self._json_request['slices'][0]['routeLanguage']
    
    @airlines.setter
    def airlines(self, airlines):
        if airlines is not None:
            self._json_request['slices'][0]['routeLanguage'] = airlines
            self._json_request['slices'][1]['routeLanguage'] = airlines

    def build_solutions(self):    
        data = self._base_request + json.dumps(self._json_request)
        request_url = self._base_url + self._request_uri + data

        self._logger.info('Making request to ITA Matrix: %s', (request_url))
        print 'Making request to ITA Matrix: %s' % (request_url)
        response = requests.post(request_url, headers=self._http_header)
        response_json = json.loads(response.text[4:])

        print response_json
        self._logger.info('Creating objects to insert to database')
        return self._parse_response(response_json)
        
    @abstractmethod
    def _parse_response(self):
        raise NotImplementedError('Subclasses must implement _parse_solution')
    
    
class ItaMatrixDriver(AbstractItaMatrixDriver):

    _base_request = "name=specificDates&summarizers=carrierStopMatrix"\
                    "%2CcurrencyNotice%2CsolutionList%2CitineraryPriceSlider%2C"\
                    "itineraryCarrierList%2CitineraryDepartureTimeRanges%2CitineraryArrivalTimeRanges"\
                    "%2CdurationSliderItinerary%2CitineraryOrigins%2CitineraryDestinations%2C"\
                    "itineraryStopCountList%2CwarningsItinerary&format=JSON&inputs="

    _json_request = json.loads('{"slices":[{"origins":["PDX"],"originPreferCity":false,"commandLine":"airlines AA DL AS UA",\
                               "destinations":["SEA"],"destinationPreferCity":false,"date":"2013-06-07","isArrivalDate":false,\
                                "dateModifier":{"minus":0,"plus":0}},{"destinations":["PDX"],"destinationPreferCity":false,\
                                "origins":["SEA"],"originPreferCity":false,"commandLine":"airlines AA DL AS","date":"2013-06-09",\
                                "isArrivalDate":false,"dateModifier":{"minus":0,"plus":0}}],"pax":{"adults":1},"cabin":"COACH","maxStopCount":0,\
                                "changeOfAirport":false,"checkAvailability":true,"page":{"size":2000},"sorts":"default"}')

    def __init__(self, origin, destination, depart_date, return_date, max_stops=None, airlines=None):
        super(ItaMatrixDriver, self).__init__(origin, destination, depart_date, return_date, max_stops, airlines)

    @property
    def depart_date(self):
        return datetime.datetime.strptime(self._json_request['slices'][0]['date'], "%Y-%m-%d")

    @depart_date.setter
    def depart_date(self, depart_date):
        self._json_request['slices'][0]['date'] = depart_date.strftime('%Y-%m-%d')

    @property
    def return_date(self):
        return datetime.datetime.strptime(self._json_request['slices'][1]['date'], "%Y-%m-%d")

    @return_date.setter
    def return_date(self, return_date):
        self._json_request['slices'][1]['date'] = return_date.strftime('%Y-%m-%d')
        
    @property
    def airlines(self):
        return self._json_request['slices'][0]['routeLanguage']
    
    @airlines.setter
    def airlines(self, airlines):
        self._json_request['slices'][0]['routeLanguage'] = airlines
        self._json_request['slices'][1]['routeLanguage'] = airlines

    def _parse_response(self, response_json):
        """
            Builds search solution. Adds to MongoDB and returns the Solution object.
        """
        self._logger.info('Creating objects to insert to database')
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
            origin_flight.save()
 
            return_flight_airline = sol['itinerary']['slices'][1]['flights'][0][:2]
            return_flight_number = int(sol['itinerary']['slices'][1]['flights'][0][2:])
            dep_time = datetime.datetime.strptime(sol['itinerary']['slices'][1]['departure'][:-6], "%Y-%m-%dT%H:%M")
            arr_time = datetime.datetime.strptime(sol['itinerary']['slices'][1]['arrival'][:-6], "%Y-%m-%dT%H:%M")
            arr_city = sol['itinerary']['slices'][1]['destination']['code']
            dep_city = sol['itinerary']['slices'][1]['origin']['code']
 
            return_flight = Flight(airline=return_flight_airline, fno=return_flight_number, dep_city=dep_city, arr_city=arr_city, dep_time=dep_time, arr_time=arr_time)
            return_flight.save()
 
            flight_list = [origin_flight, return_flight]
            price = sol['displayTotal']
            itinerary = Itinerary(flights=flight_list, price=price)
            solution.itineraries.append(itinerary)
            solution = Solution(engine=self.engine, origin=self.origin, destination=self.destination, depart_date=self.depart_date, return_date=self.return_date)
 
        solution.save()
 
        return solution

class CalendarItaMatrixDriver(AbstractItaMatrixDriver):
    
    _base_request = "name=calendar&summarizers=currencyNotice%2CovernightFlightsCalendar"\
                    "%2CitineraryStopCountList%2CitineraryCarrierList%2Ccalendar&format=JSON&inputs="
    
    _json_request = json.loads('{"slices":[{"origins":["BWI"],"originPreferCity":false,"routeLanguage":"C:DL","destinations":["MSP"],\
                               "destinationPreferCity":false},{"destinations":["BWI"],"destinationPreferCity":false,"origins":["MSP"],\
                               "originPreferCity":false,"routeLanguage":"C:DL"}],"startDate":"2014-07-01","layover":{"max":5,"min":4},\
                               "pax":{"adults":1},"cabin":"COACH","maxStopCount":0,"changeOfAirport":false,"checkAvailability":true,\
                               "firstDayOfWeek":"SUNDAY","endDate":"2014-08-01"}')
    
    def __init__(self, origin, destination, depart_date, return_date, day_range, max_stops=None, airlines=None):
        super(CalendarItaMatrixDriver, self).__init__(origin, destination, depart_date, return_date, max_stops, airlines)
        self.day_range  = day_range
    
    @property
    def depart_date(self):
        return datetime.datetime.strptime(self._json_request['startDate'], "%Y-%m-%d")

    @depart_date.setter
    def depart_date(self, depart_date):
        self._json_request['startDate'] = depart_date.strftime('%Y-%m-%d')

    @property
    def return_date(self):
        return datetime.datetime.strptime(self._json_request['endDate'], "%Y-%m-%d")

    @return_date.setter
    def return_date(self, return_date):
        self._json_request['endDate'] = return_date.strftime('%Y-%m-%d')
        
    @property
    def day_range(self):
        return self._json_request['layover']
    
    @day_range.setter
    def day_range(self, days):
        self._json_request['layover'] = {'min': days[0], 'max': days[1]}
        
    def _parse_response(self, response_json):         
        self._logger.info('Creating objects to insert to database')
        solution = CalendarSolution(engine=self.engine, origin=self.origin, destination=self.destination, 
                                    depart_date=self.depart_date, return_date=self.return_date)
 
        prices = []
        for month in response_json['result']['calendar']['months']:
            for week in month['weeks']:
                for day in week['days']:
                    if day['solutionCount'] == 0:
                        continue
                    for sol in day['tripDuration']['options']:
                        
                        dep_time = datetime.datetime.strptime(sol['solution']['slices'][0]['departure'][:10], "%Y-%m-%d").date()
                        arr_time = datetime.datetime.strptime(sol['solution']['slices'][1]['departure'][:10], "%Y-%m-%d").date()
                        price = sol['minPrice']
                        trip  = TripMinimumPrice(dep_city=self.origin, arr_city=self.destination, dep_time=dep_time, arr_time=arr_time, price=price)
                        prices.append(float(price.replace('USD', ''))) #FIXME: Can't assume USD
                        
                        solution.trip_prices.append(trip)
 
        solution.min_price = str(min(prices))
        solution.save()
        
        return solution
