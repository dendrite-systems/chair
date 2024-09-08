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
            expected_page="You should be logged in with the instagram feed visible",
        )

        # Use natural language to interact with the page
        first_post = await page.ask("Describe the first post in my feed")
        print("First post description:", first_post.return_data)


asyncio.run(instagram_example())
