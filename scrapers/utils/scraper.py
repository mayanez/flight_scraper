#!/bin/zsh

import time
import dateutil
import calendar
import datetime
from scrapers import controller


from datetime import *
from dateutil.rrule import *
from dateutil.parser import *
from scrapers.solution_model import Solution, SeatQuery, Flight


def search_flights(origin, dest, date_pair):
    """
    Searches all engines for queried flight.
    """
    dep_date = date_pair[0].strftime("%Y-%m-%d")
    return_date = date_pair[1].strftime("%Y-%m-%d")

    print "Searching %s -> %s : %s to %s" % (origin, dest, dep_date, return_date)
    return controller.run_all_flight_scrapers(origin, dest, dep_date, return_date)

def search_seats(origin, dest, dep_date):
    dep_date = dep_date.strftime("%Y-%m-%d")
    print "Searching %s -> %s : %s" % (origin, dest, dep_date)
    return controller.run_all_seat_scrapers(origin, dest, dep_date)

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

def get_solutions(origin, dest, date_pair):
    """
    Returns a Solution object from MongoDB
    """
    solutions = Solution.objects(depart_date=date_pair[0], return_date=date_pair[1], origin=origin, destination=dest)

    return solutions

def get_all_prices_for_date_pair(origin, dest, date_pair):
    """
    Returns a dict of all queried prices and query_dates for a specific date_pair.
    """
    result = dict()
    solutions = get_solutions(origin, dest, date_pair)

    for sol in solutions:
        query_date = sol.query_date
        min_price = float(sol.min_price[3:]) #get rid of USD
        
        if (not result.has_key(query_date)):
            prices = list()
            prices.append(min_price)
            result[query_date] = prices
        else:
            result[query_date].append(min_price) 

    return result

def get_seats(origin, dest, date):

    seat_query = SeatQuery.objects(flights__dep_city=origin, flights__arr_city=dest, flights__dep_time=date)

    return seat_query

def get_total_seat_availability(origin, dest, date):

    seat_availability = dict()
    seat_query = get_seats(origin, dest, date)

    for query in seat_query:
        flights = query.flights

        for flight in flights:
            seats = flight.seats
            for seat in seats:
                if (not seat_availability.has_key(query.query_date)):
                    seat_availability[query.query_date] = seat.availability
                else:
                    seat_availability[query.query_date] += seat.availability

    return seat_availability

def get_itineraries(origin, dest, dep_date, ret_date, match_flights):

    results = list()
    solutions = get_solutions(origin, dest, [dep_date, ret_date])

    for sol in solutions:
        itineraries = sol.itineraries
        for itinerary in itineraries:
            flights = set(itinerary.flights)
            matched = flights.intersection(match_flights)
            if len(matched) > 0:
                results.append(itinerary)

    return results

def get_min_price_itinerary(itineraries):

    return min(itineraries, key=lambda x: x.price)


















