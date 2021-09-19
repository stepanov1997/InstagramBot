from selenium import webdriver
from InstagramBot import InstagramBot
import base64
import time

driver = webdriver.Edge("C:\\Users\\stepa\\Desktop\\msedgedriver.exe", verbose=False)

instagramBot = InstagramBot(driver=driver,
                            username="*********************",
                            password="*********************")

try:
    instagramBot.login()
    instagramBot.explorePeoples()
    instagramBot.serialize_new_changes()
except Exception as ex:
    print(ex)
