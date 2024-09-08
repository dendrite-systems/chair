import threading
import os
import json
import logging

from db.db import create_script
from llm.api_client import GeminiAPIClient
from llm.prompts import CODE_PROMPT, ANNOTATE_PROMPT
from llm.parse_utils import (
    extract_python_code,
    extract_name_and_description,
)

gemini_api_client = GeminiAPIClient()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_dendrite_script_from_video(file_name, file_path):
    def agent_prompt_file_response():
        logger.info(f"Starting script generation for file: {file_name}")

        logger.info("Requesting code generation from Gemini API")
        response = gemini_api_client.get_prompt_response_with_file(
            CODE_PROMPT, file_name, file_path
        )

        logger.info("Extracting Python code from response")
        code = extract_python_code(response)
        if code is None:
            logger.error("Failed to generate code")
            return

        logger.info("Requesting script annotation from Gemini API")
        annotate_prompt = ANNOTATE_PROMPT.replace("{{SCRIPT}}", code)
        res = gemini_api_client.get_response(annotate_prompt)

        logger.info("Extracting name and description from annotation")
        name_and_description = extract_name_and_description(res)
        if name_and_description is None:
            logger.error("Failed to generate name and description")
            return

        # Save the generated script to the database
        logger.info("Saving generated script to database")
        script = create_script(
            name=name_and_description["name"],
            script=code,
            user_id="AI_GENERATED",  # You might want to change this
            description=name_and_description["description"],
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
