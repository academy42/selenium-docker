import os
import zipfile

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy

from config import settings

PROXY_HOST = "dc3.ibaldr.ru"  # rotating proxy
PROXY_PORT = 8120
PROXY_USER = "63eqtpf95"
PROXY_PASS = "e92vhr2j5y"

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
          },
          bypassList: ["localhost"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (
    PROXY_HOST,
    PROXY_PORT,
    PROXY_USER,
    PROXY_PASS,
)


class Application:

    __driver = None
    """Драйвер селениума"""

    def __init__(self):
        dc = self.__setup_chrome_capabilities()
        self.__driver = self.get_chromedriver(dc=dc, use_proxy=True)

    @staticmethod
    def get_chromedriver(dc: DesiredCapabilities, use_proxy=False, user_agent=None):
        path = os.path.dirname(os.path.abspath(__file__))
        chrome_options = webdriver.ChromeOptions()
        if use_proxy:
            pluginfile = "proxy_auth_plugin.zip"

            with zipfile.ZipFile(pluginfile, "w") as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)
        if user_agent:
            chrome_options.add_argument("--user-agent=%s" % user_agent)
        driver = webdriver.Remote(
            command_executor=f"http://{settings.HUB_HOST}:4444/wd/hub",
            options=chrome_options,
            desired_capabilities=dc,
            keep_alive=True,
        )
        return driver

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
