
import sqlalchemy
from sqlalchemy import create_engine, text
from flask import Flask, request, render_template, jsonify, current_app
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


debug = True


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('./config.py')
    db = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = db
    EMAIL = app.config['EMAIL']
    PASSWORD = app.config['PASSWORD']

    
    
    @app.route('/')
    def run_bot():
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)

        globalURL = 'https://www.messenger.com/t/101210925710184'
        driver.get(globalURL)   


        def urlCheck(currentURL):
            if globalURL != currentURL:
                driver.get(globalURL)
                time.sleep(4)
                return urlCheck(driver.current_url)
            else:
                return True

            

        time.sleep(2)

        email = driver.find_element(By.ID, 'email')
        email.send_keys(f'{EMAIL}')
        password = driver.find_element(By.ID, 'pass')
        password.send_keys(f'{PASSWORD}')
        keepLogIn = driver.find_element(By.CSS_SELECTOR, '#loginform > div._9h75 > div > div > label.uiInputLabelInput > span')
        keepLogIn.click()
        login = driver.find_element(By.XPATH, '//*[@id="loginbutton"]')
        login.click()

        time.sleep(2)

        # Mocking_Jae messenger page
        driver.get('https://www.messenger.com/t/101210925710184')

        time.sleep(2)

        while True:

            senders = [sender['name'] for sender in current_app.database.execute(text("SELECT * FROM senders")).fetchall()]

            cells = driver.find_elements(By.CSS_SELECTOR, '.nqmvxvec.j83agx80.cbu4d94t.tvfksri0.aov4n071.bi6gxh9e.l9j0dhe7')

            # container is a dictionary that maps top n users to their recent m messages
            # updated every session
            container = {}
            nameToURL = {}

            for cell in cells:
                cell.click()
                time.sleep(1)
                globalURL = driver.current_url
                time.sleep(2)

                try:
                    # get the name of the user
                    urlCheck(driver.current_url)
                    name = driver.find_element(By.CSS_SELECTOR,
                    ".oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8").text
                    urlCheck(driver.current_url)
                    container[name] = [message.get_attribute('innerHTML') for message in driver.find_elements(By.CSS_SELECTOR, ".oo9gr5id.ii04i59q")]
                    urlCheck(driver.current_url)
                    nameToURL[name] = driver.current_url
                except:
                    continue

            for name in container.keys():
                if name not in senders:
                    id = current_app.database.execute(text("INSERT INTO senders (name) VALUES (:name)"), {'name' : name}).lastrowid

                    for message in container[name]:
                        current_app.database.execute(text("INSERT INTO messages (id, message) VALUES (:id, :message)"), {'id' : id, 'message' : message})

                    driver.get(nameToURL[name])
                    globalURL = driver.current_url
                    time.sleep(3)
                    urlCheck(driver.current_url)
                    messageBox = driver.switch_to.active_element
                    if debug:
                        messageBox.send_keys(f"{name}야 메시지 줘서 고마워 ! 지금은 자동 응답기 테스트 중이야 !", Keys.ENTER)
                    else:
                        messageBox.send_keys(f"{name}야 고마워 ! 주소도 알랴주면 재우가 답장을 할 수 있어 !", Keys.ENTER)
                
        
                else:
                    id = current_app.database.execute(text("SELECT * FROM senders WHERE name = :name"), {'name' : name}).fetchone()['id']
                    messages = current_app.database.execute(text("SELECT message FROM messages WHERE id = :id"), {'id' : id})
                    for message in container[name]:
                        if message not in messages:
                            current_app.database.execute(text("INSERT INTO messages (id, message) VALUES (:id, :message)"), {'id' : id, 'message' : message})
                            if container[name][-1] == message:
                                driver.get(nameToURL[name])
                                globalURL = driver.current_url
                                time.sleep(3)
                                urlCheck(driver.current_url)
                                messageBox = driver.switch_to.active_element
                                if debug:
                                    messageBox.send_keys(f"{name}야 메시지 줘서 고마워 ! 지금은 자동 응답기 테스트 중이야 !", Keys.ENTER)
                                else:
                                    messageBox.send_keys(f"{name}야 고마워 ! 주소도 알랴주면 재우가 답장을 할 수 있어 !", Keys.ENTER)
                                time.sleep(2)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(threaded=True, port=5000, debug=True)











