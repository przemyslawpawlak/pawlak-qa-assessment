import pytest
from playwright.sync_api import Page, expect

APP_URL = "http://localhost:9000/index.html"

def app_frame(page: Page):
    """The app UI is two iframes deep: #outerFrame (vf-container) -> #appFrame (app)."""
    return page.frame_locator("#outerFrame").frame_locator("#appFrame")

@pytest.fixture
def data_issues(page: Page):
    """Fresh load -> dismiss welcome modal -> open the Data Issues grid.
    Returns the app frame once the grid has rendered."""
    page.goto(APP_URL)
    page.get_by_role("button", name="Got it").click()            # top-page modal
    app = app_frame(page)
    app.get_by_role("button", name="Review & Fix Issues").click()
    # Cards render after app.html's randomDelay(500, 5000); wait for the grid to appear.
    expect(app.locator(".issue-card").first).to_be_visible(timeout=10000)
    return app