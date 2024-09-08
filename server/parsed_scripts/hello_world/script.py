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
