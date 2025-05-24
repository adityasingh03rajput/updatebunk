from flask import Flask, request, jsonify
import time
import threading
from collections import defaultdict

app = Flask(__name__)

# Store attendance data
attendance_data = defaultdict(dict)
# Store connected clients
connected_clients = {
    'students': {},
    'teachers': {}
}

@app.route("/ping", methods=["POST"])
def ping():
    """Handle client heartbeats"""
    data = request.json
    client_type = data.get('type')
    username = data.get('username')
    
    if client_type and username:
        connected_clients[client_type][username] = time.time()
        return {"status": "ok"}, 200
    return {"error": "Invalid data"}, 400

@app.route("/attendance", methods=["POST"])
def update_attendance():
    """Update attendance status"""
    data = request.json
    username = data.get('username')
    status = data.get('status')
    
    if username and status:
        attendance_data['students'][username] = status
        # Broadcast update to all teachers
        broadcast_attendance()
        return {"status": "updated"}, 200
    return {"error": "Missing data"}, 400

@app.route("/get_attendance", methods=["GET"])
def get_attendance():
    """Get current attendance data"""
    return jsonify(attendance_data['students'])

def broadcast_attendance():
    """Send attendance updates to all connected teachers"""
    data = {"action": "update_attendance", "data": attendance_data['students']}
    for teacher in list(connected_clients['teachers'].keys()):
        try:
            # In a real implementation, we'd send this to the teacher's socket
            pass
        except:
            # Remove disconnected teachers
            connected_clients['teachers'].pop(teacher, None)

def cleanup_clients():
    """Periodically clean up disconnected clients"""
    while True:
        current_time = time.time()
        for client_type in ['students', 'teachers']:
            for username, last_seen in list(connected_clients[client_type].items()):
                if current_time - last_seen > 60:  # 1 minute timeout
                    connected_clients[client_type].pop(username, None)
        time.sleep(30)

if __name__ == "__main__":
    # Start cleanup thread
    threading.Thread(target=cleanup_clients, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
