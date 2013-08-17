#!/bin/zsh

import time
import dateutil
import calendar
import datetime
from .. import controller 
from ..solution_model import *

from datetime import *
from dateutil.rrule import *
from dateutil.parser import *


def search_flights(origin, dest, date_pair):
    """
    Searches all engines for queried flight.
    """
    dep_date = date_pair[0].strftime("%Y-%m-%d")
    return_date = date_pair[1].strftime("%Y-%m-%d")

    print "Searching %s -> %s : %s to %s" % (origin, dest, dep_date, return_date)
    return controller.run_all(origin, dest, dep_date, return_date)


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


















