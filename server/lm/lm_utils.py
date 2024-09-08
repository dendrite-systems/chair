import threading
import os
import json

from lm.api import GeminiAPIClient
from server.lm.prompts import CODE_PROMPT, ANNOTATE_PROMPT
from server.lm.parse_code_output import (
    extract_python_code,
    extract_name_and_description,
)

gemini_api_client = GeminiAPIClient()


def start_agent_prompt_file_response_thread(file_name, file_path):
    # Start a thread that will prompt the agent with a file response
    def agent_prompt_file_response():
        response = gemini_api_client.get_prompt_response_with_file(
            CODE_PROMPT, file_name, file_path
        )
        code = extract_python_code(response)
        if code is None:
            print("Failed to generate code")
            return

        annotate_prompt = ANNOTATE_PROMPT.replace("{{SCRIPT}}", code)
        res = gemini_api_client.get_response(annotate_prompt)
        name_and_description = extract_name_and_description(res)
        if name_and_description is None:
            print("Failed to generate name and description")
            return

        res = {
            "name": name_and_description["name"],
            "description": name_and_description["description"],
            "code": code,
        }

        # Save the generated script to the parsed_scripts directory
        script_dir = os.path.join("parsed_scripts", res["name"])
        os.makedirs(script_dir, exist_ok=True)

        # Save the script
        with open(os.path.join(script_dir, "script.py"), "w") as f:
            f.write(res["code"])

        # Save the config
        config = {
            "Name": res["name"],
            "Display Name": res["name"].replace("_", " ").title(),
            "Author": "AI Generated",
            "Description": res["description"],
            "Version Number": "1.0",
        }
        with open(os.path.join(script_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=4)

        return res

    thread = threading.Thread(target=agent_prompt_file_response)
    thread.start()


if __name__ == "__main__":
    pass
