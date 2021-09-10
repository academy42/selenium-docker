from selenium import webdriver

from config import settings


class Application:

    __driver = None
    """Драйвер селениума"""

    def __init__(self):
        self.__driver = webdriver.Remote(
            command_executor=f"http://{settings.HUB_HOST}:4444/wd/hub",
            desired_capabilities={"browserName": "chrome", "javascriptEnabled": True},
            keep_alive=True,
        )

    @property
    def driver(self):
        """Геттер драйвера"""
        return self.__driver

    def get_page(self, url):
        """Пример для получения HTML странички"""
        self.driver.get(url)
        return self.driver.page_source
