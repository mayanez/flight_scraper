import os
import time
import datetime
import scraper_utils
import graph_engine

from flask import Flask, render_template, send_from_directory, request
from scraper_utils import *
from datetime import *
from mongoengine import *
from graph_engine import *
#----------------------------------------
# Utilities
#----------------------------------------


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

@app.route("/graph", methods=['GET'])
def graph():
	origin = request.args.get('origin')
	dest = request.args.get('dest')
	dept = request.args.get('dept')
	ret = request.args.get('ret')

	dept = datetime.strptime(dept, '%m-%d-%Y')
	ret = datetime.strptime(ret, '%m-%d-%Y')

	return render_template('graph.html', json_obj=graph_prices(origin, dest, dept, ret))

#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


