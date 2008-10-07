#----------------------------Test Use case 3.2--------------------------------------


from tools.selenium import selenium
import unittest, time, re

class NewTest(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 5555, "*iexplore", "http://localhost:8080/")
        self.selenium.start()
    
    def test_new(self):
        sel = self.selenium
        sel.open("/browse")
        sel.click("link=Log In")
        sel.wait_for_page_to_load("30000")
        sel.click("submit-login")
        sel.wait_for_page_to_load("30000")
        sel.click("link=My Profile")
        sel.wait_for_page_to_load("30000")
        sel.click("//div[@id='main']/table/tbody/tr[2]/td[4]/a")
        sel.wait_for_page_to_load("30000")
        sel.select("id_destination", "label=Christchurch")
        sel.select("date_day", "label=10")
        sel.select("date_month", "label=October")
        sel.select("time_time", "label=11:00pm")
        sel.type("id_available_seats", "2")
        sel.type("id_notes", "edit")
        sel.click("//input[@value='Save']")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Akaroa to Christchurch, 2008-10-10", sel.get_text("//div[@id='main']/h3"))
        self.assertEqual("Owner test@example.com\nFrom Akaroa to Christchurch\nOn 2008-10-10 departing at 23:00:00\nSeats Available 2\nNotes\nedit", sel.get_text("//div[@id='main']/p[1]/code"))
        sel.click("link=My Profile")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
