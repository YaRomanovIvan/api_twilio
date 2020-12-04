import os
import time
import requests

from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()
token = os.getenv("VK_TOKEN")


def get_status(user_id):
    params = {
        "METHOD_NAME": "users.get",
        "access_token": os.getenv("VK_TOKEN"),
        "v": "5.92",
        "user_ids": user_id,
        "fields": "online",
    }
    response = requests.post("https://api.vk.com/method/users.get", params=params)
    return response.json()["response"][0]["online"]


def sms_sender(sms_text):
    account_sid = os.getenv("account_sid")
    auth_token = os.getenv("auth_token")
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=sms_text,
        from_=os.getenv("twilio_number"),
        to=os.getenv("to_number"),
    )
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f"{vk_id} сейчас онлайн!")
            break
        time.sleep(5)
