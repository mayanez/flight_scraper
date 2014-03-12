from flight_scraper.solution_model import Solution, CalendarSolution, SeatQuery
from engines.ita_matrix.driver import ItaMatrixDriver, CalendarItaMatrixDriver


class FlightScraper(object):
    
    def __init__(self, origin, destination, depart_date, return_date, 
                 max_stops=0, day_range=None, airlines=None):
        self.origin         =   origin
        self.destination    =   destination
        self.depart_date    =   depart_date
        self.return_date    =   return_date
        self.day_range      =   day_range
        self.max_stops      =   max_stops
        self.airlines       =   airlines

    def search_flights(self):
        ita_driver = ItaMatrixDriver(self.origin, self.destination, self.depart_date, self.return_date)
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

if __name__=="__main__":
    
    from datetime import date
    scraper =   FlightScraper('BWI', 'MSP', date(2014, 6, 1), date(2014, 6, 6))
    flights =   scraper.search_flights()
    
    a = 1
