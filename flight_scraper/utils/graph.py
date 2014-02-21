import gviz_api
from flight_scraper.utils.scraper import get_prices_by_query_dates


def graph_prices(flight_scraper):
    """
        This function creates a Google Visualizations DataTable JSON object.
        It is then passed to the Google Visualizations API to be rendered.
    """
    description = {"query_date" : ("datetime", "Query Date"),
                   "min_price" : ("number", "%s to %s" % (flight_scraper.depart_date, flight_scraper.return_date))}

    dates = list()
    dates.append(flight_scraper.depart_date)
    dates.append(flight_scraper.return_date)

    result = get_prices_by_query_dates(flight_scraper)
    data = list()
    for r in result:
        for p in result[r]:
            v = {"query_date" : r, "min_price" : p}
            data.append(v)

    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    return data_table.ToJSon(columns_order=("query_date", "min_price"), order_by="query_date")

def graph_seats(origin, dest, dept_date):
    """ TODO: Refactor """
    #description = {"query_date" : ("datetime", "Query Date"),
    #               "seat_avail" : ("number", "%s" % (dept_date))}
    #
    #seat_query = scraper.get_total_seat_availability(origin, dest, dept_date)
    #data = list()
    #for query_date, avail in seat_query.iteritems():
    #    v = {"query_date" : query_date, "seat_avail" : avail}
    #    data.append(v)
    #
    #data_table = gviz_api.DataTable(description)
    #data_table.LoadData(data)
    #
    #return data_table.ToJSon(columns_order=("query_date", "seat_avail"), order_by="query_date")

