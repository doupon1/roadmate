from selenium import selenium
import unittest, time, re


#-----------user choose wrong date 31-11-2008-------------
# expected system promote hit
#-------------------------------------------------------------



class NewTest(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 5555, "*iexplore", "http://localhost:8080/")

        self.selenium.start()
    
    def test_new(self):
        sel = self.selenium
        sel.open("/ride_create")
        sel.type("id_source_address", "Alexander st, palmerston north")
        sel.type("id_destination_address", "Linton st, palmerston north")
        sel.select("date_month", "label=November")
        sel.select("date_day", "label=31")
        sel.select("departure_time_time", "label=9:00am")
        sel.select("arrival_time_time", "label=5:00pm")
        sel.select("departure_time_time", "label=4:30pm")
        sel.click("//input[@value='Create']")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
