import sys
import os
from dotenv import load_dotenv
import logging


def load_configurations(app):
    #load_dotenv()
    app.config["ACCESS_TOKEN"] = "EAAQawGS7qxYBO8KD0U1E5qvFLZC94aqNEmV6AXjfPnajIB5uxNCpjzgxmUZCqZCcs3qvBes4gp3vJ7Be0jC6nhOfLkHsoxj2idHvLPlK3DyihijjX7Uy1UtFvxm6dRtYCKRrnadYEQSeWZBSAXXZCixaIB77JqsNYejg1fMicZAk4qUJTa2K0lz17KZAGicFKWWB20BWwx5R1PnXJesPCy5Pmm9"
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
