import unittest, time, re

from tools.selenium import selenium

#---------------------------------------------------------
#After user create a new ride offer
#user can view ride offer by click this ride offer from home page
#---------------------------------------------------------

#self.selenium = selenium("localhost", 5555, "*iexplore", "http://localhost:8080/")


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
        sel.type("id_source_address", "Palmerston North")
        sel.type("id_destination_address", "Wellington")
        sel.select("departure_time_time", "label=7:00am")
        sel.select("arrival_time_time", "label=9:00am")
        sel.type("id_number_of_seats", "5")
        sel.type("id_notes", "de")
        sel.click("//input[@value='Create']")
        #sel.wait_for_page_to_load("30000")
        sel.click("link=Manage My Rides")
        #sel.wait_for_page_to_load("30000")
        #sel.click("//div[@id='main']/table/tbody/tr[21]/td/strong/a")
        #sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()



