# Public Cyber Consent Research Demo

This is the consent-based research demo with:
- explicit location permission
- explicit camera permission
- one still camera snapshot after consent
- IP address, timestamp, user agent and optional location
- protected sender dashboard using HTTP Basic Authentication
- in-memory storage only

## Local

```bash
python -m pip install -r requirements.txt
python app.py
```

Recipient: http://127.0.0.1:5000/
Dashboard: http://127.0.0.1:5000/dashboard

For local dashboard auth, set:
```bat
set SENDER_USER=admin
set SENDER_PASSWORD=choose-a-password
python app.py
```

## Render deployment

Render can deploy Flask with:
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

Set environment variables in Render:
- `SENDER_USER` = your dashboard username
- `SENDER_PASSWORD` = a strong dashboard password
- `PYTHON_VERSION` = `3.13.0` or another supported 3.13 release

Do not publish the dashboard password in GitHub.

The public service uses HTTPS supplied by the hosting provider. Camera/location permission still requires the participant to explicitly approve the browser prompts.

## Data and privacy

Use only with authorized participants who have been clearly told what is collected. IP addresses and precise location can be sensitive personal data. The demo stores events in memory and therefore loses them when the service restarts/redeploys. Do not use this storage model for production research records without adding appropriate security, retention, access control, and privacy measures.
