
import sqlalchemy
from sqlalchemy import create_engine, text
from flask import Flask, request, render_template, jsonify, current_app
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json

app = Flask(__name__)
app.config.from_pyfile('./config.py')
db = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
app.database = db
EMAIL = app.config['EMAIL']
PASSWORD = app.config['PASSWORD']


driver = webdriver.Chrome('/Users/USER/Projects/seleniumBeta/chromedriver')

senders = [sender['name'] for sender in current_app.database.execute(text("SELECT * FROM senders")).fetchall()]


driver.get('https://www.messenger.com/t/101210925710184')

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

    cells = driver.find_elements(By.CSS_SELECTOR, '.nqmvxvec.j83agx80.cbu4d94t.tvfksri0.aov4n071.bi6gxh9e.l9j0dhe7')

    # container is a dictionary that maps top n users to their recent m messages
    # updated every session
    container = {}

    for cell in cells:
        cell.click()
        time.sleep(2)
        # get the name of the user
        name = driver.find_element(By.CSS_SELECTOR,
         ".oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8").text
        container[name] = [message.get_attribute('innerHTML') for message in driver.find_elements(By.CSS_SELECTOR, ".oo9gr5i.ii04i59q")]

    for name in container.keys:
        if name not in senders:
            id = current_app.database.execute(text("INSERT INTO senders (name) VALUES (:name)"), {'name' : name}).lastrowid
            for message in container[name]:
                current_app.database.execute(text("INSERT INTO messages (id, message) VALUES (:id, :message)"), {'id' : id, 'message' : message})
        else:
            id = current_app.database.execute(text("SELECT id FROM senders WHERE name = :name"), {'name' : name})[0]
            messages = current_app.database.execute(text("SELECT message FROM messages WHERE id = :id"), {'id' : id})
            for message in container[name]:
                if message not in messages:
                    current_app.database.execute(text("INSERT INTO messages (id, message) VALUES (:id, :message)"), {'id' : id, 'message' : message})
                    if container['name'][-1] == message:
                        driver.get(f'https://www.messenger.com/t/{name}')
                        time.sleep(1)
                        messageBox = driver.switch_to.active_element
                        messageBox.send_keys(f"고마워 ! 주소도 알랴주면 재우가 답장을 할 수 있어 !", Keys.ENTER)




