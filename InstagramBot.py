import json
import time


class InstagramBot:
    def __init__(self, driver, username, password):
        self.list_of_profiles = []
        self.driver = driver
        self.username = username
        self.password = password

    def login(self):
        while True:
            try:
                self.driver.get("https://www.instagram.com/")
                time.sleep(3)
                username = self.driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
                username.send_keys(self.username)
                password = self.driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
                password.send_keys(self.password)
                log_in_button = self.driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')
                log_in_button.click()
                time.sleep(3)
            except:
                time.sleep(5)

    def explorePeoples(self):
        self.driver.get("https://www.instagram.com/explore/people/")
        time.sleep(3)
        while True:
            self.follow_all_suggested_people()
            self.scroll_to_end()
            time.sleep(4)
            if self.is_scrolled_to_end():
                break

    def follow_all_suggested_people(self):
        people_list = self.driver.find_elements_by_xpath('/html/body/div[1]/section/main/div/div[2]/div/div/*')
        for person in people_list[len(self.list_of_profiles):]:

            if len([p for p in self.list_of_profiles if p["id"] == person.id]) != 0:
                continue

            try:
                profile_image = person.find_element_by_xpath(
                    '//div[1]/div/div/span/img')
            except:
                profile_image = person.find_element_by_xpath(
                    './/div[1]/div/div/a/img')

            profile_image_src = profile_image.get_attribute("src")
            profile_name_element = person.find_element_by_xpath(
                './/div[2]/div[1]/div/span/a')
            profile_name = profile_name_element.text
            profile_link = profile_name_element.get_attribute("href")

            try:
                type_of_suggestion_element = person.find_element_by_xpath(
                    './/div[2]/div[3]/div')
                type_of_suggestion = type_of_suggestion_element.text

                profile_description_element = person.find_element_by_xpath(
                    './/div[2]/div[2]/div')
                profile_description = profile_description_element.text
            except:
                type_of_suggestion_element = person.find_element_by_xpath(
                    './/div[2]/div[2]/div')
                type_of_suggestion = type_of_suggestion_element.text
                profile_description = ""

            if type_of_suggestion == "Suggested for you":
                profile_follow_button = person.find_element_by_xpath(
                    './/div[3]/button')
                profile_follow_button.click()

            self.list_of_profiles.append({
                "id": person.id,
                "profile_name": profile_name,
                "profile_description": profile_description,
                "profile_link": profile_link,
                "profile_image": profile_image_src,
                "type_of_suggestion": type_of_suggestion
            })
            self.serialize_new_changes()
            time.sleep(1)

    def serialize_new_changes(self):
        global old_profiles
        try:
            load_fs = open("profiles.json", "r")
            old_profiles = json.load(load_fs)
            load_fs.close()
        except:
            old_profiles = None

        if old_profiles is not None:
            self.list_of_profiles = old_profiles.append(self.list_of_profiles)
        dump_fs = open("profiles.json", "w")
        json.dump(self.list_of_profiles, dump_fs)
        dump_fs.close()

    def is_scrolled_to_end(self):
        document_height = self.driver.execute_script("return document.body.scrollHeight;")
        current_scroll = self.driver.execute_script("return window.scrollY + window.innerHeight;")
        modifier = 100
        return current_scroll + modifier > document_height

    def scroll_to_end(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
