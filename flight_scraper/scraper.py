from flight_scraper.solution_model import Solution, ItaSolution, CalendarSolution, SeatQuery
from engines.ita_matrix.driver import ItaMatrixDriver, ItaMatrixDriverMulti, CalendarItaMatrixDriver, Slice
from datetime import date, timedelta

class FlightScraper(object):
    
    def __init__(self, origin, destination, depart_date, return_date, 
                 max_stops=None, day_range=None, airlines=None):
        self.origin         =   origin
        self.destination    =   destination
        self.depart_date    =   depart_date
        self.return_date    =   return_date
        self.day_range      =   day_range
        self.max_stops      =   max_stops
        self.airlines       =   airlines

    def search_flights(self):
        ita_driver = ItaMatrixDriver(self.origin, self.destination, self.depart_date, self.return_date, self.max_stops, self.airlines)
        return ita_driver.build_solutions()
    
    def search_calendar(self):
        ita_driver = CalendarItaMatrixDriver(self.origin, self.destination, self.depart_date, self.return_date, 
                                     day_range=self.day_range, max_stops=self.max_stops, airlines=self.airlines)
        return ita_driver.build_solutions()
    
    def minimum_trips(self):
        """
        Returns a CalendarSolution object from MongoDB
        """
        return CalendarSolution.objects(origin=self.origin, destination=self.destination, 
                                        depart_date=self.depart_date, return_date=self.return_date) 

    def solutions(self):
        """
        Returns a Solution object from MongoDB
        """
        return Solution.objects(depart_date=self.depart_date, return_date=self.return_date, 
                                origin=self.origin, destination=self.destination)

    def itineraries(self, flights_to_match):
        results = list()
        solutions = self.solutions()

        for sol in solutions:
            itineraries = sol.itineraries
            for itinerary in itineraries:
                flights = set(itinerary.flights)
                matched = flights.intersection(flights_to_match)
                if len(matched) > 0:
                    results.append(itinerary)

        return results

    def __get_seats(self, date):
        seat_query = SeatQuery.objects(flights__dep_city=self.__origin, flights__arr_city=self.__destination, flights__dep_time=date)
        return seat_query

    def departure_seats(self):
        return self.__get_seats(self.__depart_date)

    def return_seats(self):
        return self.__get_seats(self.__return_date)
    
class FlightScraperMulti(object):
    
    def __init__(self, max_stops=None):
        #self.origin         =   None
        #self.destination    =   None
        #self.depart_date    =   None
        #self.return_date    =   None
        #self.day_range      =   None
        self.max_stops      =   max_stops
        #self.airlines       =   None
        self._ita_driver = ItaMatrixDriverMulti(self.max_stops)
        
    def add_flight(self, origin, destination, depart_date, airlines=None):
        self._ita_driver.add_slice_params(origin, destination, depart_date, airlines)
        
    def search_flights(self):
        return self._ita_driver.build_solutions()

def scrape_return():    
    scraper =   FlightScraper('SFO', 'SEA', date.today() + timedelta(days=30), date.today() + timedelta(days=47))
    solution =  scraper.search_flights()
    
    return solution
    
def scrape_multi():    
    from datetime import date
    scraper =   FlightScraperMulti()
    scraper.add_flight('SFO', 'SEA', date.today() + timedelta(days=30), airlines="AA DL AC")
    scraper.add_flight('SEA', 'PHX', date.today() + timedelta(days=40))
    scraper.add_flight('PHX', 'SFO', date.today() + timedelta(days=47))
    solution =  scraper.search_flights()
    
    return solution
    
if __name__=="__main__":
    import ConfigParser
    import mongoengine
    
    Config = ConfigParser.ConfigParser()
    if Config.read('flight_scraper.cfg')==[]:
        print "Please copy flight_scraper.cfg.example to flight_scraper.cfg"
        raise Exception('Could not read config file')
    
    try:
        host_string=Config.get("mongodb", "host")
        mongoengine.connect(Config.get("mongodb", "name"),host=host_string)
    except ConfigParser.NoOptionError:
        mongoengine.connect(Config.get("mongodb", "name"))
        
    solution = scrape_multi()
