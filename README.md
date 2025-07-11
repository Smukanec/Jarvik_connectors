
# Jarvik Connector – Auto Email/Kalendář Agent

Tento modul umožňuje Jarvikovi automaticky zpracovat přirozený text typu:

```
Připoj se na e-mail jiri@firma.cz, server mail.firma.cz, port 993, SSL, heslo je tajne123.
```

## 📦 Obsah

- `agents/auto_connector.py` – hlavní rozhraní, které rozpozná typ služby a vytvoří konfiguraci.
- `agents/email_agent.py` – jednoduchý IMAP klient.
- `config/connections.json` – uložené připojení.
  Soubor je vygenerován při volání `handle_message` a je uložen v adresáři `config/`.
- `secrets/token.json` – připraveno pro případné API tokeny (např. Google Calendar).

## ▶️ Použití

V kódu Jarvika:

```python
from agents import auto_connector
odpoved = auto_connector.handle_message(vstup_uzivatele)
```

## ✅ Funkce

- Automatické rozpoznání e-mailové konfigurace z textu
- Připojení k IMAP schránce
- Výpis počtu zpráv
- Po spočítání zpráv se spojení uzavře
- Uložení připojení

## 📅 Plánované

- Google Calendar agent
- SMTP odpovědi

---

## 🗓️ Kalendářový Agent (`calendar_agent.py`)

- `list_events()` – vrací simulované události
- `create_event(title, start_time, duration)` – vytvoří novou (simulovanou) událost

Poznámka: Toto je zatím lokální mock. Napojení na Google Calendar API je plánované přes `google-api-python-client`.
