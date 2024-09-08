MODEL_LIBRARY = "GEMINI"

IDLE_RESPONSE_TIME = 7

CODE_PROMPT = """You are an AI agent that takes a screen recording of a user showing you how to complete an automated task on the web.=======

Your goal is to look at the screen recording and generate a python script that uses the Dendrite SDK. Dendrite is an SDK that uses natural language to automate actions on the web.

Here is an example of how to use the Dendrite SDK:

```python
import asyncio
from dendrite_sdk import DendriteBrowser


async def hello_world():
    # Initate the Dendrite Browser
    async with DendriteBrowser() as browser:

        # Navigate with `goto`, which returns a 'DendritePage' that controls the current page. DendritePage is a wrapper around a Playwright Page.
        page = await browser.goto("https://google.com")

        # Get elements from the current page with `get_element`.
        search_bar = await page.get_element("The search bar")
        
        # Let's enter hello world into the search bar.
        await search_bar.fill("hello world")
        
        # Wait for the search results to have loaded in, we do this to make sure the element will be available.
        await page.wait_for("the search results to have loaded in")

        # Get the video tab to see video results
        video_tab = await page.get_element("The tab for showing video results")
        
        # Click the video tab
        await video_tab.click()

        # Extract all the video URLs.
        urls = await page.extract(
            "Get all the urls of the displayed videos as a list of valid urls as strings"
        )
        
        for url in urls:
            print("url: ", url)


asyncio.run(hello_world())
```

As you can see, it's very easy to extract and interact with elements on the page using natural language.

Here is a more advanced example that uses the dendrite SDK and a OpenAI request to handle semantic requests:

```python
import asyncio
import os
import time
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

from dendrite_sdk import DendriteBrowser


def ai_request(prompt: str):
    openai = OpenAI()
    messages = [ChatCompletionUserMessageParam(role="user", content=prompt)]
    oai_res = openai.chat.completions.create(messages=messages, model="gpt-4o-mini")
    if oai_res.choices[0].message.content:
        return oai_res.choices[0].message.content
    raise Exception("Failed to get successful response from Open AI.")


async def find_recipe(recipe: str, preferences: str):
    async with DendriteBrowser() as dendrite:
        page = await dendrite.goto("https://www.ica.se/recept/")

        close_cookies_button = await page.get_element("The reject cookies button")
        if close_cookies_button:
            await close_cookies_button.click()

        search_bar = await page.get_element("The search bar for searching recipes with placeholder sök ingrediens etc")
        await search_bar.fill(recipe)

        # You can use the playwright keyboard by accessing `page.keyboard`. 
        await page.keyboard.press("Enter")

        await page.wait_for("Wait for the recipies to be loaded")
        # This function will scroll the page to the bottom until there is no scroll left.
        await page.scroll_to_bottom()
        recipes_res = await page.extract(
            "Get all the recipes on the page and return and array of dicts like this {{name: str, time_to_make: str, url_to_recipe: str}}"
        )

        find_recipe_prompt = f'''Here are some recipes:
        
        {{recipes_res.return_data}}
        
        Please output the url of the recipe that best suits these food preferences: {{preferences}}. 
        
        Important: You output should consist of only one valid URL, nothing else, pick the one that best suits my preferences.'''

        url = ai_request(find_recipe_prompt)
        page = await dendrite.goto(url)
        res = await page.ask(
            "Please output a nice, readable string containing the page's recipe that contains a header for ingredients and one for the steps in English.",
            str,
        )

        generated_recipe = res.return_data
        print(
            f"Find recipe took: {time.time() - start_time}. Here is the recipe:\n\n{{generated_recipe}}"
        )
        
        return generated_recipe
```

Finally, let's take a look at authentication.

The Dendrite SDK uses a Chrome extension called Dendrite Vault to securely authenticate websites. This mirrors the access you have in your local browser. Here's how it works:

1. Users install the Dendrite Vault extension in your Chrome browser.
2. Users navigate to the website that they want to authenticate (e.g., Instagram).
3. They use the on the Dendrite Vault extension icon and press "Save authentication session".
4. In your Python script, use await browser.authenticate("domain.com") to apply the saved authentication, to be able to access their account with the script.

This method allows you to automate tasks on websites that require login, without exposing your credentials in the script. The authenticate function retrieves and applies the saved session from Dendrite Vault.

Here's an example of how to authenticate with Instagram:

```python
import asyncio
from dendrite_sdk import DendriteBrowser

async def instagram_example():
    # Initiate the Dendrite Browser
    async with DendriteBrowser() as browser:
        # Authenticate with Instagram
        await browser.authenticate("instagram.com")
        
        # Navigate to Instagram
        page = await browser.goto(
            "https://instagram.com",
            expected_page="You should be logged in with the instagram feed visible"
        )
        
        # Use natural language to interact with the page
        first_post = await page.ask("Describe the first post in my feed")
        print("First post description:", first_post.return_data)


asyncio.run(instagram_example())
```

Now, based of the video recording, you will generate a python script that can be used to automate the task.

Output it in a python code block. like this:

```python
<your script here>
```
"""

ANNOTATE_PROMPT = """Look at the script below and output a json object that contains a name and description for the entire script with backticks. like this:

```json
{{
    "name": "name of the script",
    "description": "description of the script"
}}
```

Here is the script:

```python   
{{SCRIPT}}
```

Output the json now:"""
