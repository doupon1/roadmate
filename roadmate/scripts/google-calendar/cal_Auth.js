/**
 * @author yizhang
 */

    //<![CDATA[
	
	
	
	var myService;
	var scope= "http://www.google.com/calendar/feeds/";
     var feedUrl = 'http://www.google.com/calendar/feeds/default/private/full';

    /*
     * loading gdata library
     */
	google.load("gdata", "1");
	
	/*
	 * init check if user already
	 *  log into google account
	 */
    google.setOnLoadCallback(init_display);
    
	
	
	// set up google Authsub log in and log out function
	
	function logMeIn() {
    
    var token = google.accounts.user.login(scope);
    }

  
    
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
	
	
	 // user add event or log in 
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
	
	
   
   //clear html text field
    function clearText(id){
   	
	document.getElementById(id).innerHTML='';
	
   }
   
 
    //get use id from html page hidden field
     function getuserid(){
   	
	 return document.getElementById('ride_id').value;
	
   }
   
   /*
    * if user already login to google account
    *  display addevent button to user
    * otherwise require user to login google calendar
    * 
    */
     function init_display(){
   	  
	
   	
     var obj1 = document.getElementById("log_in");
	 var obj2=document.getElementById("add_event");
	  
	
	   if (islogin()) {
	 	
		
		
		obj2.style.display='block'
	    obj1.style.display='none';
		
		   
			
			
		}
		else {
		
	      obj2.style.display='none';
		  obj1.style.display='block';
		
		}
	 
   }
   
   
      function addInnerText(id,words){
	  	
		
			document.getElementById(id).innerHTML = words;
		
	  }
   
   
  
    //refresh current page
   
      function refresh(newurl){
   
            window.location.replace( newurl );
      }


	 
	 // create current event

    function  creat_event_list(){
	      var eventset=["name","from","to","startTime","endTime"];
	      var temp=new Array();
	      for(var i in eventset){
		  if (document.getElementById(eventset[i]) != undefined) {
			 temp[eventset[i]] = document.getElementById(eventset[i]).value;
		  }
	
	    };
		
		
	
	  return temp;
	
	}

  //event Id generator
  
     function idgenerate(){
	 	var id=new Array();
		var idString="";
		for (var i = 0; i < 10; i++) {
			var t = Math.floor(Math.random()*11);
			id[i]=t;
		}
	    
		for(var j in id){
			idString=idString+id[j];
		}
		return idString;
	 }
	 
	 
	  //get check box value
      function getRemindtype(){
	  	 var remindMethod=new Array();
		 var j=0;
		 for(var i=0; i < document.remindForm.reminder.length; i++){
             if (document.remindForm.reminder[i].checked) {
			 	remindMethod[j] = document.remindForm.reminder[i].value;
			 	j++;
			 }
			 	
           }
		 if(remindMethod.length==0){
		 	remindMethod[0]="email";
		 }
		 return remindMethod;
	  }

  
 //insert a event into RoadMate Calendar.
 
   
      function insertEvents(){
   	
	
              var myService = new google.gdata.calendar.CalendarService('roadmate-App-1');
			  var feedUri = 'http://www.google.com/calendar/feeds/default/private/full';
              var entry = new google.gdata.calendar.CalendarEventEntry();
              var eventList=creat_event_list();
              entry.setTitle(google.gdata.Text.create('road mate ride offer'+" id "+idgenerate()));
			  
			  
   
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
			 //user can choose remind method
			 var remindMethod=getRemindtype();


            // Set the reminder to be 1440 minutes(1 day) prior the event start time
            reminder.setMinutes(1440);

            // Set the reminder methods, sms or email.
            for (var i = 0; i < remindMethod.length; i++) {
				if (remindMethod[i]=="email") {
					reminder.setMethod(google.gdata.Reminder.METHOD_EMAIL  );
					
					
				}
				if(remindMethod[i]=="sms"){
					reminder.setMethod(google.gdata.Reminder.METHOD_SMS );
					
				}
				
			}

            // Add the reminder with the When object
             when.addReminder(reminder);

           // Add the When object to the event
              entry.addTime(when);
 
           // The callback method that will be called after a successful insertion from insertEntry()
             var callback = function(result) {
             addInnerText('addcalendar','ride has been successfully add into google calendar');
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
                 
                 var calendarService = new google.gdata.calendar.CalendarService('roadmate-App-1');
                  CALENDAR_FEED_URL = 'http://www.google.com/calendar/feeds/default/private/full';

                  DISPLAY_DIV = '#display';
                  $(DISPLAY_DIV).empty();
                
				 var tempEventId=0;
                
                 
                 // Create a CalendarEventQuery, and specify that this query is
                 // applied toward the "private/full" feed
                 var query = new google.gdata.calendar.CalendarEventQuery(CALENDAR_FEED_URL);

                 // Set the query with the query text
                // query.setFullTextQuery(searchText);
                
				query.setFutureEvents();
  

                //error handle function
  
                var handleError = function(error) {
                         alert(error);
                       }

                  calendarService.getEventsFeed(
                         query, 
						 //inner function retieve calendar feeds
                             function(root) {
                              var entries = root.feed.getEntries();

      
	                          var temp=[];
	                          var output='';

                              for (var i = 0, entry; entry = entries[i]; i++ ) {

                              var title = entry.getTitle().getText();

                            
       
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
                                var deleteButton = "<input id=\"delete_bt\" type=\"button\" value=\"delete\" onclick=\"deleteEvent(document.getElementById(\'"+title+"\').innerHTML); clearText("+tempEventId+");\"/>";
                                 var timeLabel = 'Start: '+time.getStartTime().getDate().
                                  toLocaleString() + ' <br\> End : ' + entry.getTimes()[j].
                                  getEndTime().getDate().toLocaleString()
                                  times += times + ' ' + timeLabel;
                                 }

                              temp.push('<span id=\"'+tempEventId+ '\" >'+'<fieldset>'+'Title: ' + '<span id=\"'+title+'\" >'+title+'</span> '+'<br/> '+'Organizer(s): ' + creators+' <br/>' +times+' <br/>'+locations+'<br/>'+deleteButton+'</fieldset> <br/><br/></span>');
                              
							   
							  tempEventId++;
							   
							 }     

      
	                     for(var st in temp){
	   	
		                  output=output+temp[st];
	                     }
	                    // document.getElementById('display').innerHTML=output;
	                             }, 
	
                         handleError);  

             }
			 

 

