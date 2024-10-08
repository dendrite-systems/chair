import pprint
import asyncio
import threading
from flask import Flask, request, jsonify
import os, time
from flask_cors import CORS
import base64
from io import BytesIO

# from llm.llm_utils import create_dendrite_script_from_video
from db.db import get_all_scripts, get_script_by_id

video_save_dir = "video_cache"
script_dir = "parsed_scripts"

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


# @app.route("/upload_video", methods=["POST"])
# def upload_video():
#     app.logger.info("Received video upload request")

#     # Check if the request contains a file
#     if "video" not in request.files and (
#         not request.json or "video_base64" not in request.json
#     ):
#         app.logger.error("No video file provided in the request")
#         return jsonify({"error": "No video file provided"}), 400

#     # Generate a timestamped filename
#     timestamp = int(time.time())
#     filename = f"{timestamp}.mp4"
#     file_path = os.path.join(video_save_dir, filename)
#     app.logger.info(f"Generated filename: {filename}")

#     if "video" in request.files:
#         app.logger.info("Processing video file from request.files")
#         video_file = request.files["video"]
#         video_file.save(file_path)
#         app.logger.info(f"Video file saved to {file_path}")
#     elif request.json and "video_base64" in request.json:
#         app.logger.info("Processing base64 encoded video from request.json")
#         video_base64 = request.json["video_base64"]
#         video_data = base64.b64decode(video_base64)
#         with open(file_path, "wb") as f:
#             f.write(video_data)
#         app.logger.info(f"Decoded base64 video saved to {file_path}")
#     else:
#         app.logger.error("No video file provided in the request")
#         return jsonify({"error": "No video file provided"}), 400

#     # Start a thread that will prompt the agent with a file response
#     app.logger.info(f"Creating Dendrite script from video: {filename}")
#     create_dendrite_script_from_video(filename, file_path)
#     app.logger.debug(f"Request JSON: {request.json}")

#     app.logger.info("Video upload process completed successfully")
#     return (
#         jsonify({"message": "Video uploaded successfully", "filename": filename}),
#         200,
#     )


@app.route("/get_scripts_list", methods=["GET"])
def get_scripts_list():
    scripts = get_all_scripts().data
    # print(scripts[0].keys())
    script_list = [
        {
            "id": script["script_id"], 
            "name": script["name"],
            "author": script["author"],
            "script": script["script"],
            "version": script["version"],
            "description": script["description"],
            "input_json_schema": script["input_json_schema"],
            "output_json_schema": script["output_json_schema"]
        } for script in scripts
    ]
    return jsonify({"scripts": script_list}), 200


@app.route("/get_script_details", methods=["GET"])
def get_script_details():
    script_id = request.args.get("script_id")
    if script_id is None:
        return jsonify({"error": "Script ID not provided"}), 400

    script = get_script_by_id(script_id)
    if script is None:
        return jsonify({"error": "Script not found"}), 404

    return (
        jsonify(
            {
                "script_id": script.script_id,
                "name": script.name,
                "description": script.description,
                "code": script.script,
                "author": script.author,
                "version": script.version,
                "input_json_schema": script.input_json_schema,
                "output_json_schema": script.output_json_schema,
            }
        ),
        200,
    )


@app.route("/run_script", methods=["POST"])
def run_script():
    if not request.json:
        return jsonify({"error": "Invalid JSON data"}), 400
    script_id = request.json.get("script_id")
    if not script_id:
        return jsonify({"error": "Script ID not provided"}), 400

    script = get_script_by_id(script_id)
    if script is None:
        return jsonify({"error": "Script not found"}), 404

    print("Input:", request.json.get("input_data", {}))
    
    return jsonify({"ok": "ok"}), 200

# Example default route to check server is running
@app.route("/")
def index():
    return "Flask server is running!"


def handle_exit():
    global stop_events
    print("Exiting")
    for stop_event in stop_events:
        stop_event.set()

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5050, debug=False)

        # print("Starting upload test")
        # test_upload_video()
        # test_run_script(
        #     script_id="47a8a887-d212-47c3-9b5d-7c19a1597667",
        #     input_data={"github_url": "https://github.com/charlesmaddock/fishards"},
        # )
    except Exception as e:
        print(e)
    finally:
        handle_exit()
