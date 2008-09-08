-------------------------------------------------------------------------------
	RoadMate - README
-------------------------------------------------------------------------------

:: Introduction ::
RoadMate is a web based application, designed to support users in organising
car pooling between locations.

RoadMate is built on-top of the Google App Engine framework.

:: Directory Structure ::
The following is an outline of RoadMate's directory structure:
				
--	./images
	
		Images used by RoadMate.

--	./pages

		RoadMate's site pages and their corresponding python files.
	
--	./roadmate

		Python packages containing classes used by RoadMate.
	
--	./roadmate/models

		Data model classes for RoadMate.
	
--	./roadmate/models/data

		A collection of line delimited text files. 

		These contain static data, which is loaded into RoadMate's database
		when is it is first run on a new system.

		E.g. Lists of towns, geographical data .etc.
	
--	./stylesheets

		RoadMate's Cascading Style Sheets and their accompanying files.

--	./templates

		Template files used as starting points for most of the common files in RoadMate.

--	./openid

		JanRain's Python OpenID library.
