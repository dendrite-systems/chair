# import dendrite_sdk
# import os
# from dotenv import load_dotenv


# class PythonSandbox:
#     def __init__(self):
#         # Load environment variables from .env file
#         load_dotenv("server/.env")

#         self.globals = {
#             "dendrite_sdk": dendrite_sdk,
#             "os": os,
#         }

#         # Explicitly load required environment variables
#         env_vars = [
#             "OPENAI_API_KEY",
#             "ANTHROPIC_API_KEY",
#             "BROWSERBASE_API_KEY",
#             "BROWSERBASE_CONNECTION_URI",
#             "BROWSERBASE_PROJECT_ID",
#             "DENDRITE_API_KEY",
#         ]

#         for var in env_vars:
#             value = os.getenv(var)
#             if value:
#                 self.globals[var] = value
#             else:
#                 print(f"Warning: {var} not found in environment variables")

#         # Set Dendrite API key
#         if "DENDRITE_API_KEY" in self.globals:
#             dendrite_sdk.api_key = self.globals["DENDRITE_API_KEY"]

#     def execute_with_output(self, code):
#         output = []

#         def _print(*args, **kwargs):
#             output.append(" ".join(map(str, args)))

#         try:
#             self.globals["print"] = _print
#             exec(code, self.globals)
#             return "\n".join(output)
#         except Exception as e:
#             return f"Error: {str(e)}"


# # # Example usage
# # if __name__ == "__main__":
# #     sandbox = PythonSandbox()

# #     # Test with allowed module
# #     result = sandbox.execute_with_output(
# #         """
# # import asyncio
# # from dendrite_sdk import DendriteBrowser

# # async def get_wishlist_count():
# #     async with DendriteBrowser() as browser:
# #         page = await browser.goto("https://fishards.com")
# #         await page.scroll(0, 300)  # Scroll down by 300 pixels
# #         wishlist_count = await page.ask("What is the current wishlist count on this page?")
# #         print(wishlist_count.return_data)

# # asyncio.run(get_wishlist_count())
# # """
# #     )
# #     print(result)

# #     # Test with any module (no restrictions)
# #     result = sandbox.execute_with_output(
# #         """
# # import os
# # print("Current working directory:", os.getcwd())
# # """
# #     )
# #     print(result)
