# This class is responsible for talking to the Flight Search API.
import os
import requests
from flight_data import FlightData

FLIGHT_ENDPOINT = "http://tequila-api.kiwi.com"
FLIGHT_API_KEY = os.environ.get("TEQUILA_API_KEY")


class FlightSearch:
    def get_iata(self, city):
        flight_headers = {"apikey": FLIGHT_API_KEY}
        flight_params = {
            "term": city,
            "location_types": "city"
        }

        response = requests.get(
            url=f"{FLIGHT_ENDPOINT}/locations/query",
            params=flight_params,
            headers=flight_headers
        )

        response.raise_for_status()
        result = response.json()["locations"]
        return result[0]["code"]

    def get_flights(self, origin_code, destination_code, from_time, to_time):
        flight_headers = {"apikey": FLIGHT_API_KEY}
        flight_params = {
            "fly_from": origin_code,
            "fly_to": destination_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 21,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "locale": "de",
        }

        response = requests.get(
            url=f"{FLIGHT_ENDPOINT}/v2/search",
            params=flight_params,
            headers=flight_headers
        )

        try:
            data = response.json()["data"][0]
        except:
            print(f"No flights found for {destination_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )

        print(f"{flight_data.destination_city}: {flight_data.price}€")
        return flight_data
