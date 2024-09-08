import threading, random, time

from lm.api import ConversationAgent
from lm.constants import CODE_PROMPT, ANNOTATE_PROMPT
from server.lm.parse_code_output import parse_code_output, extract_name_and_description

agent = ConversationAgent()


def start_agent_prompt_file_response_thread(file_name, file_path):
    # Start a thread that will prompt the agent with a file response
    def agent_prompt_file_response():
        print("Prompting agent with file response")
        response = agent.get_prompt_response_with_file(
            CODE_PROMPT, file_name, file_path
        )
        code = parse_code_output(response)

        annotate_prompt = ANNOTATE_PROMPT.replace("{{SCRIPT}}", code)
        res = agent.get_response(annotate_prompt)
        name_and_description = extract_name_and_description(res)

        res = {
            "name": name_and_description["name"],
            "description": name_and_description["description"],
            "code": code,
        }
        print(res)
        return res

    thread = threading.Thread(target=agent_prompt_file_response)
    thread.start()


if __name__ == "__main__":
    pass
