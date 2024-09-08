from openai import OpenAI
import os
OpenAI.api_key = os.environ["OPENAI_API_KEY"]

class GPTModel():
    def __init__(self):
        self.client = OpenAI()
        pass
    
    def get_conversation_completion(self, conversation):
        result = self.client.chat.completions.create(
                        model="chatgpt-4o-latest",
                        messages=self.conversation,
                    )
        return result