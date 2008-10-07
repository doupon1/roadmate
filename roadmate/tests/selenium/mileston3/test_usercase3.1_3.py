import unittest, time, re

from tools.selenium import selenium

#---------------------------------------------------------
#user enters large number of seats number such as:100
#expected that system prompts hit.
#---------------------------------------------------------


class NewTest(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 5555, "*iexplore", "http://localhost:8080/")
        self.selenium.start()
    
    def test_new(self):
        sel = self.selenium
        sel.open("/")
        sel.click("link=Offer A Ride")
        sel.wait_for_page_to_load("30000")
        sel.click("submit-login")
        sel.wait_for_page_to_load("30000")
        sel.type("id_source_address", "Alexander st, palmerston north")
        sel.type("id_destination_address", "Linton st, palmerston north")
        sel.select("date_day", "label=16")
        sel.select("date_month", "label=November")
        sel.select("departure_time_time", "label=1:00am")
        sel.select("arrival_time_time", "label=2:30am")
        sel.type("id_number_of_seats", "400")
        sel.click("//input[@value='Create']")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Number of seats cannot be more than 80.", sel.get_text("//div[@id='main']/form/div[3]/div[1]/ul/li"))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
