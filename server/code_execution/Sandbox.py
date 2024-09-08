import dendrite_sdk
import os
from dotenv import load_dotenv


class PythonSandbox:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv("server/.env")

        self.globals = {
            "dendrite_sdk": dendrite_sdk,
            "os": os,
        }

        # Explicitly load required environment variables
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
            else:
                print(f"Warning: {var} not found in environment variables")

    def execute_with_output(self, code):
        output = []

        def _print(*args, **kwargs):
            output.append(" ".join(map(str, args)))

        try:
            self.globals["print"] = _print
            exec(code, self.globals)
            return "\n".join(output)
        except Exception as e:
            return f"Error: {str(e)}"
