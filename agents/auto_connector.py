
import json
import os
import shlex
import base64
import uuid
import logging
from agents import email_agent, calendar_agent

logging.basicConfig(level=logging.INFO)

# Map service types to handler callables
SERVICE_REGISTRY = {
    "email": lambda cfg: email_agent.connect(cfg),
    "calendar": lambda cfg: calendar_agent.list_events(cfg),
}

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
    lower_msg = message.lower()
    if "imap" in lower_msg or "email" in lower_msg or "e-mail" in lower_msg:
        config["type"] = "email"
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
    elif "calendar" in lower_msg or "kalendar" in lower_msg or "kalendář" in lower_msg:
        config["type"] = "calendar"
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
    service_type = config.get("type")
    handler = SERVICE_REGISTRY.get(service_type)
    if not handler:
        return "Nepodporovaný typ služby."

    password = config.pop("password", None)
    if password:
        secret_id = store_password(password)
        logging.info("%s password stored with id %s", service_type, secret_id)
        config["password_id"] = secret_id

    os.makedirs("config", exist_ok=True)
    with open("config/connections.json", "w") as f:
        json.dump(config, f, indent=2)

    kwargs = {**config, "password": password} if password is not None else config
    return handler(kwargs)
