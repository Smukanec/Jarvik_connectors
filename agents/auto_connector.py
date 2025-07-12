
import json
import os
import shlex
from agents import email_agent

try:
    import validators
except Exception:  # pragma: no cover - fallback for environments without package
    import re

    class validators:  # type: ignore
        @staticmethod
        def domain(value: str) -> bool:
            return bool(re.match(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", value))

def parse_connection_request(message):
    config = {}
    if "imap" in message.lower():
        config["type"] = "imap"
        tokens = [t.strip(",.;") for t in shlex.split(message)]

        config["ssl"] = any(t.lower() == "ssl" for t in tokens)

        # locate email address
        config["user"] = next((t for t in tokens if "@" in t), None)

        # extract password "heslo je <pwd>"
        try:
            idx = next(i for i, t in enumerate(tokens) if t.lower() == "heslo")
            if tokens[idx + 1].lower() == "je":
                config["password"] = tokens[idx + 2].strip(",.;")
        except (StopIteration, IndexError):
            pass

        # extract server hostname
        try:
            idx = next(i for i, t in enumerate(tokens) if t.lower() == "server")
            host = tokens[idx + 1]
            if validators.domain(host):
                config["server"] = host
        except (StopIteration, IndexError):
            pass

        # extract and validate port
        port = None
        try:
            idx = next(i for i, t in enumerate(tokens) if t.lower() == "port")
            port_candidate = int(tokens[idx + 1])
            if 1 <= port_candidate <= 65535:
                port = port_candidate
        except (StopIteration, IndexError, ValueError):
            pass
        config["port"] = port if port is not None else 993
    return config


def handle_message(message):
    config = parse_connection_request(message)
    if config.get("type") == "imap":
        os.makedirs("config", exist_ok=True)
        with open("config/connections.json", "w") as f:
            json.dump(config, f, indent=2)
        return email_agent.connect(config)
    return "Nepodporovaný typ služby."
