import engines.itamatrix as itamatrix


def run_itamatrix(origin, dest, dep_date, return_date):
	print "\tRunning ITA Matrix Scraper..."
	itamatrix.set_origin(origin)
	itamatrix.set_destination(dest)
	itamatrix.set_dep_date(dep_date)
	itamatrix.set_return_date(return_date)
	return itamatrix.build_solutions()


def run_all(origin, dest, dep_date, return_date):
	print "Running All Scrapers..."
	return run_itamatrix(origin, dest, dep_date, return_date)