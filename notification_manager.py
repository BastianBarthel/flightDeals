# This class is responsible for sending notifications with the deal flight details.
import os
from twilio.rest import Client

ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
PHONE_NUMBER_FROM = os.environ.get("PHONE_NUMBER_FROM")
PHONE_NUMBER_TO = os.environ.get("PHONE_NUMBER_TO")


class NotificationManager:
    def send_sms(self, price, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date):
        text = f"{origin_city}({origin_airport} to {destination_city}({destination_airport} for {price}€. {out_date} to {return_date})"
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages \
            .create(
            body=text,
            from_=PHONE_NUMBER_FROM,
            to=PHONE_NUMBER_TO
        )
