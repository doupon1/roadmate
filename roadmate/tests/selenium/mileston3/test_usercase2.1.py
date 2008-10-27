import unittest, time, re

from tools.selenium import selenium

#---------------------------------------------------------
#user log in
#user can manage profile by edit firstname lastname hometwon phone
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
        sel.click("//div[@id='sidebar']/ul/li[2]/a")
        sel.wait_for_page_to_load("30000")
        sel.click("submit-login")
        sel.wait_for_page_to_load("30000")
        sel.click("first_name")
        sel.type("value", "test")
        sel.click("last_name")
        sel.type("//form[@id='last_name-inplaceeditor']/input", "test")
        sel.click("town")
        sel.type("//form[@id='town-inplaceeditor']/input", "test")
        sel.click("phone")
        sel.type("//form[@id='phone-inplaceeditor']/input", "test")
        sel.click("link=save")
        sel.click("link=save")
        sel.click("link=save")
        sel.click("link=save")
        #sel.click("//div[@id='sidebar']/ul/li[1]/a")
        #sel.wait_for_page_to_load("30000")
        #sel.click("//div[@id='sidebar']/ul/li[2]/a")
        #sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()



