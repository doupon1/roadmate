from selenium import selenium
import unittest, time, re




class NewTest(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 5555, "*iexplore", "http://localhost:8080/")
        self.selenium.start()
        #usual case:
        self.testcase=(["label=Alexandra","label=Ashburton","label=2","label=February","label=2009","label=12:30am","4","A"],\
                   ["label=Alexandra","label=Auckland","label=4","label=March","label=2008","label=11:00am","5","B"],\
                   ["label=Brighton","label=Coromandel","label=11","label=May","label=2010","label=10:00am","6","c"],\
                    ["label=Dargaville","label=Drury","label=14","label=July","label=2009","label=1:00pm","1","D"],\
                    ["label=Dunedin","label=Duntroon","label=16","label=June","label=2008","label=2:00pm","2","E"],\
                ["label=Edgecumbe","label=Eltham","label=19","label=July","label=2011","label=1:00pm","40","D"],\
                 ["label=Fairlie","label=Drury","label=21","label=April","label=2009","label=3:00pm","50","E"],\
                 ["label=Dargaville","label=Glenorchy","label=22","label=October","label=2012","label=4:00pm","30","F"])
        #unavailable input:
        self.badcase=(["label=Dargaville","label=Glenorchy","label=31","label=February","label=2012","label=4:00pm","30","F"],\
                     ["label=Dunedin","label=Duntroon","label=16","label=June","label=2008","label=5:00pm","0","E"],\
                     ["label=Dunedin","label=Duntroon","label=16","label=June","label=2008","label=5:00pm","-42","E"],\
                     ["label=Dunedin","label=Duntroon","label=16","label=June","label=2008","label=5:00pm","1000","E"],\
                      ["label=Dunedin","label=Duntroon","label=16","label=June","label=2008","label=5:00pm","aAS","E"])
        
        self.monthdic={"January":"01","February":"02", "March":"03", "April":"04", "May":"05", "June":"06", "July":"07", "August":"08", "September":"09", "October":"10", "November":"11","December":"12"}
        self.daydic={"1":"01","2":"02","3":"03","4":"04","5":"05","6":"06","7":"07","8":"08","9":"09","10":"10","11":"11","12":"12","13":"13",\
                 "14":"14","15":"15","16":"16","17":"17","18":"18","19":"19","20":"20","21":"21","22":"22","23":"23","24":"24",\
             "25":"25","26":"26","27":"27","28":"28","29":"29","30":"30","31":"31"}
                
    
    def test_new(self):
        self.error=" "
        sel = self.selenium
        sel.open("/")
        sel.click("link=Offer Ride")
        sel.wait_for_page_to_load("30000")
        sel.click("submit-login")
        sel.wait_for_page_to_load("30000")
        
        for case in self.testcase:
            sel.select("id_source", case[0])
            sel.select("id_destination", case[1])
            sel.select("date_day", case[2])
            sel.select("date_month", case[3])
            sel.select("date_year", case[4])
            sel.select("time_time", case[5])
            sel.type("id_available_seats", case[6])
            sel.type("id_notes", case[7])
            sel.click("//input[@value='Save']")
            sel.wait_for_page_to_load("30000")
            t1=case[5][6:-2]
            t2=case[5][-2:]
            
            if len(t1)==4:
                t1="0"+t1+":00"
            else:
                t1=t1+":00"
            
            if t2=="am":
                if t1[0:2]=="12":
                    t1="00"+t1[2:]
            else:
                if t1[0:2]=="12":
                    pass
                else:
                    temp=int(t1[0:2])
                    temp=temp+12
                    t1=str(temp)+t1[2:]
                    
                
                
            
            #input value should same as output expected value.   
            self.assertEqual("Owner test@example.com\nFrom "+case[0][6:]+" to "+case[1][6:]+"\nOn "+case[4][6:]+"-"+self.monthdic[case[3][6:]]+"-"+self.daydic[case[2][6:]]+" departing at "+t1+"\nSeats Available "+case[6]+"\nNotes\n"+case[7], sel.get_text("//div[@id='main']/p[1]/code"))
       
            sel.click("link=Offer Ride")
            sel.wait_for_page_to_load("30000")
       
    
    def test_wrong_day_input(self):
        self.pattern_validation(0)
    
    def test_zero_seats_input(self):
        self.pattern_validation(1)
    
    def test_negative_seats_input(self):
        self.pattern_validation(2)
    
    def test_large_seats_input(self):
        self.pattern_validation(3)
    
    def test_wrongtype_seats_input(self):
        self.pattern_validation(4)
    
   
    
    def pattern_validation(self,row):
        sel = self.selenium
        sel.open("/")
        sel.click("link=Offer Ride")
        sel.wait_for_page_to_load("30000")
        sel.click("submit-login")
        sel.wait_for_page_to_load("30000")
        
        
        sel.select("id_source", self.badcase[row][0])
        sel.select("id_destination", self.badcase[row][1])
        sel.select("date_day", self.badcase[row][2])
        sel.select("date_month", self.badcase[row][3])
        sel.select("date_year", self.badcase[row][4])
        sel.select("time_time", self.badcase[row][5])
        sel.type("id_available_seats", self.badcase[row][6])
        sel.type("id_notes", self.badcase[row][7])
        sel.click("//input[@value='Save']")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Create Ride Offer", sel.get_text("//div[@id='main']/h2"))
        
   
        
        
    
    
        
    def makeNewTestSuite():
        suite = unittest.TestSuite()
        suite.addTest(NewTest("test_new"))
        suite.addTest(NewTest("test_wrong_day_input"))
        suite.addTest(NewTest("test_zero_seats_input"))
        suite.addTest(NewTest("test_negative_seats_input"))
        suite.addTest(NewTest("test_large_seats_input"))
        suite.addTest(NewTest("test_wrongtype_seats_input"))
        return suite

    def suite():
        return unittest.makeSuite(NewTest)

        
        
       
    
    def tearDown(self):
        #self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
