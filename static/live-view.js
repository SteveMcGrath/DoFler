$(document).ready(function(){ 
//attach a jQuery live event to the button
images();
accounts();

// Some basic settings that we need to set in order for
// everything to function properly.
var urlhost = '';
var image_delay = 5;		// This is set in seconds.
var id_delay = 5;			// Also set in seconds.

var max_images = 500;		// We need to set some sort
							// of a sane number so that
							// we dont kill the browser.

var max_ids = 20;			// Used to keep the account
							// display looking clean more
							// than anything.


// Here we are setting the window fetch intervals.  This is
// how we control the refresh rate of the content on the screen.
window.setInterval(images, (image_delay * 1000));
window.setInterval(accounts, (id_delay * 1000));


var hashes = [];
function images(){
	ts = Math.round((new Date()).getTime() / 1000) - image_delay;
	imgcount = $('.resize').length;
	$.getJSON(urlhost + '/api/images/' + ts, function(data) {
		$.each(data, function(key, val) {
			$("#content").prepend('<img id="dofler-image" class="resize" src="' + urlhost + '/api/image/' + val.hash + '" />');
			imgcount++;
			if(imgcount > max_images){
				$('.resize:first').remove();
				imgcount--;
			}
        });

	});
};

function accounts(){
	current = parseInt($('.account-id:first').attr('aid'))
	if(isNaN(current)){
		current = 0;
	}
	idcount = $('.account-id').length;
	$.getJSON(urlhost + '/api/accounts/' + (current + 1), function(data) {
		$.each(data, function(key, val) {
		    $("#accounts-table tbody").prepend('<tr class="account-id" aid="' + val.id + '"><td>'+ val.info.substr(0,28) +'</td><td>'+ val.proto +'</td><td>'+ val.username +'</td><td>'+ val.password.substr(0,15) +'</td></tr>');
		    idcount++;
		    if(idcount > max_ids){
		    	$('.account-id:last').remove();
		    	idcount--;
		    }
		});
	});
};

});