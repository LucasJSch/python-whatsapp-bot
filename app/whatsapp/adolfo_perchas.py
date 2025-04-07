from typing import List, Dict, Any
from .whatsapp_parser import WhatsAppParser
from app.scheink.state_machine import StateMachine
import json


def build_button_json(id: str, text: str) -> Dict[str, Any]:
    return {"type": "reply", "reply": {"id": id, "title": text}},

class AdolfoPerchasInteraction:
    """ Class to handle interactions with Adolfo Perchas store. """
    def __init__(self):
        self.json_state_machine = '''
        {
            "initial_state": "presentation",
            "presentation": {
                "message": ["Welcome to Adolfo Perchas! How can I help you?"],
                "menu": {
                    "prices": {"message": ["Prices"], "next_state": ["prices"]},
                    "hours": {"message": ["Hours"], "next_state": ["hours"]},
                    "human_interaction": {"message": ["Talk to a human"], "next_state": ["human_interaction"]},
                    "what_else": {"message": ["En que mas puedo ayudarte?"], "next_state": ["state_a"]}
                }
            },
            "prices": {
                "message": ["Here are the prices: \n Percha de madera: $10  \n Percha de plastico: $5"],
                "menu": {
                    "back": {"message": ["Back"], "next_state": ["presentation"]}
                }
            },
            "hours": {
                "message": ["🕒 Mon-Fri: 8 AM - 8 PM", "🕒 Sat-Sun: 9 AM - 6 PM"],
                "menu": {
                    "back": {"message": ["Back"], "next_state": ["presentation"]}
                }
            },
            "human_interaction": {
                "message": ["Please wait while we connect you to a human agent..."],
                "menu": {
                    "back": {"message": ["Back"], "next_state": ["presentation"]}
                }
            }
        }
        '''
        self.state_machine = StateMachine(self.json_state_machine)

    def process_message(self, body):
        parsed_data = WhatsAppParser(body)
        button_id = parsed_data.get_button_reply_id()
        return self.generate_json_response(button_id)

    def get_template_menu_json(self):
        buttons = []
        for button_id, button_text in self.main_menu.items():
            buttons.append(build_button_json(button_id, button_text))
        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "type": "interactive",
            "interactive": {
                "type": "button",
                "action": {
                    "buttons": []
                }
            }
        }
    
    def generate_json_response(self, button_id, wa_id):
            msg = self.state_machine.get_message(button_id)
            menu = self.get_menu(button_id)
            response_text = msg["message"]
            text_message = self.get_text_message_input_text(wa_id, response_text)
            return text_message
    
            menu_message = self.get_template_menu_json()
            menu_message["to"] = wa_id
            return menu_message

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