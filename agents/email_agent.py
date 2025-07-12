
import imaplib
from typing import Any, Dict

DEFAULT_TIMEOUT = 10

def connect(config: Dict[str, Any]) -> Dict[str, Any]:
    """Connect to an IMAP server and return connection status."""
    timeout = config.get("timeout", DEFAULT_TIMEOUT)
    cls = imaplib.IMAP4_SSL if config.get("ssl") else imaplib.IMAP4
    try:
        mail = cls(config["server"], config["port"], timeout=timeout)
        mail.login(config["user"], config["password"])
        mail.select("inbox")
        _, data = mail.search(None, "ALL")
        count = len(data[0].split())
        mail.logout()
        return {"status": "ok", "mail_count": count}
    except imaplib.IMAP4.abort as e:
        return {"status": f"abort: {e}", "mail_count": None}
    except imaplib.IMAP4.error as e:
        return {"status": f"error: {e}", "mail_count": None}
    except Exception as e:
        return {"status": f"exception: {e}", "mail_count": None}
