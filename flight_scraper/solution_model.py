import datetime
import urllib

from mongoengine import *

class Seat(EmbeddedDocument):
    cabin_code = StringField()
    fare_class = StringField()
    availability = IntField()

    def __str__(self):
        return "cabin: %s fare: %s avail: %s" % (self.cabin_code, self.fare_class, self.availability)

class Flight(EmbeddedDocument):
    airline = StringField()
    fno = IntField()
    dep_city = StringField()
    arr_city = StringField()
    dep_time = DateTimeField()
    arr_time = DateTimeField()
    seats = ListField(EmbeddedDocumentField(Seat))

    def __str__(self):
        return "Flight: %s %s \n%s-%s\n%s  -  %s" % (self.airline, self.fno, self.dep_city, self.arr_city, self.dep_time, self.arr_time)

    def __repr__(self):
        return self.__str__

    def __eq__(self, other):
        return ((self.airline == other.airline) and (self.fno == other.fno))

    def __hash__(self):
        return hash((self.airline, self.fno))

    def seat_map(self):
        url = "http://www.seatguru.com/findseatmap/findseatmap.php?"
        params = { 'carrier':self.airline,
                    'flightno':self.fno,
                     'date':self.dep_time.strftime('%m-%d-%Y') }
        url = url + urllib.urlencode(params)
        return url

class Itinerary(EmbeddedDocument):
    flights = ListField(EmbeddedDocumentField(Flight))
    price = StringField()

    def __str__(self):
        return "Itinerary:\n \tPrice=%s\n \t%s" % (self.price, [str(f) for f in self.flights])

    def set_stop(self, conn_flight):
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

class SeatQuery(Document):
    query_date = DateTimeField(default=datetime.datetime.utcnow(), required=True)
    flights = ListField(EmbeddedDocumentField(Flight))

class TripMinimumPrice(EmbeddedDocument):
    dep_city = StringField()
    arr_city = StringField()
    dep_time = DateTimeField()
    arr_time = DateTimeField()
    price    = StringField()
    
    def __str__(self):
        return 'TripMinimimumPrice: %s->%s\n%s - %s: %s' % (self.dep_city, self.arr_city, self.dep_time, self.arr_time, self.price)
    
    def query(self):
        pass

class CalendarSolution(Document):
    query_date = DateTimeField(default=datetime.datetime.utcnow(), required=True)
    engine = StringField(required=True)
    origin = StringField(max_length=100, required=True)
    destination = StringField(max_length=100, required=True)
    depart_date = DateTimeField()
    return_date = DateTimeField()
    min_price = StringField(required=False)
    trip_prices = ListField(EmbeddedDocumentField(TripMinimumPrice))
