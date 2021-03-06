from model.contact import Contact
from selenium.webdriver.support.select import Select
import re

class ContactHelper:

    def __init__(self, app):
        self.app = app

    def return_to_home_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("home page").click()

    def create(self, contact):
        wd = self.app.wd
        # init contact creation
        wd.find_element_by_link_text("add new").click()
        self.fill_contact_form(contact)
        # submit contact creation
        wd.find_element_by_xpath("(//input[@name='submit'])[2]").click()
        self.return_to_home_page()
        self.сontact_cache = None

    def fill_contact_form(self, contact):
        wd = self.app.wd
        self.change_field_value("firstname", contact.firstname)
        self.change_field_value("middlename", contact.middlename)
        self.change_field_value("lastname", contact.lastname)
        self.change_field_value("nickname", contact.nickname)
        self.change_field_value("address", contact.address)
        self.change_field_value("home", contact.homephone)
        self.change_field_value("mobile", contact.mobile)
        self.change_field_value("work", contact.work)
        self.change_field_value("phone2", contact.fax)
        self.change_field_value("email", contact.email)
        self.change_field_value("email2", contact.email2)
        self.change_field_value("email3", contact.email3)
        #self.change_field_value("nickname", contact.nikname)

    def change_field_value(self, fild_firstname, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(fild_firstname).click()
            wd.find_element_by_name(fild_firstname).clear()
            wd.find_element_by_name(fild_firstname).send_keys(text)

    def choice_contact_by_index(self, index):
        wd = self.app.wd
        #wd.find_elements_by_name("selected[]")[index].click()
        wd.find_elements_by_xpath("//img[@alt='Edit']")[index].click()

    def choice_contact(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()


    def delete_contact_by_index(self, index):
        wd = self.app.wd
        self.choice_contact_by_index(index)
        # submit contact deletion
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        wd.switch_to.alert.accept()
        wd.find_element_by_css_selector("div.msgbox")
        self.open_home_page()
        self.сontact_cache = None


    def delete_contact_by_id(self, id):
        wd = self.app.wd
        self.choice_contact_by_id(id)
        # submit contact deletion
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        wd.switch_to.alert.accept()
        wd.find_element_by_css_selector("div.msgbox")
        self.open_home_page()
        self.сontact_cache = None

    def modify_contact_by_id(self, id, contact_new):
        wd = self.app.wd
        self.open_home_page()
        # init edit contact
        wd.find_element_by_css_selector("a[href='edit.php?id=%s" % id).click()
        self.fill_contact_form(contact_new)
        # submit contact update
        wd.find_element_by_name("update").click()
        self.return_to_home_page()
        self.сontact_cache = None

    def choice_contact_by_id(self, id):
        wd = self.app.wd
        self.open_home_page()
        wd.find_element_by_css_selector("input[value='%s" % id).click()


    def delete_first_contact(self):
        wd = self.app.wd
        # init contact deletion
        self.choice_first_contact()
        # submit contact deletion
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        wd.switch_to.alert.accept()
        wd.find_element_by_css_selector("div.msgbox")
        self.open_home_page()
        self.сontact_cache = None


    def choice_first_contact(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()

    def choice_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_name("selected[]")[index].click()

    def modify_contact_by_index(self, index, contact_new):
        wd = self.app.wd
        # init edit contact
        self.choice_contact_by_index(index)
        wd.find_elements_by_xpath("//img[@alt='Edit']")[index].click()
        wd.find_element_by_name("update")
        self.fill_contact_form(contact_new)
        # submit contact update
        wd.find_element_by_name("update").click()
        self.return_to_home_page()
        self.сontact_cache = None

    def modify_first_contact(self, new_contact_data):
        wd = self.app.wd
        # init edit contact
        wd.find_element_by_xpath("//img[@alt='Edit']").click()
        wd.find_element_by_name("update")
        self.fill_contact_form(new_contact_data)
        # submit contact update
        wd.find_element_by_name("update").click()
        self.return_to_home_page()
        self.сontact_cache = None

    def count_contact(self):
        wd = self.app.wd
        self.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    def open_home_page(self):
        wd = self.app.wd
        if not len(wd.find_elements_by_name("add")) > 0:
            wd.find_element_by_link_text("home").click()

    сontact_cache = None

    def get_contact_list(self):
        if self.сontact_cache is None:
            wd = self.app.wd
            self.open_home_page()
            self.сontact_cache = []
            for row in wd.find_elements_by_name("entry"):
                cells = row.find_elements_by_tag_name("td")
                id = cells[0].find_element_by_name("selected[]").get_attribute("value")
                lastname = cells[1].text
                firstname = cells[2].text
                address = cells[3].text
                all_emails = cells[4].text
                all_phones = cells[5].text
                self.сontact_cache.append(Contact(firstname=firstname, lastname=lastname, id=id,
                                                  address=address, all_emails_from_home_page=all_emails,
                                                  all_phones_from_home_page=all_phones))

        return list(self.сontact_cache)


    def open_contact_to_edit_by_index(self, index):
        wd = self.app.wd
        self.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[7]
        cell.find_element_by_tag_name("a").click()

    def open_contact_view_by_index(self, index):
        wd = self.app.wd
        self.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[6]
        cell.find_element_by_tag_name("a").click()

    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.open_home_page()
        self.open_contact_to_edit_by_index(index)
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        id = wd.find_element_by_name("id").get_attribute("value")
        address = wd.find_element_by_name("address").get_attribute("value")
        email = wd.find_element_by_name("email").get_attribute("value")
        email2 = wd.find_element_by_name("email2").get_attribute("value")
        email3 = wd.find_element_by_name("email3").get_attribute("value")
        homephone = wd.find_element_by_name("home").get_attribute("value")
        workphone = wd.find_element_by_name("work").get_attribute("value")
        mobilephone = wd.find_element_by_name("mobile").get_attribute("value")
        secondaryphone = wd.find_element_by_name("phone2").get_attribute("value")
        return Contact(first_name=firstname, last_name=lastname, id=id,
                       address=address, email=email, email2=email2, email3=email3,
                       homephone=homephone, workphone=workphone,
                       mobilephone=mobilephone, secondaryphone=secondaryphone)

    def get_contact_from_view_page(self, index):
        wd = self.app.wd
        self.open_contact_view_by_index(index)
        text = wd.find_element_by_id("content").text
        homephone = re.search("H: (.*)", text).group(1)
        workphone = re.search("W: (.*)", text).group(1)
        mobilephone = re.search("M: (.*)", text).group(1)
        secondaryphone = re.search("P: (.*)", text).group(1)
        return Contact(homephone=homephone, workphone=workphone,
                       mobilephone=mobilephone, secondaryphone=secondaryphone)

    def select_none(self):
        wd = self.app.wd
        self.app.open_home_page()
        Select(wd.find_element_by_name("group")).select_by_visible_text("[none]")
        wd.find_element_by_xpath("//option[@value='[none]']").click()

    def add_contact_in_group(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()
        wd.find_element_by_name("to_group").click()
        Select(wd.find_element_by_name("to_group")).select_by_visible_text("test")
        wd.find_element_by_name("add").click()
        self.app.open_home_page()

    def remove_contact_in_group(self):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_name("group").click()
        Select(wd.find_element_by_name("group")).select_by_visible_text("test")
        wd.find_element_by_name("selected[]").click()
        wd.find_element_by_name("remove").click()
        wd.find_element_by_link_text("home").click()

    def open_contact_list_in_group_by_id(self, id):
        wd = self.app.wd
        self.app.open_home_page()
        Select(wd.find_element_by_xpath('//*[@id="right"]/select')).select_by_value(id)

    def open_contact_list_not_in_group(self):
        wd = self.app.wd
        self.app.open_home_page()
        Select(wd.find_element_by_name("group")).select_by_visible_text("[none]")

    def add_contact_in_group(self, contact_id, group_id):
        wd = self.app.wd
        self.open_contact_list_not_in_group()
        self.choice_contact_by_id(contact_id)
        wd.find_element_by_xpath("(//option[@value='%s'])[2]" % group_id).click()
        wd.find_element_by_name("add").click()
        self.contact_cache = None

    def delete_contact_from_group(self, contact_id, group_id):
        wd = self.app.wd
        self.open_contact_list_in_group_by_id(group_id)
        self.choice_contact
        wd.find_element_by_name("remove").click()