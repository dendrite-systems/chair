import threading, random, time

from lm.api import ConversationAgent
from lm.constants import INITIAL_PROMPT, NULL_INPUT, IDLE_RESPONSE_TIME, SLEEP_DURATION 

agent = ConversationAgent()
 
def start_agent_prompt_file_response_thread(file_name, file_path):
    # Start a thread that will prompt the agent with a file response
    def agent_prompt_file_response():
        print("Prompting agent with file response")
        response = agent.get_prompt_response_with_file(INITIAL_PROMPT, file_name, file_path)
        print(response)
    thread = threading.Thread(target=agent_prompt_file_response)
    thread.start()

if __name__ == "__main__":
    pass