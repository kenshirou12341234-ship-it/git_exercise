import os
import django
import pytest
from playwright.sync_api import Browser, BrowserContext, Page

# Django設定の初期化
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jazz_guitarist_paper.settings')
django.setup()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context arguments."""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720,
        },
    }


@pytest.fixture(scope="function")
def context(browser: Browser, browser_context_args):
    """Create a new browser context for each test."""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Create a new page for each test."""
    page = context.new_page()
    yield page
    page.close()
