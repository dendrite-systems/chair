from flask import Flask, Response, request, jsonify
import cv2
from flask_cors import CORS
import threading, queue

stop_events = []
threads = {}

app = Flask(__name__)
CORS(app)


def start_threads():
    # start asynchronous threads here
    global stop_events
    global threads
    pass
    
with app.app_context():
    start_threads()

@app.route('/set_control/<control_name>', methods=['POST'])
def set_control(control_name):
    if control_name in control_states:
        set_control_state(control_name, request.json.get('value'))
        print(f"{control_name} set to {control_states[control_name]}")
        return jsonify({"status": "success", "control": control_name, "value": control_states[control_name]})
    else:
        return jsonify({"status": "error", "message": "Invalid control name"}), 400

# Example default route to check server is running
@app.route('/')
def index():
    return "Flask server is running!"

def handle_exit():
    # handle cleanup here
    global stop_events
    print("Exiting")
    cv2.destroyAllWindows()
    for stop_event in stop_events:
        stop_event.set()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5050, debug=False)
    except Exception as e:
        print(e)
    finally:
        handle_exit()
