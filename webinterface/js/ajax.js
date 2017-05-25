$(document).ready(function () {
        console.log("loli");
        $.getJSON("http://192.168.1.15/api/areas/", function(result){
		$.each( result._items, function( key, val ) {
            console.log(val);
			jQuery('<div/>', {
				id: val._id,
                class: 'dropzone js-drop',
				text: val.title
			}).appendTo('.dropzone-wrapper');

		});
		
        });
        
        $.getJSON("http://192.168.1.15/api/bulbs/", function(result){
	
		$.each( result._items, function( key, val ) {
		console.log("#"+val.area);
            console.log($('#' + val.area).offset());
            
            if($("#" + val.area).length == 0) {
                jQuery('<div/>', {
				    id: val._id,
                    class: 'draggable js-drag',
				    text: val.name
                }).appendTo('.drag-wrapper');
            } else {
                jQuery('<div/>', {
				    id: val._id,
                    class: 'draggable js-drag',
				    text: val.name,
                    textContent: val.name
                }).appendTo('.drag-wrapper');
                //}).appendTo('#' + val.area);
            };

		});
		
        });
});