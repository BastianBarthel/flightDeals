from data_manager import DataManager
from flight_search import FlightSearch
import datetime

ORIGIN_CODE = "FRA"

data_manager = DataManager()
sheet_data = data_manager.get_flight_data()
flight_search = FlightSearch()

if not sheet_data[0]["iataCode"]:
    for row in sheet_data:
        row["iataCode"] = flight_search.get_iata(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_flight_data()

start_search = datetime.datetime.now() + datetime.timedelta(days=30)
end_search = start_search + datetime.timedelta(days=6*30)

for destination in sheet_data:
    flight = flight_search.get_flights(
        ORIGIN_CODE,
        destination["iataCode"],
        start_search,
        end_search
    )

    try:
        if flight.price < destination["lowestPrice"]:
            from notification_manager import NotificationManager
            notification_manager = NotificationManager()
            notification_manager.send_sms(
                flight.price,
                flight.origin_city,
                flight.origin_airport,
                flight.destination_city,
                flight.destination_airport,
                flight.out_date,
                flight.return_date
            )
    except:
        pass
