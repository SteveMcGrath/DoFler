$(document).ready(function(){ 
//attach a jQuery live event to the button
images();
accounts();

//Fetch intervals
window.setInterval(images, 5000);
window.setInterval(accounts, 5000);


var hashes = [];
function images(){
	$.getJSON('http://10.10.50.120:8089/api/images/25', function(data) {	
		$.each(data, function(key, val) {
		     if(hashes.indexOf(val.hash) == -1){
			     $("#actual-images").prepend('<img class="resize" src="http://10.10.50.120:8089/api/image/' + val.hash + '" />');
			     hashes.push(val.hash)
			 }
        });
        hashes = Array.prototype.slice.call(hashes, -6);

	});
};
var ids = [];
function accounts(){
	$.getJSON('http://10.10.50.120:8089/api/accounts/25', function(data) {	
		$.each(data, function(key, val) {
			     if(ids.indexOf(val.id) == -1){
			         $("#accounts-table tbody").prepend("<tr><td>"+ val.info +"</td><td>"+ val.proto +"</td><td>"+ val.username +"</td><td>"+ val.password +"</td></tr>");
			     ids.push(val.id)
			 }
		});
		ids = Array.prototype.slice.call(ids, -6);
	});
};

});