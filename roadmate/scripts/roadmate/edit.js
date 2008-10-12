// editControl(fieldname, userid)
// use this function to standardize the creation of all the inplaceeditor controls
// just a wrapper on the creation of InPlaceEditor
//
// Params:
//        fieldname       name (id) of the field to bind the control to
//        handler         page to handle the request (can return a new value)
//
// Returns: an instance of Ajax.InPlaceEditor
//
function editTextControl(fieldname, handler) {
	new Ajax.InPlaceEditor(
		$(fieldname),
		handler,
		{
			highlightcolor: "#88ac0b",
			highlightendcolor: "#E8E8E8",
			okControl: 'link',
			okText: 'save',
			cancelControl: 'false'
		}
		);
	};