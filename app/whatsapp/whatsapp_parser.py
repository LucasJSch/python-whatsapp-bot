from typing import List, Dict, Any

class WhatsAppParser:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.entries = data.get("entry", [])

    def get_phone_number(self) -> str:
        if self.entries:
            return self.entries[0]["changes"][0]["value"]["metadata"]["display_phone_number"]
        return ""
    
    def get_contacts(self) -> List[Dict[str, Any]]:
        if self.entries:
            return self.entries[0]["changes"][0]["value"].get("contacts", [])
        return []
    
    def get_messages(self) -> List[Dict[str, Any]]:
        if self.entries:
            return self.entries[0]["changes"][0]["value"].get("messages", [])
        return []
    
    def get_button_reply_id(self) -> Dict[str, str]:
        messages = self.get_messages()
        if messages and messages[0].get("type") == "interactive":
            return messages[0]["interactive"]["button_reply"]["id"]
        return {}
    
    def get_id(self) -> str:
        """Extracts the ID of the message."""
        contact = self.get_contacts()[0]
        if contact:
            return contact.get("wa_id", "")
        return ""
    
    def get_name(self) -> str:
        """Extracts the name of the contact."""
        return self.get_contacts()[0]["profile"].get("name", "")
    

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WhatsAppWebhookPayload:
    raw: Dict[str, Any]

    @property
    def entry(self) -> Optional[Dict[str, Any]]:
        return self.raw.get("entry", [{}])[0] if self.raw.get("entry") else None

    @property
    def change(self) -> Optional[Dict[str, Any]]:
        return self.entry.get("changes", [{}])[0] if self.entry else None

    @property
    def value(self) -> Optional[Dict[str, Any]]:
        return self.change.get("value", {}) if self.change else None

    @property
    def statuses(self) -> Optional[List[Dict[str, Any]]]:
        return self.value.get("statuses")

    @property
    def messages(self) -> Optional[List[Dict[str, Any]]]:
        return self.value.get("messages")

    @property
    def contacts(self) -> Optional[List[Dict[str, Any]]]:
        return self.value.get("contacts")

    @property
    def metadata(self) -> Optional[Dict[str, Any]]:
        return self.value.get("metadata")

    @property
    def wa_id(self) -> Optional[str]:
        if self.contacts:
            return self.contacts[0].get("wa_id")
        return None
