import sys
import os
from dotenv import load_dotenv
import logging


def load_configurations(app):
    app.config["ACCESS_TOKEN"] = "EAAQawGS7qxYBOznlZASdlHI5BHaCaV6ZAgj2IjAPxZB9TUtK8WAC1l5aBUgKVk9u3ESJUc5kgZAVvGy8rY0UX9C8g8OwJlcn28kOkflvXYAbaphmw0XORQN9dIZA349TXr6c0TyUMTQE1gVKVkyfFDuLfwF7OSd9dIzii6adnbZCRcxKRY756P9i1ZBHZCZBVbt6zbSHXX6yJpjFR4aarssVCSpJI"
    app.config["YOUR_PHONE_NUMBER"] = "589785260887815"
    app.config["APP_ID"] = "1155313532906262"
    app.config["APP_SECRET"] = "997363276fe1222198d4e16c3a7d8206"
    app.config["RECIPIENT_WAID"] = "541166734594"
    app.config["VERSION"] = "v22.0"
    app.config["PHONE_NUMBER_ID"] = "589785260887815"
    app.config["VERIFY_TOKEN"] = "holahola2"


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
