
import time
import datetime

from scraper_utils import *
from scraper_controller import run_all

from datetime import *
from mongoengine import *

if __name__ == '__main__':
	
	connect('flight_scraper')
	origin = "SEA"
	dest = "NYC"

	TODAY = date.today()
	weekdays = (FR,SU)
	until_date = datetime.strptime('12-01-2013', '%m-%d-%Y')
	date_pairs = generate_date_pairs(DAILY, weekdays, TODAY, until_date)
	
	#Polls search engines
	print "Running..."
	for d in date_pairs:
		search_flights(d, origin, dest)
		search_flights(d, dest, origin)


	# #test 2 - eventually this will be graphed and displayed in webpage, for now CSV
	# # X axis: query_dates
	# # Y axis: prices
	# #output = open("results.csv", "w")
	# date_pair = [datetime.strptime('08-16-2013', '%m-%d-%Y'), datetime.strptime('08-18-2013', '%m-%d-%Y')]
	
	# #result= get_all_prices_for_date_pair(date_pair)
	# for r in result:
	# 	for p in result[r]:
	# 		print "%s, %s" % (r, p)
	# 		#output.write("%s, %s\n" % (r,p))

	# #output.close()