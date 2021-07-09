# This class is responsible for talking to the Google Sheet.
import os
import requests

SHEET_LINK = os.environ.get("SHEET_LINK")


class DataManager:
    def __init__(self):
        self.destination_data = []

    def get_flight_data(self):
        response = requests.get(url=SHEET_LINK)
        response.raise_for_status()
        return response.json()["prices"]

    def update_flight_data(self):
        for city in self.destination_data:
            endpoint = f"{SHEET_LINK}/{city['id']}"
            sheet_params = {
                "price": {
                    "iataCode": city["iataCode"],
                }
            }

            response = requests.put(url=endpoint, json=sheet_params)
            print(response)
