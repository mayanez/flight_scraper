import engines.itamatrix as itamatrix
import engines.flightstats as flightstats

def run_itamatrix(origin, dest, dep_date, return_date):
    print "\tRunning ITA Matrix Scraper..."
    itamatrix.set_origin(origin)
    itamatrix.set_destination(dest)
    itamatrix.set_dep_date(dep_date)
    itamatrix.set_return_date(return_date)
    return itamatrix.build_solutions()

def run_flightstats(origin, dest, dep_date):
    print "\tRunning FlightStats Scraper..."
    flightstats.init()
    flightstats.set_origin(origin)
    flightstats.set_destination(dest)
    flightstats.set_dep_date(dep_date)
    return flightstats.get_seat_availability()

def run_all_flight_scrapers(origin, dest, dep_date, return_date):
    print "Running All Flight Scrapers..."
    return run_itamatrix(origin, dest, dep_date, return_date)

def run_all_seat_scrapers(origin, dest, dep_date):
    print "Running All Seat Scrapers..."
    return run_flightstats(origin, dest, dep_date)