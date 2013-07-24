#!/bin/zsh

import time
import dateutil
import calendar

from scraper_controller import run_all
from datetime import *
from mongoengine import *
from dateutil.rrule import *
from dateutil.parser import *


#Controller to generate sample data to begin analysis
if __name__ == '__main__':
	connect('flight_scraper')
	origin = "SEA"
	dest = "NYC"

	TODAY = date.today()

	dates = list(rrule(DAILY, byweekday=(FR,SU), dtstart=TODAY, until=parse("20131201T000000")))

	date_pairs = list()
	

	i = 1
	for d in dates:
		#For first date in pair
		if (i%2 != 0):
			p = list()
			p.append(d)
		#For second date in pair
		else:
			p.append(d)
			date_pairs.append(p)
		i += 1


	for d in dates:

		dep_date = d[0]
		return_date = d[1]

		print "Searching %s -> %s : %s to %s" % (origin, dest, dep_date, return_date)
		run_all(origin, dest, dep_date, return_date)

		print "Searching %s -> %s : %s to %s" % (origin, dest, return_date, dep_date)
		run_all(origin, dest, return_date, dep_date)