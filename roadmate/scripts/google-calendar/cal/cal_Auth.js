/**
 * @author yizhang
 */

    //<![CDATA[

    /*
     * loading gdata library
     */
	google.load("gdata", "1");
	
	/*
	 * init check if user already log into google account
	 */
    google.setOnLoadCallback(init_display);
    
	
	
	/*
	 * set up google Authsub log in and log out function
	 * 
	 * 
	 */
	var myService;
	var scope= "http://www.google.com/calendar/feeds/";
    //var feedUrl = "http://www.google.com/calendar/feeds/roadmategroup@gmail.com/private/full";
	var feedUrl = 'http://www.google.com/calendar/feeds/default/private/full';
 
  

	
	
  

    function logMeIn() {
    //scope = "http://www.google.com/calendar/feeds/";
    var token = google.accounts.user.login(scope);
    }

   /* function setupMyService() {
    myService = new google.gdata.calendar.CalendarService('roadmate-App-1');
    logMeIn();
    }*/
    
	function logMeOut() {
    google.accounts.user.logout();
	
    }
	
	
	//check if user had permission to use roadmate calendar
	function islogin(){
		var i;
		if(google.accounts.user.checkLogin(scope) ){
			i=true;
		}
		else{
			i=false;
		}
		
		return i;
	}
	
	/*
	 * user add event or log in 
	 */
	
	function log_or_add(){
		if (islogin()) {
			insertEvents();
		}
		else{
			logMeIn();
		}
		
	}
	
	//set returning url
	function changeUrl(location){
		window.location.href="http://" + window.location.toString().split("//")[1].split("/")[0] + "/"+location;
		
	}
	
	/*
	 * if user already log into google account, display calendar even contents  
	 * otherwise, display google account log in
	 * 
	 */
   
   
   function clearText(id){
   	
	document.getElementById(id).innerHTML='';
	
   }
   
 

   function getuserid(){
   	
	 return document.getElementById('ride_id').value;
	
   }
   
   
   function init_display(){
   	  
	
   	
      var obj1 = document.getElementById("log_in");
	 var obj2=document.getElementById("add_event");
	  
	
	  
	  
	  
	 
	
	 
   	 if (islogin()) {
	 	
		
		var userid=getuserid();
		obj2.innerHTML="<input id=\"log_bt\" type=\"button\" name=\"add event\" value=\"add event\" onclick=\"insertEvents();\"  /><input id=\"out_bt\" type=\"button\" name=\"addevent\" value=\"logout\" onclick=\"logMeOut();refresh(\'cal_Authlogin?id="+userid+"\');\" />" ;
		
	  // obj1.style.display = 'none';
	 
	   //obj2.style.display='show';
		getDatedEvents();
		   
			
			
		}
		else {
		
		
		
		//obj1.style.display = 'show';
		
	    //obj2.style.display ='none';
		
		obj1.innerHTML="Because of using your Google account authentication, you'll need to grant access to it by clicking the \"Login\" button. <input  id=\"log_bt\" type=\"button\" name=\"calendar permission\" value=\"logIn\" onclick=\"logMeIn();\" />";
		
		}
	 
   }
   
   
   function addInnerText(id,words){
	  	
		
			document.getElementById(id).innerHTML = words;
		
	  }
   
   
   /*
    * 
    * refresh current page
    */
   function refresh(newurl)
{
    //  This version does NOT cause an entry in the browser's
    //  page view history.  Most browsers will always retrieve
    //  the document from the web-server whether it is already
    //  in the browsers page-cache or not.
    //  
    window.location.replace( newurl );
}


	 
	 

	
 


// create current event

function  creat_event_list(){
	var eventset=["name","from","to","startTime","endTime"];
	 var temp=new Array();
	for(var i in eventset){
		if (document.getElementById(eventset[i]) != undefined) {
			temp[eventset[i]] = document.getElementById(eventset[i]).innerHTML;
		}
	
	 };
	
	return temp;
	
	
}
  
  
 
 
 
 
  
