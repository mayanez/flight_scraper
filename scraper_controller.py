import itascraper
from mongoengine import *


def run_itascraper():
	itascraper.build_solutions()

def run_all():
	run_itascraper()
	
if __name__ == '__main__':
	connect('flight_scraper')
	run_all()