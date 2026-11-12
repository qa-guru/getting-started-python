from pathlib import Path

import pytest
from dotenv import load_dotenv

from infrastructure.browser.factory import create_driver
from infrastructure.reporting.artifacts import save_failure_artifacts
from settings import Settings, load_settings

pytest_plugins = ["test_data.fixtures"]

load_dotenv()

ARTIFACTS_DIR = Path(__file__).parent / "artifacts"


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        choices=["chrome", "firefox", "chromium"],
        help="Browser: chrome | firefox ('chromium' is accepted as an alias for chrome). "
             "Priority: CLI > BROWSER env > chrome",
    )
    parser.addoption(
        "--bversion",
        action="store",
        default=None,
        help="Browser version label (passed as browserVersion capability in remote mode). "
             "Priority: CLI > BROWSER_VERSION env",
    )


@pytest.fixture(scope="session")
def settings(pytestconfig) -> Settings:
    return load_settings(
        browser_option=pytestconfig.getoption("--browser"),
        bversion_option=pytestconfig.getoption("--bversion"),
    )


@pytest.fixture
def driver(settings):
    drv = create_driver(settings)
    try:
        yield drv
    finally:
        drv.quit()


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

    save_failure_artifacts(drv, ARTIFACTS_DIR, item.name.replace("/", "_"))
