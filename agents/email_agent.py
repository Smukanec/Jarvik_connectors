
import imaplib

def connect(config):
    try:
        mail = imaplib.IMAP4_SSL(config["server"], config["port"]) if config["ssl"] else imaplib.IMAP4(config["server"], config["port"])
        mail.login(config["user"], config["password"])
        mail.select("inbox")
        result, data = mail.search(None, "ALL")
        count = len(data[0].split())
        mail.logout()
        return f"✅ Připojeno k e-mailu {config['user']}. Počet zpráv ve schránce: {count}"
    except Exception as e:
        return f"❌ Chyba při připojení: {e}"