/*
 * insert a event into RoadMate Calendar.
 * 
 */
   
   
   function insertEvents(){
   	
	
   var myService = new google.gdata.calendar.CalendarService('roadmate-App-1');


   var feedUri = 'http://www.google.com/calendar/feeds/default/private/full';


   var entry = new google.gdata.calendar.CalendarEventEntry();


   var eventList=creat_event_list();
   
  
 
 
  entry.setTitle(google.gdata.Text.create('road mate ride offer'));
   
  //set location
 var where =new google.gdata.Where();
   where.setValueString('From '+eventList["from"]+' to '+ eventList['to']);
  entry.addLocation(where);
   
   
	
	

// Create a When object that will be attached to the event
   var when = new google.gdata.When();

// Set the start and end time of the When object
  var startTime = google.gdata.DateTime.fromIso8601(eventList["startTime"]);
  var endTime = google.gdata.DateTime.fromIso8601(eventList["endTime"]);
   when.setStartTime(startTime);
  when.setEndTime(endTime);
  
 
  
  var reminder = new google.gdata.Reminder();

// Set the reminder to be 30 minutes prior the event start time
reminder.setMinutes(1440);

// Set the reminder method to be all, sms pop up email.
reminder.setMethod(google.gdata.Reminder.METHOD_EMAIL  );

// Add the reminder with the When object
  when.addReminder(reminder);



// Add the When object to the event
   entry.addTime(when);
 
 

// The callback method that will be called after a successful insertion from insertEntry()
  var callback = function(result) {
  alert('event created!');
}

// Error handler will be invoked if there is an error from insertEntry()
   var handleError = function(error) {
  alert(error);
}

// Submit the request using the calendar service object
   myService.insertEntry(feedUrl, entry, callback,
    handleError, google.gdata.calendar.CalendarEventEntry);
	
	
   }
   
   
   
   //get calendar events had title ride offer
   
   function getDatedEvents() {
  //var calendblogger = {};
  //var calendarService = 
  var calendarService = new google.gdata.calendar.CalendarService('roadmate-App-1');
   CALENDAR_FEED_URL = 'http://www.google.com/calendar/feeds/default/private/full';

  DISPLAY_DIV = '#display';
  $(DISPLAY_DIV).empty();
  
  var searchText = 'road mate ride offer';

// Create a CalendarEventQuery, and specify that this query is
// applied toward the "private/full" feed
var query = new google.gdata.calendar.CalendarEventQuery(CALENDAR_FEED_URL);

// Set the query with the query text
query.setFullTextQuery(searchText);
  
  

 /* following code can be query time if we need to add this function
  * 
  * var query = 
      new google.gdata.calendar.CalendarEventQuery(
      CALENDAR_FEED_URL);
	  
	  var startMin = google.gdata.DateTime.fromIso8601(startDate);
var startMax = google.gdata.DateTime.fromIso8601(endDate);
query.setMinimumStartTime(startMin);
query.setMaximumStartTime(startMax);*/

  // Set the start-min 
  //query.setMinimumStartTime();
 
  // Set the start-max
  //query.setMaximumStartTime(new google.gdata.DateTime(endDate, true));
  
  var handleError = function(error) {
  alert(error);
}

  calendarService.getEventsFeed(
    query, 
    function(root) {
      var entries = root.feed.getEntries();

      //var html = [];
	  var temp=[];
	  var output='';

      for (var i = 0, entry; entry = entries[i]; i++ ) {

        var title = entry.getTitle().getText();

        // if content is empty, replace it with "---"
       /* var content = 
            (entry.getContent().getText() == undefined) ? '---' : 
            entry.getContent().getText();*/
        var creators = '';
        var locations = '';
        var times = '';

        for (var j = 0, author; author = entry.getAuthors()[j]; j++) {
          var creatorName = author.getName().getValue();
          creators += creators + ' ' + creatorName;
        }

        for (var j = 0, location; location = entry.getLocations()[j]; j++) {

          // if location is empty, replace it with "---"
          var locationLabel = (location.getValueString()  == undefined) ? 
              '---' : entry.getLocations()[j].getValueString();
          locations += locations + ' ' + locationLabel;
        }

        for (var j = 0, time; time = entry.getTimes()[j]; j++) {

          var timeLabel = time.getStartTime().getDate().
              toLocaleString() + '  to : ' + entry.getTimes()[j].
              getEndTime().getDate().toLocaleString()
          times += times + ' ' + timeLabel;
        }

        
	  temp.push('Title: ' + title+'<br/> '+'Organizer(s): ' + creators+' <br/>'+'When: ' + times+' <br/>'+'Where: ' + locations+' '+' <br/><br/>  ');
       
      
	  
	  }     

      //if (entries.length > 0) {
      //  printToDisplay(html.join('<br>'));  
     // }
	   for(var st in temp){
	   	
		  output=output+temp[st];
	   }
	  document.getElementById('display').innerHTML=output;
	   
         
    }, 
	
	
    handleError
  );  

}


   
   
    //]]>
    