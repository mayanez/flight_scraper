#!/usr/local/bin/python
import datetime
import logging
from mongoengine import *
from dateutil.rrule import *
from scrapers.utils.scraper import generate_date_pairs, search_flights, search_seats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_daily_both_ways(origin, dest, until_date):
    """ Sample Script for automation."""
    connect('flight_scraper')


    MO, TU, WE, TH, FR, SA, SU = tuple(range(7))
    weekdays_1 = (FR,SU)
    weekdays_2 = (FR,MO)
    TODAY = datetime.date.today()
    start_date = TODAY

    if (TODAY.weekday() == SA or TODAY.weekday() == SU):
        start_date = TODAY + datetime.timedelta(days=2)

    if (TODAY.weekday() == MO):
        start_date = TODAY + datetime.timedelta(days=1)

    date_pairs_1 = generate_date_pairs(DAILY, weekdays_1, start_date, until_date)
    date_pairs_2 = generate_date_pairs(DAILY, weekdays_2, start_date, until_date)

    for d in date_pairs_1:
        search_flights(origin, dest, d)
        search_seats(origin, dest, d[0])
        search_seats(dest, origin, d[1])


    for d in date_pairs_2:
        search_flights(dest, origin, d)
        search_seats(dest, origin, d[0])
        search_seats(origin, dest, d[1])


if __name__ == '__main__':
    origin = "SEA"
    dest = "PDX"
    try:
        logger.info("Started at %s" % (datetime.datetime.utcnow()))
        scrape_daily_both_ways(origin, dest, datetime.datetime.strptime("1-1-2014", "%m-%d-%Y"))
    except Exception, e:
        logger.error(e)
        pass

    logger.info("Ended at %s" % (datetime.datetime.utcnow()))