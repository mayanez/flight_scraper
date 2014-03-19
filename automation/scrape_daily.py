#!/usr/local/bin/python
import ConfigParser
import datetime
import logging
from mongoengine import *
from dateutil.rrule import *
from flight_scraper.flight_scraper import FlightScraper
from flight_scraper.utils.scraper import generate_date_pairs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
Config = ConfigParser.ConfigParser()
Config.read('scrape_daily.cfg')

def bidirectional_search(origin, dest, until_date):
    """ Sample Script for automation."""

    #Initialize FlightScraper
    flight_scraper = FlightScraper()

    MO, TU, WE, TH, FR, SA, SU = tuple(range(7))

    #Dates to search
    weekdays_1 = (FR,SU)
    weekdays_2 = (FR,MO)
    start_date = __get_start_date()

    #Generates depart_date & return_date pairs in that order from start_date to util_date
    date_pairs_1 = generate_date_pairs(DAILY, weekdays_1, start_date, until_date)
    date_pairs_2 = generate_date_pairs(DAILY, weekdays_2, start_date, until_date)

    #Search 1
    for d in date_pairs_1:
        flight_scraper.origin = origin
        flight_scraper.destination = dest
        flight_scraper.depart_date = d[0]
        flight_scraper.return_date = d[1]

        flight_scraper.search_flights()

    #Search 2
    for d in date_pairs_2:
        flight_scraper.origin = dest
        flight_scraper.destination = origin
        flight_scraper.depart_date = d[0]
        flight_scraper.return_date = d[1]

        flight_scraper.search_flights()

def __get_start_date():

    TODAY = datetime.date.today()
    start_date = TODAY

    if (TODAY.weekday() == SA or TODAY.weekday() == SU):
        start_date = TODAY + datetime.timedelta(days=2)

    if (TODAY.weekday() == MO):
        start_date = TODAY + datetime.timedelta(days=1)

    return start_date

if __name__ == '__main__':
    #Connect to MongoDB
    connect(Config.get("mongodb", "name"))

    origin = "SEA"
    dest = "PDX"

    try:
        logger.info("Started at %s" % (datetime.datetime.utcnow()))
        bidirectional_search(origin, dest, datetime.datetime.strptime(Config.get("dates", "end"), "%m-%d-%Y"))
    except Exception, e:
        logger.error(e)
        pass

    logger.info("Ended at %s" % (datetime.datetime.utcnow()))