from flask import Flask, request, jsonify
import time

app = Flask(__name__)


devices = {}
alerts = {}

@app.route("/ping", methods=["POST"])
def ping():
    ip = request.remote_addr
    devices[ip] = time.time()
    return {"status": "pong"}, 200

@app.route("/devices", methods=["GET"])
def get_devices():
    now = time.time()
    active_devices = [ip for ip, t in devices.items() if now - t < 60]
    return jsonify(active_devices)

@app.route("/send_alert", methods=["POST"])
def send_alert():
    data = request.json
    target_ip = data.get("target_ip")
    message = data.get("message", "ALERT!")
    if target_ip:
        alerts[target_ip] = message
        return {"status": "alert queued"}, 200
    return {"error": "Missing target_ip"}, 400

@app.route("/get_alert", methods=["GET"])
def get_alert():
    ip = request.remote_addr
    alert = alerts.pop(ip, None)
    return jsonify({"alert": alert}) if alert else jsonify({})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
