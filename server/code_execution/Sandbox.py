import ast
import sys
from io import StringIO


class Sandbox:
    def __init__(self):
        self.globals = {
            "__builtins__": {
                "print": print,
                "len": len,
                "range": range,
                "sum": sum,
                "min": min,
                "max": max,
                "list": list,
                "dict": dict,
                "set": set,
                "int": int,
                "float": float,
                "str": str,
                "bool": bool,
            }
        }

    def check_ast(self, code):
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                raise ValueError("Import statements are not allowed")
            elif isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and func.attr in [
                    "__import__",
                    "eval",
                    "exec",
                ]:
                    raise ValueError(f"Function '{func.attr}' is not allowed")
        return tree

    def run_code(self, code):
        try:
            self.check_ast(code)
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()
            exec(code, self.globals)
            sys.stdout = old_stdout
            return redirected_output.getvalue()
        except Exception as e:
            return f"Error: {str(e)}"


sandbox = Sandbox()
llm_generated_code = """
import asyncio
from dendrite_sdk import DendriteBrowser


async def get_wishlist_count():
    async with DendriteBrowser() as browser:
        page = await browser.goto("https://fishards.com")
        wishlist_count = await page.ask("What is the current wishlist count on this page?")
        print(wishlist_count.return_data)


asyncio.run(get_wishlist_count())
"""

output = sandbox.run_code(llm_generated_code)
print("Sandbox output:", output)
