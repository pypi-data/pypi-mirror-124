import selenium.common.exceptions

import wwshc.wwserr
import wwshc.wwsels
import warnings


def void(*args, **kwargs):
    """
    *** UNDOCUMENTATED ***
    """
    pass


def filterUserList(self, only_online: bool, stop_name: str, stop_mail: str):
    """
    *** UNDOCUMENTATED ***
    """
    res = []
    if not only_online:
        self.driver.find_element_by_link_text("Alle Mitglieder anzeigen").click()
    for u in self.M.driver.find_element_by_id("table_users").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr"):
        if not u.text == "":
            res.append(wwshc.wwsels.User(u.find_element_by_class_name("c_fullname").text, u.find_element_by_class_name("c_login").text, self, self.M))
        if u.text == stop_name:
            return res
    return res


def filterUserListMail(self, mail:str, only_online: bool):
    """
    *** UNDOCUMENTATED ***
    """
    res = []
    if not only_online:
        self.driver.find_element_by_link_text("Alle Mitglieder anzeigen").click()
    try:
        u = self.M.driver.find_element_by_id("table_users").find_element_by_tag_name("tbody").find_element_by_xpath(f"//*[contains(text(),'{mail}')]").find_element_by_xpath("..")
    except selenium.common.exceptions.NoSuchElementException:
        raise wwshc.wwserr.NoSuchUser(f"No user with mail '{mail}' found.")
    return wwshc.wwsels.User(u.find_element_by_class_name("c_fullname").text, u.find_element_by_class_name("c_login").text, self, self.M)


def filterUserListName(self, name: str, only_online: bool):
    """
    *** UNDOCUMENTATED ***
    """
    res = []
    if not only_online:
        self.driver.find_element_by_link_text("Alle Mitglieder anzeigen").click()
    try:
        u = self.M.driver.find_element_by_id("table_users").find_element_by_tag_name("tbody").find_element_by_xpath(f"//*[contains(text(),'{name}')]").find_element_by_xpath("..")

    except selenium.common.exceptions.NoSuchElementException:
        raise wwshc.wwserr.NoSuchUser(f"No user with mail '{name}' found.")
    return wwshc.wwsels.User(u.find_element_by_class_name("c_fullname").text, u.find_element_by_class_name("c_login").text, self, self.M)


def usePopup(self, ignore=[]):
    """
    *** UNDOCUMENTATED ***
    """
    main = self.driver.current_window_handle
    alls = self.driver.window_handles
    alls.remove(main)
    for i in ignore:
        alls.remove(i)
    self.driver.switch_to.window(alls.pop())
    return main


def useAlert(self):
    """
    *** UNDOCUMENTATED ***
    """
    warnings.warn("Use wws.driver.switch_to.alert() instead.")


def useMain(self, main):
    """
    *** UNDOCUMENTATED ***
    """
    self.driver.switch_to_window(main)


class Filter:
    def __init__(self, **kwargs):
        """
        *** UNDOCUMENTATED ***
        """
        self.allowed = kwargs.keys()
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

    def filter(self, list):
        """
        *** UNDOCUMENTATED ***
        """
        filtered_list = list
        for a in self.allowed:
            for e in list:
                if self.__getattribute__(a) == e.__getattribute__(a):
                    filtered_list.remove(e)
        return filtered_list
