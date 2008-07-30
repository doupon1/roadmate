-------------------------------------------------------------------------------
	RoadMate - README
-------------------------------------------------------------------------------

:: Introduction ::
RoadMate is a web based application, designed to support users in organising
car pooling between locations.

RoadMate is built on-top of the Google App Engine framework.

:: Directory Structure ::
The following is an outline of RoadMate's directory structure:

--	./data
	
	A collection of line delimited text files. 
	
	These contain static data, which is loaded into RoadMate's database when 
	is it is first run on a new system.
				
	E.g. Lists of towns, geographical data .etc.
				
	The rational behind this, is that text files play much more nicely with 
	version control systems than binary datastores.
				
--	./images
	
	Images used by RoadMate.

--	./pages

	RoadMate's site pages and their corresponding python files.
	
--	./roadmate

	Python packages containing classes used by RoadMate.
	
	E.g. Data Models, Helper Classes .etc.
	
--	./stylesheets

	RoadMate's Cascading Style Sheets and their accompanying files.