//delete a event
      function deleteEvent(searchText){
	  	       

                    // Create the calendar service object
              var calendarService = new google.gdata.calendar.CalendarService('GoogleInc-jsguide-1.0');

               // The default "private/full" feed is used to delete existing event from the
               // primary calendar of the authenticated user
              var feedUri = 'http://www.google.com/calendar/feeds/default/private/full';

              

               // Create a CalendarEventQuery, and specify that this query is
               // applied toward the "private/full" feed
              var query = new google.gdata.calendar.CalendarEventQuery(feedUri);

              // Set the query with the query text
             query.setFullTextQuery(searchText);

             // This callback method that will be called when getEventsFeed() returns feed data
              var callback = function(result) {

                // Obtain the array of matched CalendarEventEntry
              var entries = result.feed.entry;

               // If there is matches for the full text query
             if (entries.length > 0) {

                     // delete the first matched event entry  
                  var event = entries[0];
                 event.deleteEntry(
                 function(result) {
                      alert('event deleted!');
                   },
                     handleError);
                 } else {
                     // No match is found for the full text query
                     alert('Cannot find event(s) with text: ' + searchText);
                  }
               }

               // Error handler to be invoked when getEventsFeed() or updateEntry()
                // produces an error
               var handleError = function(error) {
                     alert(error);
                  }

               // Submit the request using the calendar service object
                calendarService.getEventsFeed(query, callback, handleError);
	           }
   
   
    //]]>
    