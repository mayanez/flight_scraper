import itascraper
from mongoengine import *


def run_itascraper(origin, dest, dep_date, return_date):
	print "\tRunning ITA Matrix Scraper..."
	itascraper.set_origin(origin)
	itascraper.set_destination(dest)
	itascraper.set_dep_date(dep_date)
	itascraper.set_return_date(return_date)
	itascraper.build_solutions()

def run_all(origin, dest, dep_date, return_date):
	print "Running All Scrapers..."
	run_itascraper(origin, dest, dep_date, return_date)
	
if __name__ == '__main__':
	connect('flight_scraper')
	origin = "SEA"
	dest = "NYC"
	dep_date = "2013-06-14"
	return_date = "2013-06-16"
	print "Searching %s -> %s : %s to %s" % (origin, dest, dep_date, return_date)
	run_all(origin, dest, dep_date, return_date)