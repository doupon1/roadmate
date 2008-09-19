
#----Test UserCase 2.2---------------------------
#-----------------------------------------------------------------------------------------
#   testing process:
#   user login with MyRider@example and edit her/his profile.
#   create ride offer
#   log out
#   another user login and this user should be able to see first user's profile by clicking first user's name from home page
#------------------------------------------------------------------------------------------

from tools.selenium import selenium
import unittest, time, re

class NewTest(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 5555, "*iexplore", "http://localhost:8080/")
        self.selenium.start()
    
    def test_new(self):
        sel = self.selenium
        sel.open("/")
        sel.click("link=Log In")
        sel.wait_for_page_to_load("30000")
        sel.type("email", "MyRider@example.com")
        sel.click("submit-login")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Offer Ride")
        sel.wait_for_page_to_load("30000")
        sel.click("link=My Profile")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Edit")
        sel.wait_for_page_to_load("30000")
        sel.type("id_first_name", "My")
        sel.type("id_last_name", "Rider")
        sel.select("id_town", "label=Auckland")
        sel.type("id_phone", "0213456789")
        sel.click("//input[@value='Save']")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Offer Ride")
        sel.wait_for_page_to_load("30000")
        sel.select("id_source", "label=Amberley")
        sel.select("id_destination", "label=Bulls")
        sel.select("date_day", "label=18")
        sel.select("date_month", "label=March")
        sel.select("date_year", "label=2010")
        sel.select("time_time", "label=9:00am")
        sel.type("id_available_seats", "2")
        sel.type("id_notes", "testing")
        sel.click("//input[@value='Save']")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Log Out")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Log In")
        sel.wait_for_page_to_load("30000")
        sel.click("submit-login")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Home")
        sel.wait_for_page_to_load("30000")
        sel.click("link=MyRider")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Email: MyRider@example.com \nHometown: Auckland \nPhone: 0213456789", sel.get_text("//div[@id='main']/p/code"))
        self.assertEqual("My Rider", sel.get_text("//div[@id='main']/h3"))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
