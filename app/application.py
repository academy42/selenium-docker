from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy

from config import settings


class Application:

    __driver = None
    """Драйвер селениума"""

    def __init__(self):
        dc = self.__setup_chrome_capabilities()
        self.__driver = webdriver.Remote(
            command_executor=f"http://{settings.HUB_HOST}:4444/wd/hub",
            desired_capabilities=dc,
            keep_alive=True,
        )

    @staticmethod
    def __setup_chrome_capabilities() -> DesiredCapabilities:
        """Настраиваем доп фичи хрома"""
        desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        desired_capabilities["browserName"] = "chrome"
        desired_capabilities["javascriptEnabled"] = True

        proxy_cfg = {
            "httpProxy": settings.PROXY,
            "sslProxy": settings.PROXY,
        }
        proxy = Proxy(raw=proxy_cfg)
        proxy.add_to_capabilities(desired_capabilities)

        return desired_capabilities

    @property
    def driver(self):
        """Геттер драйвера"""
        return self.__driver

    def get_page(self, url):
        """Пример для получения HTML странички"""
        self.driver.get(url)
        return self.driver.page_source
