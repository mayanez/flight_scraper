flight_scraper
===============

This is a quick script that I reversed engineered in order to poll ITA Matrix Airfare Search. It is still a bit rough around the edges as I try to clean it up. The ultimate goal of this is for me to monitor usage on flight fares for certain days of the weeks for multiple weeks and have it alert me on good deals. I'll eventually add some cool graphics and charts and build myself a dashboard that I can then use to display on a picture frame or something. Anyways, I hope someone else out there finds this useful.

The ITA Matrix Airfare Search is a great tool so I suggest you go check it out here: http://matrix.itasoftware.com/

#Dependencies#
* Requests (http://docs.python-requests.org/)
* MongoDB (http://www.mongodb.org/)
* Flask (http://flask.pocoo.org/)
* python-dateutil (http://labix.org/python-dateutil)
* Google Vizualizations API (https://code.google.com/p/google-visualization-python/)

#TO-DO#
* Get # of available seats left on flight at time of search. 
* Add support for non-direct flights
* Calendar automated search support.
* Command Line Interface
* Backtest after enough data is gathered.

* Add more Search Engine Scrapers
* Add price forecasting from Kayak & Bing
* Output reminders kayak style:
	* http://www.kayak.com/images/sample-alerts.gif
* Stylize WebApp for reporting/Dashboard

