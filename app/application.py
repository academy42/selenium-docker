import time

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy
from seleniumwire import webdriver

from config import settings


class Application:

    __driver = None
    """Драйвер селениума"""

    def __init__(self):
        time.sleep(5)
        dc = self.__setup_chrome_capabilities()

        option = webdriver.ChromeOptions()
        option.add_argument("--proxy-server={}".format("app:3000"))

        self.__driver = webdriver.Remote(
            command_executor=f"http://{settings.HUB_HOST}:4444/wd/hub",
            options=option,
            seleniumwire_options={
                "auto_config": False,
                "addr": "0.0.0.0",
                "port": 3000,
                "proxy": {
                    "http": "http://63eqtpf95:e92vhr2j5y@dc3.ibaldr.ru:8120",
                },
            },
            desired_capabilities=dc,
            keep_alive=True,
        )

    @staticmethod
    def __setup_browser_proxy() -> Proxy:
        """Настраиваем прокси"""
        proxy_cfg = {"httpProxy": settings.PROXY, "sslProxy": settings.PROXY}
        proxy = Proxy(raw=proxy_cfg)
        return proxy

    @staticmethod
    def __setup_chrome_capabilities() -> DesiredCapabilities:
        """Настраиваем доп фичи хрома"""
        desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        desired_capabilities["browserName"] = "chrome"
        desired_capabilities["javascriptEnabled"] = True
        return desired_capabilities

    @property
    def driver(self):
        """Геттер драйвера"""
        return self.__driver

    def get_page(self, url):
        """Пример для получения HTML странички"""
        self.driver.get(url)
        return self.driver.page_source
