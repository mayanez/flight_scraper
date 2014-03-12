from dateutil.rrule import *
from dateutil.parser import *



def search_seats(origin, dest, dep_date):
    """ TODO: Refactor """
    #dep_date = dep_date.strftime("%Y-%m-%d")
    #print "Searching %s -> %s : %s" % (origin, dest, dep_date)
    raise NotImplementedError('search_seats needs to be implemented')

def generate_date_pairs(frequency, weekdays, start_date, until_date):

    until_date = until_date.strftime('%m-%d-%Y')

    dates = list(rrule(frequency, byweekday=weekdays, dtstart=start_date, until=parse(until_date)))

    date_pairs = list()

    i = 1
    for d in dates:
        #For first date in pair - DEPARTURE DATE
        if (i%2 != 0):
            p = list()
            p.append(d)
        #For second date in pair - RETURN DATE
        else:
            p.append(d)
            date_pairs.append(p)
        i += 1

    return date_pairs

def get_prices_by_query_dates(flight_scraper):
        """ Returns a dict of all queried prices and query_dates for the depart_date & return_date. """
        result = dict()
        solutions = flight_scraper.solutions()

        for sol in solutions:
            query_date = sol.query_date
            min_price = float(sol.min_price[3:]) #gets rid of USD in string

            if (not result.has_key(query_date)):
                prices = list()
                prices.append(min_price)
                result[query_date] = prices
            else:
                result[query_date].append(min_price)

        return result
def get_total_seat_availability(origin, dest, date):
    """ TODO: Refactor """

    #seat_availability = dict()
    #seat_query = get_seats(origin, dest, date)
    #
    #for query in seat_query:
    #    flights = query.flights
    #
    #    for flight in flights:
    #        seats = flight.seats
    #        for seat in seats:
    #            if (not seat_availability.has_key(query.query_date)):
    #                seat_availability[query.query_date] = seat.availability
    #            else:
    #                seat_availability[query.query_date] += seat.availability
    #
    #return seat_availability
    pass

def get_min_price_itinerary(itineraries):

    return min(itineraries, key=lambda x: x.price)


















