import itascraper


def run_itascraper(origin, dest, dep_date, return_date):
	print "\tRunning ITA Matrix Scraper..."
	itascraper.set_origin(origin)
	itascraper.set_destination(dest)
	itascraper.set_dep_date(dep_date)
	itascraper.set_return_date(return_date)
	return itascraper.build_solutions()


def run_all(origin, dest, dep_date, return_date):
	print "Running All Scrapers..."
	return run_itascraper(origin, dest, dep_date, return_date)