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
        sel.click("link=My Profile")
        sel.wait_for_page_to_load("30000")
        sel.click("submit-login")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Edit")
        sel.wait_for_page_to_load("30000")
        sel.type("id_first_name", "Test")
        sel.type("id_last_name", "Test")
        sel.select("id_town", "label=Ashburton")
        sel.type("id_phone", "0211234567")
        sel.click("//input[@value='Save']")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Test Test", sel.get_text("//div[@id='main']/h3"))
        self.assertEqual("Email: test@example.com \nHometown: Ashburton \nPhone: 0211234567", sel.get_text("//div[@id='main']/p[1]/code"))
        
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
