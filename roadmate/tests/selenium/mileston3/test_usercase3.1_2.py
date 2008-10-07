import unittest, time, re

from tools.selenium import selenium

#---------------------------------------------------------
#give empty inputs of source , destination.
#give same arrive depature time and arrival time
#
#expected out put : system should prompt hit 
#
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
        sel.click("//input[@value='Create']")
	self.assertEqual("Please choose a source address.", sel.get_text("//div[@id='main']/form/ul/li[1]"))
        self.assertEqual("Please choose a destination address.", sel.get_text("//div[@id='main']/form/ul/li[2]"))
        self.assertEqual("Depature time must be before arrival time.", sel.get_text("//div[@id='main']/form/ul/li[3]"))
        #sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
