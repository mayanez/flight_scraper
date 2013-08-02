import os
import time
import datetime

from flask import Flask, render_template, send_from_directory
from scraper_utils import *
from datetime import *
from mongoengine import *

#----------------------------------------
# Utilities
#----------------------------------------

def generate_table():


	TODAY = date.today()
	weekdays = (FR,SU)
	until_date = datetime.strptime('12-01-2013', '%m-%d-%Y')
	date_pairs = generate_date_pairs(DAILY, weekdays, TODAY, until_date)
	data = list()
	for d in date_pairs:
		result= get_all_prices_for_date_pair(d)
		for r in result:
			for p in result[r]:
				v = [d[0].isoformat(), d[1].isoformat(), r, p]
				data.append(v)
	return data

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)

connect('flight_scraper')

app.config.update(
    DEBUG = True,
)

#----------------------------------------
# controllers
#----------------------------------------
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.route("/")
def index():
	return render_template('flights.html', data=generate_table())

#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


