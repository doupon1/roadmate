/**
 * @author yizhang
 */

    //<![CDATA[
	
	
	
	var myService;
	var scope= "http://www.google.com/calendar/feeds/";
    var feedUrl = 'http://www.google.com/calendar/feeds/default/private/full';
	
	
	// button change for create or remove calendar reminder. 
   var createbutton="<input id=\"create\" class=\"button\" type=\"button\" value=\"Create\" onClick=\"insertEvents(); setTimeout('showRemoveBt()', 3000);return false; \"/>";
   var removebutton="<input id=\"remove\" class=\"button\" type=\"button\" value=\"Remove\" onClick=\"var hiddencal_id=document.getElementById('ride_id').value; deleteEvent(hiddencal_id);setTimeout('showCreateBt()', 3000); return false;\"/> ";
    
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
	
	
	/**
 * Detect whether the current session is a token redirect
 * @return {Boolean} True/false to whether this is a redirect session
 */  
    function isTokenRedirect() {

         var status = false;

         var url = location.href;

          var matchArr = url.match(/#2/);
  
        if (matchArr != null) {
           status = true;
         }
		 
		 

  return status;
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
   
   //add text to a field
     function addInnerText(id,words){
	  	
		
			document.getElementById(id).innerHTML = words;
		
	  }
	  
	  //display romove button
	  
	  function showRemoveBt(){
	  	  
		  clearText('addcalendar'); 
		  addInnerText('addcalendar',removebutton);
		
		
	  }
	  
	  function showCreateBt(){
	  	
		clearText('addcalendar'); 
		addInnerText('addcalendar',createbutton);
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
   	  google.gdata.client.init();
	  
	  
			  //alert(isIncal+"");
   	
      var obj1 = document.getElementById("log_in");
	  var obj2=document.getElementById("add_event");
	  var obj3=document.getElementById("wait");
	 

	 
	   if (isTokenRedirect()) {
	   	     
			 	obj1.style.display = 'none';
			 	obj2.style.display = 'none';
			 	obj3.style.display = 'block';
				
			   
				setTimeout('showcreatefiled()',5000);
	   	   
				
				 
			 
			 
	   
	   }
	   
	   
	   else {
	   	    
			
			  
		   
	     	if (islogin()) {
	   	
	   	         obj2.style.display = 'block';
	   		     obj1.style.display = 'none';
			     obj3.style.display = 'none';
				// alert('login');
				 
				 var searchText=document.getElementById('ride_id').value;
				
	               checkIncal(searchText);
				    
			    
	           }
	   	    else {
	   	
	   		   obj2.style.display = 'none';
	   		   obj1.style.display = 'block';
	   		   obj3.style.display = 'none';
	   		
	   		
	   	    }
	   }
	 
   }
   
   
   //show createbutton
   
   function displayCreatbt(){
   	  var obj1 = document.getElementById("log_in");
	  var obj2=document.getElementById("add_event");
	  var obj3=document.getElementById("wait");
	     obj2.style.display = 'block';
	     obj1.style.display = 'none';
	     obj3.style.display = 'none'; 
		  
		  document.getElementById('addcalendar').innerHTML=createbutton;
		  
   }
   
   
   //show removebutton
   function displayRemovebt(){
   	   var obj1 = document.getElementById("log_in");
	  var obj2=document.getElementById("add_event");
	  var obj3=document.getElementById("wait");
	     obj2.style.display = 'block';
	     obj1.style.display = 'none';
	     obj3.style.display = 'none'; 
		  
		  document.getElementById('addcalendar').innerHTML=removebutton;
   }
   
   
   
   //block create field
   function blockCreate(){
   	var obj2=document.getElementById("add_event");
   	obj2.style.display='block';
	
   }
  
   //show create filed
   
   function showcreatefiled(){
   	   var obj1 = document.getElementById("log_in");
	   var obj2=document.getElementById("add_event");
	   var obj3=document.getElementById("wait");
	            obj2.style.display = 'block';
	   		    obj1.style.display = 'none';
			    obj3.style.display = 'none';
		var searchText=document.getElementById('ride_id').value;
				
	               checkIncal(searchText);		
	
	
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
		 /*if(remindMethod.length==0){
		 	remindMethod[0]="email";
		 }*/
		 return remindMethod;
	  }

    //get text value of select box.
	function getSelectedValue(id)
   {   
       
       var selection=document.getElementById(id);
       var option=selection.options[selection.selectedIndex].text;
       
       return option;
   }


    //get email or sms reminde time
      function getRiminderTime(timeBase, remindTime ){
		   	
			    // Set the reminder time prior the event start time
			var remindTime;
			var timeBase=getSelectedValue(timeBase);
			var selectNumber=getSelectedValue(remindTime);
			
			
			
			if(timeBase=="minutes"){
				
				var temp=parseInt(selectNumber);
				if(temp<5){
					remindTime=5;
				}else{
					remindTime=temp;
				}
			}
			if(timeBase=="hours"){
				remindTime=parseInt(selectNumber)*60;
			}
			if(timeBase=="days"){
				remindTime=parseInt(selectNumber)*24*60;
			}
		   	
			return remindTime;
			
		 }

  
 //insert a event into RoadMate Calendar.
 
   
      function insertEvents(){
   	
	
              var myService = new google.gdata.calendar.CalendarService('roadmate-App-1');
			  var feedUri = 'http://www.google.com/calendar/feeds/default/private/full';
              var entry = new google.gdata.calendar.CalendarEventEntry();
			  var calendar_id=document.getElementById('ride_id').value;
			  
			  var extendedProperty = new google.gdata.ExtendedProperty();
			  extendedProperty.setName("com.roadmate.rideid");
			  extendedProperty.setValue(calendar_id);
			  entry.addExtendedProperty(extendedProperty);

			  
              var eventList=creat_event_list();
			  
              entry.setTitle(google.gdata.Text.create('RoadMate Ride'));
			  
			  //set hindden field for search title
			  
			 // document.getElementById("calendar_id").value=eventTilte;
			  
			  
   
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
  
             var reminder1 = new google.gdata.Reminder();
			 var reminder2 = new google.gdata.Reminder();
			 //user can choose remind method
			 var remindMethod=getRemindtype();


            //get switch value
            var switchvalue=0;
			
			if(remindMethod.length==0){
				switchvalue=0;
				
			}
			
			

            for(var i=0;i<remindMethod.length;i++) {
			
				if (remindMethod[i] == "email") {
				
					var time1 = getRiminderTime('timeBase1', 'remindTime1');
					reminder1.setMinutes(time1);
					reminder1.setMethod(google.gdata.Reminder.METHOD_EMAIL);
					switchvalue=1;
					
				}
				if (remindMethod[i] == "sms") {
					var time2 = getRiminderTime('timeBase2', 'remindTime2');
					reminder2.setMinutes(time2);
					reminder2.setMethod(google.gdata.Reminder.METHOD_SMS);
					switchvalue=2;
				}
				
			}
              if(remindMethod.length==2){
				switchvalue=3;
			}
			  
			  // Add the reminder with the When object
			  switch(switchvalue)
              {
                   case 0:
				     reminder1.setMethod(google.gdata.Reminder.METHOD_NONE);
					 when.addReminder(reminder1);
					break; 
                   case 1:
                    when.addReminder(reminder1);
                     break;
                   case 2:
                    when.addReminder(reminder2);
                     break;
				   case 3:
                     when.addReminder(reminder1);
			         when.addReminder(reminder2);
					 break;
  
               }
            
             

           // Add the When object to the event
              entry.addTime(when);
 
           // The callback method that will be called after a successful insertion from insertEntry()
             var callback = function(result) {
			 	
			// document.getElementById('calendar_id').value= calendar_id;
			 //alert(hiddencal_id);
			 //var removelink="<a href=\"#\" onClick=\"deleteEvent("+hiddencal_id+"); alert(hiddencal_id);return false;\" > remove </a>"
             //addInnerText('addcalendar',removelink);
             }

             // Error handler will be invoked if there is an error from insertEntry()
             var handleError = function(error) {
             alert(error);
             }

             // Submit the request using the calendar service object
             myService.insertEntry(feedUrl, entry, callback,
              handleError, google.gdata.calendar.CalendarEventEntry);
	         }
   
   
   
           

 

//delete a event
      function deleteEvent(searchText){
	  	       

                    // Create the calendar service object
              var calendarService = new google.gdata.calendar.CalendarService('roadmate-App-1');

               // The default "private/full" feed is used to delete existing event from the
               // primary calendar of the authenticated user
              var feedUri = 'http://www.google.com/calendar/feeds/default/private/full?extq=[com.roadmate.rideid:' + searchText + ']';



               // Create a CalendarEventQuery, and specify that this query is
               // applied toward the "private/full" feed
              var query = new google.gdata.calendar.CalendarEventQuery(feedUri);

             // This callback method that will be called when getEventsFeed() returns feed data
              var callback = function(result) {

                // Obtain the array of matched CalendarEventEntry
              var entries = result.feed.entry;

               // If there is matches for the full text query
             if (entries.length > 0) {
			 	
				//alert('entry found');

                     // delete the first matched event entry  
                  var event = entries[0];
                 event.deleteEntry(
                 function(result) {
                     // alert('event deleted!');
                   },
                     handleError);
                 } else {
                     // No match is found for the full text query
                     //alert('Cannot find event(s) with text: ' + searchText);
                  }
               }

               // Error handler to be invoked when getEventsFeed() or updateEntry()
                // produces an error
               var handleError = function(error) {
                     //alert(error);
                  }

               // Submit the request using the calendar service object
                calendarService.getEventsFeed(query, callback, handleError);
	           }
 
 
  //check if ride_id  already in calendar
   function   checkIncal(searchText){
	  	       
			  
              
                    // Create the calendar service object
              var calendarService = new google.gdata.calendar.CalendarService('roadmate-App-1');

               // The default "private/full" feed is used to delete existing event from the
               // primary calendar of the authenticated user
              var feedUri = 'http://www.google.com/calendar/feeds/default/private/full?extq=[com.roadmate.rideid:' + searchText + ']';



               // Create a CalendarEventQuery, and specify that this query is
               // applied toward the "private/full" feed
              var query = new google.gdata.calendar.CalendarEventQuery(feedUri);
			  
			  

             // This callback method that will be called when getEventsFeed() returns feed data
              var callback = function(result) {

                // Obtain the array of matched CalendarEventEntry
              var entries = result.feed.entry;

               // If there is matches for the full text query
             if (entries.length > 0) {
			 	
				displayRemovebt();
				
				
				 
				 
				 
				    } else {
				 	
			      
				  displayCreatbt();
				 
					
                    
                  }
               }

               // Error handler to be invoked when getEventsFeed() or updateEntry()
                // produces an error
               var handleError = function(error) {
                     //alert(error);
					 //displayCreatbt();
                  }

               // Submit the request using the calendar service object
                   calendarService.getEventsFeed(query, callback, handleError);
				
			
				
				
				
	           }
   
   
   
   
    //]]>
    