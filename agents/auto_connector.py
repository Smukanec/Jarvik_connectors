
import json
import os
import shlex
import base64
import uuid
import logging
from agents import email_agent

logging.basicConfig(level=logging.INFO)

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


def store_password(password: str) -> str:
    """Store password in secrets file and return identifier."""
    os.makedirs("secrets", exist_ok=True)
    path = os.path.join("secrets", "secrets.json")
    try:
        with open(path) as f:
            secrets = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        secrets = {}

    secret_id = str(uuid.uuid4())
    secrets[secret_id] = base64.b64encode(password.encode()).decode()
    with open(path, "w") as f:
        json.dump(secrets, f, indent=2)
    return secret_id


def handle_message(message):
    config = parse_connection_request(message)
    if config.get("type") == "imap":
        password = config.pop("password", None)
        if password:
            secret_id = store_password(password)
            logging.info("IMAP password stored with id %s", secret_id)
            config["password_id"] = secret_id

        os.makedirs("config", exist_ok=True)
        with open("config/connections.json", "w") as f:
            json.dump(config, f, indent=2)

        return email_agent.connect({**config, "password": password} if password else config)
    return "Nepodporovaný typ služby."
