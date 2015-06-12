## HowTo: Setup Selenium Server ##

  1. Download selenium-remote-control-1.0-beta-1-dist.zip file from http://archiva.openqa.org/repository/releases/org/openqa/selenium/selenium-remote-control/1.0-beta-1/
  1. Unzip this file. You will get selenium-remote-control-1.0-beta-1 folder.
  1. Install JDK1.5 or higher. See how to setup java path http://www.ics.uci.edu/~thornton/ics22/LabManual/SettingUpJava.html .
  1. I assume that your selenium-remote-control-1.0-beta-1 folder located at d:\ selenium-remote-control-1.0-beta-1.(see step 2)
  1. Start-->Run--->type cmd
  1. cd  d:\selenium-remote-control-1.0-beta-1\selenium-server-1.0-beta-1
  1. java -jar selenium-server.jar -port 5555
  1. if you see following lines from you console , your selenium romote control server is running now.
  * 23:11:58.125 INFO - Java: Sun Microsystems Inc. 10.0-b19
  * 23:11:58.125 INFO - OS: Windows XP 5.1 x86
  * 23:11:58.125 INFO - v1.0-beta-1 [2201](2201.md), with Core v1.0-beta-1 [1994](1994.md)
  * 23:11:58.265 INFO - Version Jetty/5.1.x
  * 23:11:58.265 INFO - Started HttpContext[/selenium-server/driver,/selenium-serve/driver]
  * 23:11:58.265 INFO - Started HttpContext[/selenium-server,/selenium-server]
  * 23:11:58.265 INFO - Started HttpContext[/,/]
  * 23:11:58.375 INFO - Started SocketListener on 0.0.0.0:5555
  * 23:11:58.390 INFO - Started org.mortbay.jetty.Server@32c41a




## HowTo: Run Unit Tests At Local Host ##
  1. Setup your google app engine at port 8080 (http://localhost:8080/).
  1. Run roadmate web application from localhost  eg: dev\_appserver.py ./roadmate
  1. Run selenium server.
  1. Check out tests folder from google code repository /trunk/roadmate/tests.
  1. cd d:\tests  (Assuming your checkout tests folder is located at your computer d:\tests.)
  1. Now you can run your unit test cases. eg: python test\_rideoffer.py
  1. From console window , you will be able to see test results.


## HowTo: Run Unit Tests At Massey Host ##

  1. Run selenium server.
  1. Check out tests folder from google code repository /trunk/roadmate/tests.
  1. cd d:\tests  (Assuming your checkout tests folder is located at your computer d:\tests.)
  1. Modify your test case python file. Change "http://localhost:8080/ to "http://seat-web3.massey.ac.nz:8080/" eg: edit test\_rideoffer.py code :
```
def setUp(self):
        #change "http://localhost:8080/" to "http://seat-web3.massey.ac.nz:8080/"
        self.selenium = selenium("localhost", 5555, "*iexplore","http://localhost:8080/")
```
  1. Now you can run your unit test cases. eg: python test\_rideoffer.py
  1. From console window , you will be able to see test results.