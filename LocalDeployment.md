## Step 1: Install Google App Engine ##
Google App Engine : [Download link](http://code.google.com/appengine/downloads.html)

## Step 2: Checkout working copy of RoadMate ##
Details on how to checkout a copy of RoadMate can be found on the [RoadMate checkout page](http://code.google.com/p/roadmate/source/checkout).

  * The **latest release** can be checked out from _/svn/trunk/roadmate/_
  * For **stable releases** see _/svn/tags/_

## Step 3: Run RoadMate ##
You can now test RoadMate with the web server included with the App Engine SDK.

Start the web server with the following command, giving it the path to the _roadmate_ directory:
```
google_appengine/dev_appserver.py roadmate
```