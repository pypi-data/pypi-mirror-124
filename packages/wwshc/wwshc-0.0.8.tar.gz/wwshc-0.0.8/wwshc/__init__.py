import os

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import win10toast
import time
import wwshc.wwsels
import wwshc.wwsopt
import pydatfile
import pyderman
import wwshc.wwserr


def ensure_chromedriver():
    pyderman.install(pyderman.chrome, file_directory=".", filename="chromedriver.exe")


class Agent:
    table = "class:jail_table"

    def __init__(self, url="", user="", passwd="", hide=True, wait=0.5, no_notification=False, file=None):
        """
        THIS PROJECT WAS CREATED BY A STUDENT. THERE ARE MANY FUNCTIONS THAT ONLY ADMINS HAVE OR THAT HAVE NOT BEEN RELEASED TO ME. THESE ARE NOT INCLUDED.

        :param url: URL of your wws-System.
        :param user: E-Mail of your WebWeaverSchool-Account (Normally name@schoolname.wwsurl.topleveldomain)
        :param passwd: Password of your WebWeaverSchool-Account
        :param hide: True if you don't want
        :param wait: Time the System waits for API-Requests/Page-Builings before starting to act after page-load.
        :param no_notification: Set true if you don't want do see a success notification
        :param file: If set all other params are ignored. Sets the settings in a file
        """
        ensure_chromedriver()   # Ensure the newest chromedriver is installed.
        if file is not None:
            f = pydatfile.open(file, except_value={})
            self.URL = f["url"]
            self.USER = f["user"]
            self.PASS = f["passwd"]
            self.maw = f["wait"]
        else:
            self.URL = url
            self.USER = user
            self.PASS = passwd
            self.maw = wait
        self.holdOn = False
        opts = webdriver.ChromeOptions()
        opts.headless = hide
        self.driver = webdriver.Chrome('./chromedriver.exe', options=opts)
        self.driver.set_window_size(1500, 1000)
        self._nav("/wws/100001.php")
        self.driver.find_element_by_css_selector("a.language_selection_current_link").click()
        for lang in self.driver.find_elements_by_css_selector("a.language_selection_option_link"):
            if lang.text == "Deutsch":
                lang.click()
                break
        time.sleep(self.maw)
        if not no_notification:
            win10toast.ToastNotifier().show_toast("MHC", "MoodleHackClient-Agent erfolgreich gestartet.", threaded=True)

    def hold(self, autostop=True):
        """
        Hold the window opened (useless if headless)

        :param autostop: Atomatticcally stop holding if the window is closed.
        """
        self.holdOn = True
        while self.holdOn:
            time.sleep(self.maw)
            if autostop:
                try:
                    if len(self.driver.window_handles) == 0:
                       break
                    else:
                        pass
                except selenium.common.exceptions.InvalidSessionIdException:
                    break
                except selenium.common.exceptions.WebDriverException:
                    break

    def _navTo(self):
        """
        Navigate to the web-page of this element
        """
        self.check()
        self.driver.find_element_by_id("top_chapter_first").click()

    def _nav(self, suburl: str):
        """
        Navigate to the given url.
        :param suburl: URL to navigate to.
        """
        self.driver.get(self.URL+suburl)
        self.check()

    def check(self):
        """
        Checks if a login is needed and logs in.
        """
        try:
            time.sleep(self.maw)
            self.driver.find_element_by_css_selector('[html_title="Einloggen"').click()
            self.driver.find_element_by_id("login_login").send_keys(self.USER)
            self.driver.find_element_by_id("login_password").send_keys(self.PASS)
            self.driver.find_element_by_name("login_submit").click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def class_list(self):
        """
        Use this to list all Classes are avalible for you

        :return: List of all Classes
        """
        self.check()
        clss = []
        for c in Select(self.driver.find_element_by_css_selector('[html_title="Meine Klassen"')).options:
            if c.text != "Meine Klassen" and c.text != "--------------------------------------":
                clss.append(wwshc.wwsels.Class(c.text, self))
        return clss

    def class_get(self, name: str):
        """
        Use this to get a Class avalible for you
        :raise wwshc.err.NoSuchClass: If the Class is not avalible for you or is not existing

        :param name: Name of the Class you want to have
        :return: The Class you requested
        """
        self.check()
        for c in self.class_list():
            if c.name == name:
                return c
        raise wwshc.wwserr.NoSuchClass(f"No class with name '{name}' found.")

    def groups_list(self):
        """
        Use this to list all Groups are avalible for you

        :return: List of all Groups
        """
        self.check()
        grps = []
        for g in Select(self.driver.find_element_by_css_selector('[html_title="Meine Gruppen"')).options:
            if g.text != "Meine Gruppen" and g.text != "Gruppenübersicht" and g.text != "--------------------------------------":
                grps.append(wwshc.wwsels.Group(g.text, self))
        return grps

    def groups_get(self, name: str):
        """
        Use this to get a Group avalible for you
        :raise wwshc.err.NoSuchGroup: If the Group is not avalible for you or is not existing

        :param name: Name of the Group you want to have
        :return: The Group you requested
        """
        self.check()
        for g in self.groups_list():
            if g.name == name:
                return g
        raise wwshc.wwserr.NoSuchGroup(f"No group with name '{name}' found.")

    def users_list(self, only_online=False, stop_name="", stop_mail=""):
        """
        Use this to list all Users in Contacts

        :param only_online: If you want to list ony people are online.
        :return: List of all Users in Contacts
        """
        self._navTo()
        self.driver.find_element_by_id("menu_105492").find_element_by_tag_name("a").click()
        res = []
        if not only_online:
            self.driver.find_element_by_link_text("Alle Mitglieder anzeigen").click()
        for u in self.driver.find_element_by_class_name("table_list").find_element_by_tag_name(
                "tbody").find_elements_by_tag_name("tr"):
            if not u.text == "":
                res.append(wwshc.wwsels.User(u.find_elements_by_tag_name("td")[3].text,
                                             u.find_elements_by_tag_name("td")[4].text, self, self))
            if u.text == stop_name:
                return res
        return res

    def users_add(self, name_or_mail):
        """
        *** UNDOCUMENTATED ***
        """
        try:
            self._navTo()
            self.driver.find_element_by_id("menu_105492").find_element_by_tag_name("a").click()
            self.driver.find_element_by_link_text("Mitglied aufnehmen").click()
            time.sleep(self.maw)
            main = wwshc.wwsopt.usePopup(self)
            self.driver.find_element_by_name("add_member").send_keys(name_or_mail)
            try:
                self.driver.find_element_by_class_name("submit").click()
                self.driver.find_element_by_class_name("submit").click()
            except selenium.common.exceptions.NoSuchElementException:
                raise wwshc.wwserr.AlreadyInContacts("This User is already in your contact list")
            time.sleep(self.maw)
            wwshc.wwsopt.useMain(self, main)
        except selenium.common.exceptions.UnexpectedAlertPresentException as e:
            if e.alert_text == "Kein gültiger Nutzer":
                raise wwshc.wwserr.NoSuchUser(f"The User {name_or_mail} is not existing.")
            else:
                print(e.alert_text)

    def users_remove(self, name_or_mail):
        """
        *** UNDOCUMENTATED ***
        """
        self._navTo()
        self.driver.find_element_by_id("menu_105492").find_element_by_tag_name("a").click()
        print(self.driver.find_element_by_class_name("jail_table").find_element_by_tag_name("tbody").find_element_by_xpath(f"//*[contains(text(),'{name_or_mail}')]"))
        self.driver.find_element_by_class_name("jail_table").find_element_by_tag_name("tbody").find_element_by_xpath(f"//*[contains(text(),'{name_or_mail}')]").find_element_by_xpath("..").find_element_by_css_selector(".icons").find_element_by_css_selector('[html_title="Weitere Funktionen"]').click()
        time.sleep(self.maw)
        self.driver.find_element_by_class_name("jail_table").find_element_by_tag_name("tbody").find_element_by_xpath(f"//*[contains(text(),'{name_or_mail}')]").find_element_by_xpath("..").find_element_by_css_selector(".icons").find_element_by_xpath(f"//*[contains(text(),'Löschen')]").click()
        self.driver.switch_to.alert()
        self.driver.close()
        self.driver.switch_to.active_element()

    def users_getByName(self, name: str):
        """
        Use this to get a User in Contacts by his Name
        :raise wwshc.err.NoSuchUser: If the User cannot be found by your search arguments

        :param name: Name of the User you are requesting.
        :return: The User you Requested
        """
        for u in self.users_list(stop_name=name):
            if u.name == name:
                return u
        raise wwshc.wwserr.NoSuchUser(f"No user with name '{name}' found.")

    def users_getByMail(self, mail: str):
        """
        Use this to get a User in Contacts by his E-Mail
        :raise wwshc.err.NoSuchUser: If the User cannot be found by your search arguments

        :param mail: E-Mail of the User you are requesting.
        :return: The User you Requested
        """
        for u in self.users_list(stop_mail=mail):
            if u.mail == mail:
                return u
        raise wwshc.wwserr.NoSuchUser(f"No user with mail '{mail}' found.")

    def files_uploadFile(self, filepath):
        """
        *** UNDOCUMENTATED ***
        """
        self.driver.find_element_by_id("menu_121332").find_element_by_tag_name("a").click()
        self.driver.find_element_by_link_text("Neue Datei ablegen").click()
        time.sleep(self.maw)
        main = wwshc.wwsopt.usePopup(self)
        self.driver.find_element_by_name("file[]").send_keys(filepath)
        self.driver.find_element_by_class_name("submit").click()
        wwshc.wwsopt.useMain(self, main)

    def files_addFile(self, filepath):
        """
        *** UNDOCUMENTATED ***
        """
        raise NotImplementedError("Cannot add a file.")

    def files_removeFile(self, path):
        """
        *** UNDOCUMENTATED ***
        """
        raise NotImplementedError("Cannot remove a file.")

    def files_addFolder(self, name, description=""):
        """
        *** UNDOCUMENTATED ***
        """
        self.driver.find_element_by_id("menu_121332").find_element_by_tag_name("a").click()
        self.driver.find_element_by_link_text("Ordner anlegen").click()
        time.sleep(self.maw)
        main = wwshc.wwsopt.usePopup(self)
        self.driver.find_element_by_name("folder").send_keys(name)
        self.driver.find_element_by_name("description").send_keys(description)
        self.driver.find_element_by_class_name("submit").click()
        wwshc.wwsopt.useMain(self, main)

    def files_removeFolder(self, path):
        """
        *** UNDOCUMENTATED ***
        """
        raise NotImplementedError("Cannot remove a folder.")

    def tasks_list(self):
        """
        *** UNDOCUMENTATED ***
        """
        self._navTo()
        res = []
        self.driver.find_element_by_id("menu_105500").find_element_by_tag_name("a").click()
        for element in self.driver.find_element_by_class_name("jail_table").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr"):
            res.append(wwshc.wwsels.Task(element.find_element_by_class_name("c_title").text, element.find_element_by_class_name("c_source").text, element.get_property("sort") == "2", self, self))
        return res

    def tasks_get(self, filter: wwshc.wwsopt.Filter):
        """
        *** UNDOCUMENTATED ***
        """
        return filter.filter(self.tasks_list())[0]

    def __exit__(self):
        return self.__del__()

    def __del__(self):
        try:
            if len(self.driver.window_handles) != 0:
               self.driver.close()
        except selenium.common.exceptions.InvalidSessionIdException:
            return False
        except selenium.common.exceptions.WebDriverException:
            return False
        return True
