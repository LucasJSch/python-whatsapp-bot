import logging
from flask import current_app, jsonify
import json
import requests

# from app.services.openai_service import generate_response
import re


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input_text(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

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

def get_text_message_input_menu(recipient, text=""):
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


def generate_response(response):
    # Return text in uppercase
    return response.upper()


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        #print("request")
        #print(url)
        #print(data)
        #print(headers)
        #print("response")
        #print(response)  # 10 seconds timeout as an example
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


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    # TODO: implement custom function here
    response = generate_response(message_body)

    # OpenAI Integration
    # response = generate_response(message_body, wa_id, name)
    # response = process_text_for_whatsapp(response)

    data = get_text_message_input_menu(current_app.config["RECIPIENT_WAID"], response)
    send_message(data)

    # print(body)
#
    #wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
#
    ## Check if the message is an interactive button response
    #if "button" in body["entry"][0]["changes"][0]["value"]["messages"][0]:
    #    button_id = body["entry"][0]["changes"][0]["value"]["messages"][0]["button"]["payload"]
#
    #    if button_id == "prices":
    #        response = "Here is our price list:\n- Coffee: $3\n- Tea: $2\n- Sandwich: $5"
    #    elif button_id == "hours":
    #        response = "Our opening hours are:\n🕒 Mon-Fri: 8 AM - 8 PM\n🕒 Sat-Sun: 9 AM - 6 PM"
    #    elif button_id == "human":
    #        response = "Please wait while we connect you to a human agent..."
    #    else:
    #        response = "Sorry, I didn't understand that."
#
    #else:
    #    # If it's a normal text message, send the menu
    #    response = "Welcome! How can I assist you?\nPlease select an option from the menu."
#
    #if "button" not in body["entry"][0]["changes"][0]["value"]["messages"][0]:
    #    data = get_text_message_input(wa_id) 
    #else:
    #    data = get_text_message_input(wa_id, response)
    #send_message(data)


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
