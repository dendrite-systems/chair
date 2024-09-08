import os
from openai import OpenAI

from lm.tts import _TTS

client = OpenAI()

OpenAI.api_key = os.environ["OPENAI_API_KEY"]

class ConversationAgent:
    def __init__(self):
        self.conversation = []
        self.max_conversation_length = 10
        self.tts = _TTS()
        
    def os_say(self, text):
        os.system("say " + text)

    def clean_print(self, text):
        # remove starting and ending blank characters and quotes
        text.content = text.content.strip().strip('"')
        print(text.content)

    def forget_old_conversation(self):
        message_delete_count = len(self.conversation) - self.max_conversation_length
        # not delete system prompts
        i = 0
        while message_delete_count > 0 and i < len(self.conversation):
            if not self.conversation[i]["is_system_prompt"]:
                self.conversation.pop(i)
                message_delete_count -= 1
            else:
                i += 1
        print("cleaned conversation")

    def process_result(self, result, save=True, is_system_prompt = False, pronounce=False):
        msg = result.choices[0].message
        self.clean_print(msg)
        if save:
            self.conversation.append({
                'role': msg.role,
                'content': msg.content,
                'is_system_prompt': is_system_prompt
            })
            self.forget_old_conversation()
            
        if pronounce:
            # pronounce the message
            # self.os_say(msg.content)
            self.tts.say(msg.content)
        return msg.content

    def make_message(self, message, is_system_prompt, role="user"):
        return {"role": role, "content": message, "is_system_prompt": is_system_prompt}

    def get_response(self, message, is_system_prompt = False, pronounce=False):
        self.conversation.append(self.make_message(message, is_system_prompt))
        completion = client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=self.conversation,
        )
        return self.process_result(completion, is_system_prompt, pronounce=pronounce)

    def save_conversation(self, filename="output.txt"):
        with open(filename, "w") as f:
            for msg in self.conversation:
                f.write(msg["role"] + ": " + msg["content"] + "\n")

if __name__ == "__main__":
    conversation = []
    cnt = 1
    while cnt > 0:
        user_input = input("You: ")
        response = get_response(user_input, conversation)
        cnt -= 1

    print("Conversation ended.")
    print("Conversation:", conversation)