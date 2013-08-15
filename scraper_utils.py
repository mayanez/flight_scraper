#!/bin/zsh

import time
import dateutil
import calendar
import datetime

from scraper_controller import run_all
from scraper_engine import *

from datetime import *
from mongoengine import *
from dateutil.rrule import *
from dateutil.parser import *

MO, TU, WE, TH, FR, SA, SU = weekdays = tuple(range(7))

def search_flights(date_pair, origin, dest):

    dep_date = date_pair[0].strftime("%Y-%m-%d")
    return_date = date_pair[1].strftime("%Y-%m-%d")

    print "Searching %s -> %s : %s to %s" % (origin, dest, dep_date, return_date)
    return run_all(origin, dest, dep_date, return_date)


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

#This method returns a dict of all queried prices and query_date for a specific date_pair
def get_all_prices_for_date_pair(origin, dest, date_pair):

    result = dict()
    solutions = Solution.objects(depart_date=date_pair[0], return_date=date_pair[1], origin=origin, destination=dest)

    for sol in solutions:
        query_date = sol.query_date
        min_price = sol.min_price[3:] #get rid of USD
        
        if (not result.has_key(query_date)):
            prices = list()
            prices.append(min_price)
            result[query_date] = prices
        else:
            result[query_date].append(min_price) 

    return result


















