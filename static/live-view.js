$(document).ready(function(){ 
//attach a jQuery live event to the button
images();
accounts();

//Fetch intervals
window.setInterval(images, 5000);
window.setInterval(accounts, 5000);

var urlhost = ''
var numimages = 25
var numaccounts = 25

var hashes = [];
function images(){
	$.getJSON(urlhost + '/api/images/' + numimages, function(data) {	
		$.each(data, function(key, val) {
		     if(hashes.indexOf(val.hash) == -1){
			     $("#actual-images").prepend('<img class="resize" src="' + urlhost + '/api/image/' + val.hash + '" />');
			     hashes.push(val.hash)
			 }
        });
        hashes = Array.prototype.slice.call(hashes, -numimages);

	});
};
var ids = [];
function accounts(){
	$.getJSON(urlhost + '/api/accounts/' + numaccounts, function(data) {	
		$.each(data, function(key, val) {
			     if(ids.indexOf(val.id) == -1){
			         $("#accounts-table tbody").prepend("<tr><td>"+ val.info +"</td><td>"+ val.proto +"</td><td>"+ val.username +"</td><td>"+ val.password +"</td></tr>");
			     ids.push(val.id)
			 }
		});
		ids = Array.prototype.slice.call(ids, -numaccounts);
	});
};

});