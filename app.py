from flask import Flask, request, jsonify, send_from_directory, Response
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from datetime import datetime, timezone
import threading

app = Flask(__name__, static_folder="public", static_url_path="/public")
app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

events = []
lock = threading.Lock()

def client_ip():
    return request.remote_addr or "unknown"

@app.get("/")
def recipient():
    return send_from_directory("public", "recipient.html")

def dashboard_auth():
    expected_user = os.environ.get("SENDER_USER", "")
    expected_password = os.environ.get("SENDER_PASSWORD", "")
    if not expected_user or not expected_password:
        return False
    auth = request.authorization
    return bool(auth and auth.username == expected_user and auth.password == expected_password)

@app.get("/dashboard")
def dashboard():
    if not dashboard_auth():
        return Response(
            "Dashboard authentication required.",
            401,
            {"WWW-Authenticate": 'Basic realm="Research Dashboard"'}
        )
    return send_from_directory("public", "dashboard.html")

@app.post("/api/consent")
def consent():
    data = request.get_json(silent=True) or {}
    image = data.get("camera_snapshot")
    # Bound the demo payload to avoid accidentally accepting huge uploads.
    if isinstance(image, str) and len(image) > 2_500_000:
        return jsonify({"ok": False, "error": "Snapshot too large"}), 413

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ip": client_ip(),
        "user_agent": request.headers.get("User-Agent", ""),
        "location": data.get("location"),
        "location_permission": bool(data.get("location_permission")),
        "camera_permission": bool(data.get("camera_permission")),
        "camera_snapshot": image if data.get("camera_permission") else None,
    }

    with lock:
        events.append(event)
        del events[:-100]

    return jsonify({"ok": True})

@app.get("/api/events")
def get_events():
    if not dashboard_auth():
        return Response(
            "Dashboard authentication required.",
            401,
            {"WWW-Authenticate": 'Basic realm="Research Dashboard"'}
        )
    with lock:
        return jsonify(events)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
