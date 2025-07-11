
import re
import json
from agents import email_agent

def parse_connection_request(message):
    config = {}
    if "imap" in message.lower():
        config["type"] = "imap"
        config["ssl"] = True if "ssl" in message.lower() else False
        config["user"] = extract_field(message, r"([\w\.]+@[\w\.]+)")
        config["password"] = extract_field(message, r"heslo\s+je\s+(\S+)")
        config["server"] = extract_field(message, r"server\s+(\S+)")
        config["port"] = int(extract_field(message, r"port\s+(\d+)") or 993)
    return config

def extract_field(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return None
    try:
        return match.group(1)
    except IndexError:
        return None

def handle_message(message):
    config = parse_connection_request(message)
    if config.get("type") == "imap":
        with open("config/connections.json", "w") as f:
            json.dump(config, f, indent=2)
        return email_agent.connect(config)
    return "Nepodporovaný typ služby."
