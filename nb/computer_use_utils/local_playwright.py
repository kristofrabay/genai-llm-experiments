from playwright.sync_api import Browser, Page
from computer_use_utils.base_playwright import BasePlaywrightComputer


class LocalPlaywrightComputer(BasePlaywrightComputer):
    """Launches a local Chromium instance using Playwright."""

    def __init__(self, headless: bool = False):
        super().__init__()
        self.headless = headless

    def _get_browser_and_page(self) -> tuple[Browser, Page]:
        width, height = self.dimensions
        launch_args = [f"--window-size={width},{height}", "--disable-extensions", "--disable-file-system"]
        browser = self._playwright.chromium.launch(
            chromium_sandbox=True,
            headless=self.headless,
            args=launch_args,
            env={}
        )
        page = browser.new_page()
        page.set_viewport_size({"width": width, "height": height})
        page.goto("https://bing.com")
        return browser, page