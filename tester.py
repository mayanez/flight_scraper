
import time
import datetime

from scrapers.utils.scraper import *
from scrapers.controller import run_all

from datetime import *
from mongoengine import *


if __name__ == '__main__':
	
	connect('flight_scraper')
	origin = "SEA"
	dest = "NYC"

	TODAY = date.today() - timedelta(days=2)
	weekdays = (FR,SU)
	until_date = datetime.strptime('12-01-2013', '%m-%d-%Y')

	MO, TU, WE, TH, FR, SA, SU = weekdays = tuple(range(7))
	# print TODAY.weekday()
	print TH
	print TODAY
	# if (TODAY.weekday() == TH):
	# 	print "yes"
	date_pairs = generate_date_pairs(DAILY, weekdays, TODAY, until_date)
	

	print "Running..."
	for d in date_pairs:
		search_flights(origin, dest, d)
	# 	#search_flights(d, dest, origin)


	# #test 2 - eventually this will be graphed and displayed in webpage, for now CSV
	# # X axis: query_dates
	# # Y axis: prices
	# output = open("results.csv", "w")
	
	
	# # x = list()
	# data = list()
	# print "Depart, Return, Query, Price"
	# for d in date_pairs:
	# 	result= get_all_prices_for_date_pair(d)
	# 	for r in result:
	# 		for p in result[r]:
	# 			data.append("%s, %s, %s, %s\n" % (d[0], d[1], r, p))
	# 			# x.append(r)
	# 			# y.append(p)
	# 			#output.write("%s, %s, %s, %s\n" % (d[0], d[1], r, p))

	# data = list()
	# data.append(x)
	# data.append(y)
	# G = Scatter(data)
	# G.axes('xy')
	# G.size(500,500)
	# print str(G)
	# output.close()