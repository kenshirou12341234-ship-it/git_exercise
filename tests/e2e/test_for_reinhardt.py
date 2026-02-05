import os
import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

@pytest.mark.e2e
def test_for_reinhardt_page_has_text(page: Page):
    """Check that 'A Tribute...' text is visible somewhere on the page."""
    page.goto(f"{BASE_URL}/for_reinhardt/")
    expect(page.locator("body")).to_contain_text("A Tribute to the Great Jazz Guitarist")


@pytest.mark.e2e
def test_for_reinhardt_page_has_paragraph(page: Page):
    """Check that the page contains the expected paragraph text."""
    page.goto(f"{BASE_URL}/for_reinhardt/")
    expect(page.locator("body")).to_contain_text("From those who take the first step in learning with aspiration.")


@pytest.mark.e2e
def test_for_reinhardt_page_does_not_show_beginning_text(page: Page):
    """Check that '最初の一歩です。' is NOT visible on the page."""
    page.goto(f"{BASE_URL}/for_reinhardt/")
    expect(page.locator("body")).not_to_contain_text("最初の一歩です。")
