import os
import mongoengine

from dateutil.rrule import DAILY
from datetime import datetime
from flask import Flask, render_template, send_from_directory, request
from flight_scraper.flight_scraper import FlightScraper
from flight_scraper.utils.graph import graph_prices
from flight_scraper.utils.scraper import generate_date_pairs, search_seats

#----------------------------------------
# Utilities
#----------------------------------------


#----------------------------------------
# initialization
#----------------------------------------
app = Flask(__name__)

mongoengine.connect('flight_scraper')

app.config.update(
    DEBUG = True,
)

flight_scraper = FlightScraper()

#----------------------------------------
# controllers
#----------------------------------------
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/flight/query", methods=['GET'])
def flight_query():
    origin = request.args.get('origin')
    dest = request.args.get('dest')
    freq = request.args.get('freq')
    start_date = request.args.get('start_date')
    until_date = request.args.get('until_date')
    weekdays = request.args.getlist('weekdays')


    start_date = datetime.strptime(start_date, '%m-%d-%Y')
    until_date = datetime.strptime(until_date, '%m-%d-%Y')
    weekdays = map(int, weekdays)

    #Can probably use dateutils parser for this.
    if freq == "DAILY":
        freq=DAILY

    date_pairs = generate_date_pairs(freq, weekdays, start_date, until_date)

    result = list()

    flight_scraper.origin = origin
    flight_scraper.destination = dest

    for d in date_pairs:
        flight_scraper.depart_date = d[0]
        flight_scraper.return_date = d[1]
        v = [d[0].isoformat(), d[1].isoformat(), flight_scraper.search_flights()]
        result.append(v)

    return render_template('query.html', result=result)

@app.route("/seat/query", methods=['GET'])
def seat_query():
    """
        TODO: Refactor
    """
    #origin = request.args.get('origin')
    #dest = request.args.get('dest')
    #dept = request.args.get('dept')
    #
    #dept = datetime.strptime(dept, '%m-%d-%Y')
    #
    #return render_template('seats.html', flights=search_seats(origin, dest, dept))

@app.route("/graph", methods=['GET'])
def graph_flights():
    origin = request.args.get('origin')
    dest = request.args.get('dest')
    dept = request.args.get('dept')
    ret = request.args.get('ret')

    dept = datetime.strptime(dept, '%m-%d-%Y')
    ret = datetime.strptime(ret, '%m-%d-%Y')

    flight_scraper.origin = origin
    flight_scraper.destination = dest
    flight_scraper.depart_date = dept
    flight_scraper.return_date = ret

    solutions = flight_scraper.solutions()

    length = len(solutions)
    return render_template('graph.html', json_obj=graph_prices(flight_scraper), solutions=solutions, lengthSol=length)

@app.route("/graph_seats", methods=['GET'])
def graph_2():
    """
        TODO: Refactor
    """
    #origin = request.args.get('origin')
    #dest = request.args.get('dest')
    #dept = request.args.get('dept')
    #ret = request.args.get('ret')
    #
    #dept = datetime.strptime(dept, '%m-%d-%Y')
    #ret = datetime.strptime(ret, '%m-%d-%Y')
    #
    #return render_template('graph_seats.html', json_obj=graph_seats(origin, dest, dept))
#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5454))
    app.run(host='0.0.0.0', port=port)


