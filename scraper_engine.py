import itascraper
import datetime
import urllib

from mongoengine import *

class Flight(EmbeddedDocument):
    airline = StringField()
    fno = IntField()
    dep_city = StringField()
    arr_city = StringField()
    dep_time = DateTimeField()
    arr_time = DateTimeField()

    def __str__(self):
        return "Flight: %s %s \n%s-%s\n%s  -  %s" % (self.airline, self.fno, self.dep_city, self.arr_city, self.dep_time, self.arr_time)

    def seat_map(self):
        url = "http://www.seatguru.com/findseatmap/findseatmap.php?"
        params = { 'carrier':self.airline,
                    'flightno':self.fno }
        url = url + urllib.urlencode(params)
        return url


class Itinerary(EmbeddedDocument):
    flights = ListField(EmbeddedDocumentField(Flight))
    price = StringField()
    
    def set_stop(conn_flight):
        return None


class Solution(Document):
    query_date = DateTimeField(default=datetime.datetime.utcnow(), required=True)
    engine = StringField(required=True)
    origin = StringField(max_length=100, required=True)
    depart_date = DateTimeField()
    destination = StringField(max_length=100, required=True)
    return_date = DateTimeField()
    min_price = StringField(required=False)
    itineraries = ListField(EmbeddedDocumentField(Itinerary))
