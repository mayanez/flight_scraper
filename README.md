flight_scraper
===============

This is a quick script that I reversed engineered in order to poll ITA Matrix Airfare Search. It is still a bit rough around the edges as I try to clean it up. The goal is to determine a correlation between seat availability and price fare information to alert me on trends for flight segments. I want to build a cool dashboard in order to feed all this information to me automatically. 

Right now I use ITA Matrix for airfare search & flightstats for seat availability. I'm looking to get information from nome other sites as well in order to get better data. 

The ITA Matrix Airfare Search is a great tool so I suggest you go check it out here: http://matrix.itasoftware.com/
Also checkout Flightstats (https://flightstats.com) its a great site for finding information about tracking. I use it to monitor whether flights are on-time or not.

#Installation#
(build steps)
Copy flight_scraper.cfg.example to flight_scraper.cfg

#Dependencies#
* Requests (http://docs.python-requests.org/)
* MongoDB (http://www.mongodb.org/)
* Flask (http://flask.pocoo.org/)
* python-dateutil (http://labix.org/python-dateutil)
* Google Vizualizations API (https://code.google.com/p/google-visualization-python/)
* PhantomJS (http://phantomjs.org/)
* Selenium (http://docs.seleniumhq.org/)

#TO-DO#
* MapReduce Job to map seat availability to pricing information.
* Integrate with Prediction.io for Analysis.
* Seat map for availability - alert if aisle/window seat becomes available.
* Upgrade list - to track which flights give higher chance of upgrades.
* Add support for non-direct flights
* Calendar automated search support.
* Command Line Interface
* Backtest after enough data is gathered.

* Add more Search Engine Scrapers
* Add price forecasting from Kayak & Bing
* Output reminders kayak style:
	* http://www.kayak.com/images/sample-alerts.gif
* Stylize WebApp for reporting/Dashboard

