import os
from pathlib import Path

import allure
import pytest
from playwright.sync_api import sync_playwright

ARTIFACTS_DIR = Path(__file__).parent / "artifacts"

DEFAULT_BASE_URL = "https://niffler.qa.guru"
DEFAULT_TIMEOUT_MS = 10_000
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=os.getenv("BROWSER", "chromium"),
        choices=["chromium", "firefox", "webkit"],
        help="Browser engine: chromium | firefox | webkit",
    )
    parser.addoption(
        "--bversion",
        action="store",
        default=os.getenv("BROWSER_VERSION", ""),
        help="Browser version label (informational; playwright uses bundled builds)",
    )


@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return pytestconfig.getoption("--browser")


@pytest.fixture(scope="session")
def browser_version(pytestconfig):
    return pytestconfig.getoption("--bversion")


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", DEFAULT_BASE_URL).rstrip("/")


@pytest.fixture(scope="session")
def headless():
    return os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance, browser_name, headless):
    browser_type = getattr(playwright_instance, browser_name)
    br = browser_type.launch(headless=headless)
    yield br
    br.close()


@pytest.fixture
def context(browser):
    ctx = browser.new_context(viewport={"width": WINDOW_WIDTH, "height": WINDOW_HEIGHT})
    ctx.set_default_timeout(DEFAULT_TIMEOUT_MS)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context, base_url):
    pg = context.new_page()
    pg.base_url = base_url
    yield pg
    pg.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call" or not report.failed:
        return

    pg = item.funcargs.get("page")
    if pg is None:
        return

    ARTIFACTS_DIR.mkdir(exist_ok=True)
    name = item.name.replace("/", "_")
    try:
        screenshot = pg.screenshot(full_page=True)
        (ARTIFACTS_DIR / f"{name}.png").write_bytes(screenshot)
        allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass
    try:
        source = pg.content()
        (ARTIFACTS_DIR / f"{name}.html").write_text(source, encoding="utf-8")
        allure.attach(source, name="page_source", attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass
