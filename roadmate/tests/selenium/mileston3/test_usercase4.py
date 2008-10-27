import unittest, time, re

from tools.selenium import selenium

#---------------------------------------------------------
#
#test support page link
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
        sel.click("link=Support")
        
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
