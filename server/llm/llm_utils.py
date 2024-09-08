import base64
import json
import threading
import logging

from db.db import create_script
from llm.api_client import GeminiAPIClient
from llm.prompts import CODE_PROMPT, ANNOTATE_PROMPT
from llm.parse_utils import (
    extract_python_code,
    extract_name_and_description,
)
import pprint

gemini_api_client = GeminiAPIClient()

logger = logging.getLogger(__name__)


def create_dendrite_script_from_video(file_name, file_path):
    def agent_prompt_file_response():
        logger.info(f"Starting script generation for file: {file_name}")

        logger.info("Converting video file to base64")
        with open(file_path, "rb") as video_file:
            recording_base64 = base64.b64encode(video_file.read()).decode("utf-8")

        logger.info("Requesting code generation from Gemini API")
        response = gemini_api_client.get_prompt_response_with_file(
            CODE_PROMPT, file_name, file_path
        )

        code = extract_python_code(response)
        if code is None:
            logger.error("Failed to generate code")
            return

        logger.info("Generated code:")
        print(code)

        annotate_prompt = ANNOTATE_PROMPT.replace("{{SCRIPT}}", code)
        res = gemini_api_client.get_response(annotate_prompt)

        logger.info("Extracting name and description from annotation")
        code_annotations = extract_name_and_description(res)
        if code_annotations is None:
            logger.error("Failed to generate name and description")
            return

        logger.info("Annotation response:")
        pprint.pprint(code_annotations, indent=4, width=100)

        # Save the generated script to the database
        logger.info("Saving generated script to database")
        script = create_script(
            name=code_annotations["name"],
            description=code_annotations["description"],
            script=code,
            input_json_schema=json.dumps(code_annotations["input_json_schema"]),
            output_json_schema=json.dumps(code_annotations["output_json_schema"]),
            user_id="AI_GENERATED",
            recording_base64=recording_base64,
            author="AI Generated",
            version="1.0",
        )

        logger.info(
            f"Script '{script.name}' saved to database with ID: {script.script_id}"
        )
        return script

    logger.info("Starting script generation in a new thread")
    thread = threading.Thread(target=agent_prompt_file_response)
    thread.start()
