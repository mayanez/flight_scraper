import mongoengine
import smtplib
from datetime import datetime

def send_email(user, password, from_addr, to_addr, subject, msg):
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(user, password)

    senddate=datetime.strftime(datetime.now(), '%Y-%m-%d')

    formatted_message = "Date: %s\r\nFrom: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n %s" % (senddate, from_addr, to_addr, subject, msg)
    server.sendmail(from_addr, to_addr, formatted_message)
    server.quit()

def send_alert(email, origin, destination, dept_date, ret_date, flights):
    """ TODO: Refactor """
    #get_min_price_itinerary(get_itineraries("SEA", "JFK", datetime.strptime("12-13-2013", "%m-%d-%Y"), datetime.strptime("12-15-2013", "%m-%d-%Y"), set([Flight(airline="DL", fno="1542")])))

if __name__ == '__main__':
    mongoengine.connect('flight_scraper')
    print send_alert(None, None, None, None, None, None)