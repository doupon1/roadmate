#---------------------------------------------------------------------------------------------
#Related to Use Case 3.1
#
#
#
#----------------------------------------------------------------------------------------------


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
        sel.click("link=Offer Ride")
        sel.wait_for_page_to_load("30000")
        sel.click("submit-login")
        sel.wait_for_page_to_load("30000")
        sel.select("id_destination", "label=Ashburton")
        sel.select("date_day", "label=11")
        sel.select("date_month", "label=November")
        sel.type("id_notes", "test")
        sel.click("//input[@value='Save']")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Akaroa to Ashburton, 2008-11-11", sel.get_text("//div[@id='main']/h3"))
        self.assertEqual("Owner test@example.com\nFrom Akaroa to Ashburton\nOn 2008-11-11 departing at 00:00:00\nSeats Available 1\nNotes\ntest", sel.get_text("//div[@id='main']/p[1]/code"))
        sel.click("link=Edit")
        sel.wait_for_page_to_load("30000")
        sel.select("id_destination", "label=Blenheim")
        sel.select("date_day", "label=10")
        sel.select("date_month", "label=December")
        sel.select("date_month", "label=November")
        sel.select("time_time", "label=1:00am")
        sel.type("id_available_seats", "2")
        sel.type("id_notes", "testing")
        sel.click("//input[@value='Save']")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Akaroa to Blenheim, 2008-11-10", sel.get_text("//div[@id='main']/h3"))
        self.assertEqual("Owner test@example.com\nFrom Akaroa to Blenheim\nOn 2008-11-10 departing at 01:00:00\nSeats Available 2\nNotes\ntesting", sel.get_text("//div[@id='main']/p[1]/code"))
        sel.click("link=Home")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Akaroa - Blenheim", sel.get_table("//div[@id='main']/table.1.0"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.assertEqual("2008-11-10", sel.get_text("//div[@id='main']/table/tbody/tr[2]/td[2]"))
        self.assertEqual("2", sel.get_text("//div[@id='main']/table/tbody/tr[2]/td[3]"))
        self.assertEqual("test", sel.get_table("//div[@id='main']/table.1.3"))

    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
