#!/usr/bin/python

# ----------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------

import tools.unitest as unittest

from tools.selenium import selenium

# ----------------------------------------------------------------------------
#  Unit Tests
# ----------------------------------------------------------------------------

class ProfilePageTest(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 5555, "*iexplore", "http://localhost:8080/")
        self.selenium.start()
        
        self.owners=(["owner1@example.com","Akaroa","061234567"],["test@example.com","Arrowtown","061234567"],["owner2@example.com","Bluff","061010101"])
        
    def test_owner1(self):
        self.pattern(0)
        
    def test_owner2(self):
        self.pattern(1)
        
    def test_owner3(self):
        self.pattern(2)
        
    def pattern(self,owner_idex):
        sel = self.selenium
        
        sel.open("/")
        sel.click("link=My Profile")
        sel.wait_for_page_to_load("30000")
        sel.type("email", self.owners[owner_idex][0])
        sel.click("submit-login")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Email: "+self.owners[owner_idex][0]+" \nHometown: "+self.owners[owner_idex][1]+" \nPhone: "+self.owners[owner_idex][2], sel.get_text("//div[@id='main']/p[1]/code"))
    
    def editpattern(self,owner_index):
        sel = self.selenium
        sel.open("/")
        sel.click("link=My Profile")
        sel.wait_for_page_to_load("30000")
        sel.type("email", self.owners[owner_index][0])
        sel.click("submit-login")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Email: test@example.com \n Hometown: Akaroa \n Phone: 061234567", sel.get_text("//div[@id='main']/p[1]/code"))
        sel.click("link=Edit")
        sel.wait_for_page_to_load("30000")
        sel.type("id_first_name", "ownerchange")
        sel.type("id_last_name", "owner")
        sel.select("id_town", "label=Arrowtown")
        sel.click("//input[@value='Save']")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("ownerchange owner", sel.get_text("//div[@id='main']/h3"))
        self.assertEqual("Email: test@example.com \n Hometown: Arrowtown \n Phone: 061234567", sel.get_text("//div[@id='main']/p[1]/code"))
        
        
    
    def tearDown(self):
        self.selenium.stop()

if __name__ == "__main__":
    unittest.main()
