var accounts = [];
var account_id = null;
var socket = io();


function addImage(image) {
	// Check to see if the image that was just sent to us is already being
	// displayed.  If it isn't, then we will add it to the view.
	if ($('img[src="/images/file/' + image.filename + '"]').length < 1){
		$('#images').prepend('<img class="dofler-img" src="/images/file/' + image.filename + '">');
	}

	// As we only want to display the latest 200 images, we will want to
	// remove the oldest images once this limit has been reached.
	if ($('.dofler-img').length > 200){
		$('.dofler-img:last').remove()
	}
}


function addAccount(account) {
	accounts.push(account);
}


function protoRefresh() {
	// Get the top 5 protocols from the API and then generate the flot graph
	// based on the data returned.
	$.getJSON('/stats/proto/5', function(protos) {
		$.plot('#proto-analysis', protos, 
			{xaxis: { mode: "time", position: "right", timezone: "browser"},
			legend: {position: "nw", backgroundColor: null, backgroundOpacity: 0}
		);
	})
}


function accountCycle() {
	if (accounts.length > 5) {
		// If this is the first time the accounts have gone above 5, then we will
		// need to set the initial value.
		if (account_id == null) {account_id = 5;}

		// Increment the account_id counter.
		account_id += 1;

		// If the account_id counter exceeds the number of elements in the
		// accounts array, then we will need to rotate the id to the 
		// beginning of the array.
		if (account_id > accounts.length) {
			account_id = (account_id - 1) - accounts.length;
		}

		// If the account_id is 0, then we will want to denote that by adding
		// a horizontal line.
		if (account_id == 0) {
			$('.account-entry:first').remove();
			$('#accounts').append('<tr class="account-entry"><td colspan="5"><hr /></td></tr>');
		}

		// Now to remove the first entry and add the last entry into the
		// user view.
		$('.account-entry:first').remove();
		$('#accounts').append('<tr class="account-entry"><td>' 
							  + account_id + '</td><td>' + 
							  accounts[account_id].username + '</td><td>' +
							  accounts[account_id].password + '</td><td>' +
							  accounts[account_id].protocol + '</td><td>' +
							  accounts[account_id].dns + '</td></tr>'
		);
	}
}


socket.on('images', function(image) {
	addImage(image);
})


socket.on('accounts', function(account) {
	accounts.push(account);
})


socket.on('protocols', function(data){
	protoRefresh();
})


$(document).ready(function () {
	$.getJSON('/images/list', function(images) {
		$.each(images, function(key, image) {
			addImage(image);
		})
	})
})
