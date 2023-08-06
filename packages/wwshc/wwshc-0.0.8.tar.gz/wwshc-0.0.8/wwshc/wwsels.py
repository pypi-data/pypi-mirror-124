import time

import selenium.common.exceptions

import wwshc.wwserr
import wwshc.wwsopt
from selenium.webdriver.support.ui import Select


class User:
    def __init__(self, name: str, mail: str, found_by, wws):
        """
        :param name: Name of the User
        :param mail: E-mail of the user
        :param found_by: The Element wich found the User (Agent, Group, Class)
        :param wws: The parent Agent
        """
        self.name = name
        self.mail = mail
        self.parent = found_by
        self.M = wws
        self.driver = wws.driver
        self.maw = wws.maw

    def _navTo(self):
        """
        Navigate to the web-page of this element
        """
        self.parent._navTo()
        wwshc.wwsopt.void(self.parent.users_list())

    def quick_send(self, text):
        """
        Send a Quickmessage to the User

        :param text: Text of the Message to send
        """
        self._navTo()
        if self.parent.table.startswith("id:"):
            self.driver.find_element_by_id(self.parent.table.replace("id:", "")).find_element_by_tag_name(
                "tbody").find_element_by_xpath(f"//*[contains(text(),'{self.mail}')]").find_element_by_xpath(
                "..").find_element_by_css_selector(".icons").find_element_by_css_selector(
                '[html_title="Weitere Funktionen"]').click()
            time.sleep(self.maw)
            self.driver.find_element_by_id(self.parent.table.replace("id:", "")).find_element_by_tag_name(
                "tbody").find_element_by_xpath(f"//*[contains(text(),'{self.mail}')]").find_element_by_xpath(
                "..").find_element_by_css_selector(".icons").find_element_by_xpath(
                f"//*[contains(text(),'Quickmassage senden')]").click()
        if self.parent.table.startswith("class:"):
            self.driver.find_element_by_class_name(self.parent.table.replace("class:", "")).find_element_by_tag_name(
                "tbody").find_element_by_xpath(f"//*[contains(text(),'{self.mail}')]").find_element_by_xpath(
                "..").find_element_by_css_selector(".icons").find_element_by_css_selector(
                '[html_title="Weitere Funktionen"]').click()
            time.sleep(self.maw)
            self.driver.find_element_by_class_name(self.parent.table.replace("class:", "")).find_element_by_tag_name(
                "tbody").find_element_by_xpath(f"//*[contains(text(),'{self.mail}')]").find_element_by_xpath(
                "..").find_element_by_css_selector(".icons").find_element_by_xpath(
                f"//*[contains(text(),'Quickmassage senden')]").click()
        main = wwshc.wwsopt.usePopup(self)
        self.driver.switch_to.frame(self.driver.find_element_by_class_name("wysiwyg"))
        self.driver.find_element_by_class_name("wysiwyg").send_keys(text)
        self.driver.switch_to.default_content()
        time.sleep(self.M.maw)
        self.driver.find_element_by_class_name("submit").click()
        wwshc.wwsopt.useMain(self, main)


class Group:
    table = "id:user_table"

    def __init__(self, name: str, wws):
        """
        :param name: Of the Group
        :param wws: The parent Agent
        """
        self.name = name
        self.M = wws
        self.driver = wws.driver

    def _navTo(self):
        """
        Navigate to the web-page of this element
        """
        self.M._navTo()
        Select(self.driver.find_element_by_id("top_select_18")).select_by_visible_text(self.name)

    def users_list(self, only_online=False, stop_name="", stop_mail=""):
        """
        Use this to list all Users of this Group

        :param only_online: If you want to list ony people are online.
        :return: List of all Users of this Group
        """
        self._navTo()
        self.driver.find_element_by_id("menu_109756").find_element_by_tag_name("a").click()
        return wwshc.wwsopt.filterUserList(self, only_online, stop_name, stop_mail)

    def users_getByName(self, name: str, only_online=False):
        """
        Use this to get a User of this Group by his Name
        :raise wwshc.err.NoSuchUser: If the User cannot be found by your search arguments

        :param name: Name of the User you are requesting.
        :return: The User you Requested
        """
        self._navTo()
        self.driver.find_element_by_id("menu_109756").find_element_by_tag_name("a").click()
        return wwshc.wwsopt.filterUserListName(self, name, only_online)

    def users_getByMail(self, mail: str, only_online=False):
        """
        Use this to get a User of this Group by his E-Mail
        :raise wwshc.err.NoSuchUser: If the User cannot be found by your search arguments

        :param mail: E-Mail of the User you are requesting.
        :return: The User you Requested
        """
        self._navTo()
        self.driver.find_element_by_id("menu_109756").find_element_by_tag_name("a").click()
        return wwshc.wwsopt.filterUserListMail(self, mail, only_online)


