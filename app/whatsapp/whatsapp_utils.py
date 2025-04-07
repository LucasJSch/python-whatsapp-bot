import logging
from flask import current_app, jsonify
import json
import requests

from .whatsapp_parser import WhatsAppParser
from .adolfo_perchas import AdolfoPerchasInteraction

def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient):
    """Generate a WhatsApp interactive button menu"""
    return json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": "Welcome! How can I assist you?"},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "prices", "title": "💰 List of Prices"}},
                    {"type": "reply", "reply": {"id": "hours", "title": "🕒 Opening Hours"}},
                    {"type": "reply", "reply": {"id": "human", "title": "👨‍💼 Talk with a Human"}}
                ]
            }
        }
    })

def get_text_message_input_menu(recipient):
    return json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": "Welcome! How can I assist you?"},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "prices", "title": "💰 List of Prices"}},
                    {"type": "reply", "reply": {"id": "hours", "title": "🕒 Opening Hours"}},
                    {"type": "reply", "reply": {"id": "human", "title": "👨‍💼 Talk with a Human"}}
                ]
            }
        }
    })


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_whatsapp_message_adolfo_perchas(body):
    adolfo_perchas = AdolfoPerchasInteraction()
    adolfo_perchas.process_message(body)


def process_whatsapp_message(body):
    parsed_data = WhatsAppParser(body)
    
    wa_id = parsed_data.get_id()
    print("wa_id:", wa_id)
    name = parsed_data.get_name()
    print("name:", name)
    message = parsed_data.get_messages()[0]
    print("message:", message)
    #button_id = parsed_data.get_button_reply_id()
    #response = process_whatsapp_message_adolfo_perchas(body)

    data = get_text_message_input_menu(current_app.config["RECIPIENT_WAID"])

    send_message(data)

