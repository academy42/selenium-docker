import logging

from app.application import Application

if __name__ == "__main__":
    app = Application()

    page = app.get_page("https://gitmoji.dev")
    app.driver.close()
    app.driver.quit()  # не забываем выйти из браузера, чтобы освободить сессию перед остановкой приложения

    # для того, чтобы убедиться, что все работает
    print(page)
