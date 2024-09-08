import dendrite_sdk
import os
import json
from dotenv import load_dotenv
import asyncio
import logging


class PythonSandbox:
    def __init__(self):
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

        load_dotenv("server/.env")
        self.logger.info("Environment variables loaded")

        self.globals = {
            "dendrite_sdk": dendrite_sdk,
            "os": os,
            "asyncio": asyncio,
        }

        env_vars = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "BROWSERBASE_API_KEY",
            "BROWSERBASE_CONNECTION_URI",
            "BROWSERBASE_PROJECT_ID",
            "DENDRITE_API_KEY",
        ]

        for var in env_vars:
            value = os.getenv(var)
            if value:
                self.globals[var] = value
                self.logger.debug(f"Environment variable {var} loaded")
            else:
                self.logger.warning(f"Environment variable {var} not found")

    def execute_with_input_output(self, code, input_json):
        self.logger.info("Executing code in sandbox")
        output = []

        self.logger.info(f"Code to execute: {code} with input: {input_json}")

        def _print(*args, **kwargs):
            output.append(" ".join(map(str, args)))

        try:
            self.globals["print"] = _print
            self.globals["input_data"] = input_json
            exec(code, self.globals)
            result = self.globals.get("result", None)

            print(f"Code execution completed successfully, results: {result}")
            return {"output": "\n".join(output), "result": result}
        except Exception as e:
            self.logger.error(f"Error during code execution: {str(e)}", exc_info=True)
            return {"error": str(e)}
