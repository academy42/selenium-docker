from app.application import Application

if __name__ == "__main__":
    app = Application()

    page = app.get_page("https://2ip.ru")
    if page.find("ERR_PROXY_CONNECTION_FAILED") != -1:
        print("NOT CONNECTED!")
    else:
        print("CONNECTED!")

    app.driver.close()
    app.driver.quit()  # не забываем выйти из браузера, чтобы освободить сессию перед остановкой приложения

    # для того, чтобы убедиться, что все работает
    print(page)
    # 178.176.75.63
