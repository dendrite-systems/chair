from flask import Flask, Response, request, jsonify
import os, time
import cv2
from flask_cors import CORS
import threading, queue
import base64

from lm.lm_utils import start_agent_prompt_file_response_thread

video_save_dir = 'video_cache'

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

# Ensure the directory exists
os.makedirs(video_save_dir, exist_ok=True)

@app.route('/upload_video', methods=['POST'])
def upload_video():
    # Check if the request contains a file
    if 'video' not in request.files and 'video_base64' not in request.json:
        return jsonify({"error": "No video file provided"}), 400
    
    # Generate a timestamped filename
    timestamp = int(time.time())
    filename = f"{timestamp}.mp4"
    file_path = os.path.join(video_save_dir, filename)
    
    if 'video' in request.files:
        video_file = request.files['video']
        # Save the video
        video_file.save(file_path)
    elif 'video_base64' in request.json:
        video_base64 = request.json['video_base64']
        video_data = base64.b64decode(video_base64)
        with open(file_path, 'wb') as f:
            f.write(video_data)
    else:
        return jsonify({"error": "No video file provided"}), 400
    
    # Start a thread that will prompt the agent with a file response
    start_agent_prompt_file_response_thread(filename, file_path)
    
    return jsonify({"message": "Video uploaded successfully", "filename": filename}), 200


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
