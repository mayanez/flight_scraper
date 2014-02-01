import mongoengine
import datetime

from scrapers.utils.scraper import *

def send_alert(email, origin, destination, dept_date, ret_date, flights):
    return get_min_price_itinerary(get_itineraries("SEA", "JFK", datetime.strptime("12-13-2013", "%m-%d-%Y"), datetime.strptime("12-15-2013", "%m-%d-%Y"), set([Flight(airline="DL", fno="1542")])))

if __name__ == '__main__':
    mongoengine.connect('flight_scraper')
    print send_alert(None, None, None, None, None, None)