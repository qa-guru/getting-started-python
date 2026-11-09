import os
from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

ARTIFACTS_DIR = Path(__file__).parent / "artifacts"

DEFAULT_BASE_URL = "https://niffler.qa.guru"
DEFAULT_TIMEOUT_S = 10
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

SUPPORTED_BROWSERS = ("chrome", "firefox")
BROWSER_ALIASES = {"chromium": "chrome"}


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=os.getenv("BROWSER", "chrome"),
        choices=["chrome", "firefox", "chromium"],
        help="Browser: chrome | firefox ('chromium' is accepted as an alias for chrome)",
    )
    parser.addoption(
        "--bversion",
        action="store",
        default=os.getenv("BROWSER_VERSION", ""),
        help="Browser version label (passed as browserVersion capability in remote mode)",
    )


@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    name = pytestconfig.getoption("--browser").lower()
    return BROWSER_ALIASES.get(name, name)


@pytest.fixture(scope="session")
def browser_version(pytestconfig):
    return pytestconfig.getoption("--bversion")


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", DEFAULT_BASE_URL).rstrip("/")


@pytest.fixture(scope="session")
def headless():
    return os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")


def _build_options(browser_name, headless, browser_version):
    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        for arg in (
            f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ):
            options.add_argument(arg)
    else:
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        options.add_argument(f"-width={WINDOW_WIDTH}")
        options.add_argument(f"-height={WINDOW_HEIGHT}")
    if browser_version:
        options.browser_version = browser_version
    return options


@pytest.fixture
def driver(browser_name, browser_version, headless, base_url):
    options = _build_options(browser_name, headless, browser_version)

    remote_url = os.getenv("SELENIUM_REMOTE_URL", "").strip()
    remote_requested = os.getenv("SELENIUM_REMOTE", "").lower() in ("1", "true", "yes")

    if remote_url:
        drv = webdriver.Remote(command_executor=remote_url.rstrip("/"), options=options)
    elif remote_requested:
        pytest.fail(
            "Remote mode requested (SELENIUM_REMOTE=true) but SELENIUM_REMOTE_URL is not set. "
            "Provide the Selenium Grid/Selenoid URL, e.g. http://selenoid-host:4444/wd/hub."
        )
    elif browser_name == "chrome":
        drv = webdriver.Chrome(options=options)
    else:
        drv = webdriver.Firefox(options=options)

    try:
        drv.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    except Exception:
        pass
    drv.base_url = base_url
    yield drv
    drv.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, DEFAULT_TIMEOUT_S)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call" or not report.failed:
        return

    drv = item.funcargs.get("driver")
    if drv is None:
        return

    ARTIFACTS_DIR.mkdir(exist_ok=True)
    name = item.name.replace("/", "_")
    try:
        screenshot = drv.get_screenshot_as_png()
        (ARTIFACTS_DIR / f"{name}.png").write_bytes(screenshot)
        allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass
    try:
        source = drv.page_source
        (ARTIFACTS_DIR / f"{name}.html").write_text(source, encoding="utf-8")
        allure.attach(source, name="page_source", attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass
