import os
from lm.tts import _TTS
from constants import MODEL_LIBRARY

if MODEL_LIBRARY == "OPENAI":
    from models.gpt import GPTModel
elif MODEL_LIBRARY == "GEMINI":
    from models.gemini import GeminiModel
else:
    raise ValueError("MODEL_LIBRARY must be either 'OPENAI' or 'GEMINI'")


class ConversationAgent:
    def __init__(self):
        self.conversation = []
        self.max_conversation_length = 20
        self.tts = _TTS()
        if MODEL_LIBRARY == "OPENAI":
            self.model = GPTModel()
        else:
            self.model = GeminiModel()

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

    def process_result(
        self, result, save=True, is_system_prompt=False, pronounce=False
    ):
        msg = result.choices[0].message
        self.clean_print(msg)
        if save:
            self.conversation.append(
                {
                    "role": msg.role,
                    "content": msg.content,
                    "is_system_prompt": is_system_prompt,
                }
            )
            self.forget_old_conversation()

        if pronounce:
            self.tts.say(msg.content)
        return msg.content

    def make_message(self, message, is_system_prompt, role="user"):
        return {"role": role, "content": message, "is_system_prompt": is_system_prompt}

    def get_response(
        self, message, is_system_prompt=False, pronounce=False, in_conversation=False
    ):
        if in_conversation:
            self.conversation.append(self.make_message(message, is_system_prompt))
            completion = self.get_conversation_completion()
            return self.process_result(
                completion, is_system_prompt, pronounce=pronounce
            )
        else:
            completion = self.get_query_completion(message)
            return completion.text

    def get_prompt_response_with_file(self, prompt, file_name, file_path):
        self.model.upload_file_from_path(file_name, file_path)
        completion = self.model.get_query_completion_from_file(prompt, file_name)
        return completion.text

    def get_conversation_completion(self):
        result = self.model.get_conversation_completion(self.conversation)
        return result

    def get_query_completion(self, message):
        result = self.model.get_query_completion(message)
        return result

    def save_conversation(self, filename="output.txt"):
        with open(filename, "w") as f:
            for msg in self.conversation:
                f.write(msg["role"] + ": " + msg["content"] + "\n")


if __name__ == "__main__":
    agent = ConversationAgent()
    res = agent.get_prompt_response_with_file(
        "What do you see from the image?", "bus", "bus.jpeg"
    )

    # cnt = 1
    # while cnt > 0:
    #     user_input = input("You: ")
    #     response = agent.get_response(user_input)
    #     cnt -= 1

    # print("Conversation ended.")
    # print("Conversation:", agent.conversation)
