import os, time
import google.generativeai as genai
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class GeminiModel():
    def __init__(self):
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        self.file_dict = {}
        
    def upload_file_from_path(self, name, path):
        print(f"Uploading file...")
        file = genai.upload_file(path=path)
        print(f"Completed upload: {file.uri}")
        
        self.file_dict[name] = file
    
    def get_query_completion(self, prompt):
        print(f"Querying model with prompt: {prompt}")
        response = self.model.generate_content(prompt)
        print(f"Response: {response}")
        return response
    
    def get_query_completion_from_file(self, prompt, file_name):
        print(f"Querying model with prompt: {prompt} and file: {file_name}")
        if file_name not in self.file_dict:
            raise ValueError(f"File {file_name} not found in file dictionary")
        self.wait_for_upload(file_name)
        file = self.file_dict[file_name]
        response = self.model.generate_content([file, prompt])
        print(f"Response: {response.text}")
        return response
    
    def wait_for_upload(self, file_name):
        file = self.file_dict[file_name]
        while file.state.name == "PROCESSING":
            print('.', end='')
            time.sleep(2)
            file = genai.get_file(file.name)

        if file.state.name == "FAILED":
            raise ValueError(file.state.name)
        self.file_dict[file_name] = file
    
    
if __name__ == "__main__":
    model = GeminiModel()
    model.get_query_completion("Hello, how are you?")