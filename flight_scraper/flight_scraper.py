from scrapers.solution_model import Solution, SeatQuery
from engines.ita_matrix.driver import ItaMatrixDriver


class FlightScraper(object):

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

    def search_flights(self):
        ita_driver = ItaMatrixDriver(origin=self.__origin, destination=self.__destination, depart_date=self.__depart_date, return_date=self.__return_date)
        return ita_driver.build_solutions()

    def solutions(self):
        """
        Returns a Solution object from MongoDB
        """
        return Solution.objects(depart_date=self.__depart_date, return_date=self.__return_date, origin=self.__origin, destination=self.__destination)

    def itineraries(self, flights_to_match):
        results = list()
        solutions = self.get_solutions()

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


