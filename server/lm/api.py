from models.gemini import GeminiModel


class GeminiAPIClient:
    def __init__(self):

        self.model = GeminiModel()

    def clean_print(self, text):
        # remove starting and ending blank characters and quotes
        text.content = text.content.strip().strip('"')
        print(text.content)

    def get_response(self, message):
        completion = self.get_query_completion(message)
        return completion.text

    def get_prompt_response_with_file(
        self, prompt: str, file_name: str, file_path: str
    ) -> str:
        self.model.upload_file_from_path(file_name, file_path)
        completion = self.model.get_query_completion_from_file(prompt, file_name)
        return completion.text

    def get_query_completion(self, message):
        result = self.model.get_query_completion(message)
        return result


if __name__ == "__main__":
    agent = GeminiAPIClient()
    res = agent.get_prompt_response_with_file(
        "What do you see from the image?", "bus", "bus.jpeg"
    )