class Class:
    table = "id:user_table"

    def __init__(self, name: str, wws):
        """
        :param name: Name of the Group
        :param wws: The parent Agent
        """
        self.name = name
        self.M = wws
        self.driver = wws.driver

    def _navTo(self):
        """
        Navigate to the web-page of this element
        """
        self.M._navTo()
        Select(self.driver.find_element_by_id("top_select_19")).select_by_visible_text(self.name)

    def users_list(self, only_online=False, stop_name="", stop_mail=""):
        """
        Use this to list all Users of this Group

        :param only_online: If you want to list ony people are online.
        :return: List of all Users of this Group
        """
        self._navTo()
        self.driver.find_element_by_id("menu_109616").find_element_by_tag_name("a").click()
        return wwshc.wwsopt.filterUserList(self, only_online, stop_name, stop_mail)

    def users_getByName(self, name: str, only_online=False):
        """
        Use this to get a User of this Class by his Name
        :raise wwshc.err.NoSuchUser: If the User cannot be found by your search arguments

        :param name: Name of the User you are requesting.
        :return: The User you Requested
        """
        self._navTo()
        self.driver.find_element_by_id("menu_109616").find_element_by_tag_name("a").click()
        return wwshc.wwsopt.filterUserListName(self, name, only_online)

    def users_getByMail(self, mail: str, only_online=False):
        """
        Use this to get a User of this Class by his E-Mail
        :raise wwshc.err.NoSuchUser: If the User cannot be found by your search arguments

        :param mail: E-Mail of the User you are requesting.
        :param only_online: Only search for online users
        :return: The User you Requested
        """
        self._navTo()
        self.driver.find_element_by_id("menu_109616").find_element_by_tag_name("a").click()
        return wwshc.wwsopt.filterUserListMail(self, mail, only_online)

    def forum_commentPost(self, id: str, text: str, icon: str, popup: bool, quote: bool):
        """
        Send a commant to a post in the forum of this class

        :param id: Id of the Post (get all IDs with Class.getForumPosts())
        :param text: Text for the comment
        :param icon: The icon of the comment (i for info; l for humor; a for answer; q for question; p for pro; c for contra)
        :param popup: Pass True if you want to get System-Messages if someone answers your comment; else False
        :param quote: Pass True if you want to insert a quote of the post you're answering to
        """
        self._navTo()
        self.driver.find_element_by_id("menu_109660").find_element_by_tag_name("a").click()
        for p in self.driver.find_element_by_class_name("jail_table").find_element_by_tag_name(
                "tbody").find_elements_by_tag_name("tr"):
            if p.get_property("id") == id:
                time.sleep(self.M.maw)
                try:
                    p.find_element_by_css_selector('[html_title="Beitrag kommentieren"]').click()
                except selenium.common.exceptions.NoSuchElementException:
                    p.find_element_by_css_selector('[html_title="Aufklappen"]').click()
                    p = self.driver.find_element_by_class_name("jail_table").find_element_by_tag_name(
                        "tbody").find_element_by_css_selector(f'tr[id="{id}"]')
                    p.find_elements_by_css_selector('[html_title="Beitrag kommentieren"]')[0].click()
                time.sleep(self.M.maw)
                main = wwshc.wwsopt.usePopup(self)
                self.driver.switch_to.frame(self.driver.find_element_by_class_name("wysiwyg"))
                self.driver.find_element_by_class_name("wysiwyg").send_keys(text)
                self.driver.switch_to.default_content()
                t = self.driver.find_element_by_class_name("table_choices")
                if icon == "i":
                    t.find_element_by_id("id_125200_1").click()
                if icon == "l":
                    t.find_element_by_id("id_125200_2").click()
                if icon == "q":
                    t.find_element_by_id("id_125200_3").click()
                if icon == "a":
                    t.find_element_by_id("id_125200_4").click()
                if icon == "p":
                    t.find_element_by_id("id_125200_5").click()
                if icon == "c":
                    t.find_element_by_id("id_125200_6").click()
                self.driver.execute_script(
                    f'window.scrollTo(0, {self.driver.find_element_by_name("notification").location["y"]})')
                if popup:
                    self.driver.find_element_by_name("notification").click()
                if quote:
                    self.driver.find_element_by_name("quote").click()
                self.driver.find_element_by_name("preview").click()
                self.driver.find_element_by_name("save").click()

    def forum_createPost(self, title: str, text: str, icon: str, popup: bool):
        """
        *** UNDOCUMENTATED ***
        """
        self._navTo()
        self.driver.find_element_by_id("menu_109660").find_element_by_tag_name("a").click()
        self.driver.find_element_by_link_text("Neuen Diskussionsstrang eröffnen").click()
        time.sleep(self.M.maw)
        main = wwshc.wwsopt.usePopup(self)
        self.driver.find_element_by_name("subject").send_keys(title)
        self.driver.switch_to.frame(self.driver.find_element_by_class_name("wysiwyg"))
        self.driver.find_element_by_class_name("wysiwyg").send_keys(text)
        self.driver.switch_to.default_content()
        t = self.driver.find_element_by_class_name("table_choices")
        if icon == "i":
            t.find_element_by_id("id_125200_1").click()
        if icon == "l":
            t.find_element_by_id("id_125200_2").click()
        if icon == "q":
            t.find_element_by_id("id_125200_3").click()
        if icon == "a":
            t.find_element_by_id("id_125200_4").click()
        if icon == "p":
            t.find_element_by_id("id_125200_5").click()
        if icon == "c":
            t.find_element_by_id("id_125200_6").click()
        self.driver.execute_script(
            f'window.scrollTo(0, {self.driver.find_element_by_name("notification").location["y"]})')
        if popup:
            self.driver.find_element_by_name("notification").click()
        self.driver.find_element_by_name("preview").click()
        self.driver.find_element_by_name("save").click()

    def forum_listPosts(self):
        """
        Get a list of all posts in the forum of this class

        :return: List of dicts with infos about a forum post
        """
        res = []
        self._navTo()
        self.driver.find_element_by_id("menu_109660").find_element_by_tag_name("a").click()
        time.sleep(self.M.maw)
        for p in self.driver.find_element_by_class_name("jail_table").find_element_by_tag_name(
                "tbody").find_elements_by_tag_name("tr"):
            res.append({"id": p.get_property("id"), "title": p.find_element_by_tag_name("a").text,
                        "time": p.find_elements_by_tag_name("td")[2].get_property("sort"),
                        "comments": p.find_element_by_class_name("info").text, "author": self.users_getByName(
                    "martha.max")})  # p.find_elements_by_tag_name("td")[2].find_element_by_tag_name("span").get_property("html_title")
        return res

    def chat_send(self, msg: str):
        """
        Use This to send a Chat-MSG

        :param msg: Text of the MSG
        """
        self._navTo()
        self.driver.find_element_by_id("menu_133729").find_element_by_tag_name("a").click()
        self.driver.find_element_by_id("block_link_open_chat").click()
        time.sleep(self.M.maw)
        main = wwshc.wwsopt.usePopup(self)
        self.driver.switch_to.frame(self.driver.find_element_by_class_name("wysiwyg"))
        self.driver.find_element_by_class_name("wysiwyg").send_keys(msg)
        self.driver.switch_to.default_content()
        time.sleep(self.M.maw)
        self.driver.find_element_by_class_name("submit").click()
        self.driver.find_element_by_id("popup_top_icons_icon_close").find_element_by_tag_name("a").click()
        wwshc.wwsopt.useMain(self, main)


class Task:
    def __init__(self, title: str, source: str, done: bool, found_by, wws):
        """
        *** UNDOCUMENTATED ***
        """
        self.M = wws
        self.driver = wws.driver
        self.parent = found_by
        self.done = done
        self.made_by = source
        self.title = title

    def reload(self):
        """
        *** UNDOCUMENTATED ***
        """
        self.parent._navTo()
        wwshc.wwsopt.void(self.parent.tasks_list())

    def toggleDone(self):
        """
        *** UNDOCUMENTATED ***
        """
        self.reload()
        for element in self.driver.find_element_by_class_name("jail_table").find_element_by_tag_name(
                "tbody").find_elements_by_tag_name("tr"):
            if self.title == element.find_element_by_class_name("c_title").text:
                element.find_element_by_class_name("c_state").find_element_by_tag_name("img").click()
                time.sleep(self.M.maw)
                main = wwshc.wwsopt.usePopup(self)
                self.driver.find_element_by_id("id_419089_1").click()
                wwshc.wwsopt.useMain(self, main)
                time.sleep(self.M.maw)
                break
