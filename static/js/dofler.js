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
	if ($('.dofler-img').length > 100){
		$('.dofler-img:last').remove()
	}
}


function hostVulnList(data) {
	// Empty the table in preperation for the the new information
	$('#top-vulnerable-hosts > tbody').empty();

	// A simple function to get the percentage of the maximum number
	// of severities that the current severity specified is.
	function getPercent(value) {
		return ((value / data['max'] * 100) - 0.1).toFixed(1);
	}

	// Lets actually draw the information on to the screen.
	$.each(data['hosts'], function(i, val) {
		$('#top-vulnerable-hosts > tbody').append( 
			'<tr><td class="host-cell">' + val.host + '</td><td><div class="vuln-candy-bar">' +
			'<div class="v-crit" style="width:' + getPercent(val.crit) + '%;"></div>' +
			'<div class="v-high" style="width:' + getPercent(val.high) + '%;"></div>' +
			'<div class="v-med" style="width:' + getPercent(val.med) + '%;"></div>' +
			'<div class="v-low" style="width:' + getPercent(val.low) + '%;"></div>' +
			'</div></td></tr>'
		);
	});
}


function topVulnsList(data) {
	// Empty the list in preperation for the the new information
	$('#top-vulnerabilities').empty();

	var crits = ['info', 'low', 'med', 'high', 'crit'];

	$.each(data, function(i, val) {
		$('#top-vulnerabilities').append(
			'<li class="list-group-item vulnerability">' + val.name + '<span class="vuln-badge badge">' + val.count + '</span></li>'
		);
	});
}


function addAccount(account) {
	accounts.push(account);
}


function protoRefresh() {
	// Get the top 5 protocols from the API and then generate the flot graph
	// based on the data returned.
	$.getJSON('/stats/protocols/5', function(protos) {
		$.plot('#proto-analysis', protos, 
			{xaxis: { mode: "time", position: "right", timezone: "browser"},
			legend: {position: "nw", backgroundColor: null, backgroundOpacity: 0}
		});
	})
}


function displayAccount(account) {
	$('#account-total').html(accounts.length);
	$('#accounts-list > tbody').append(
		'<tr class="account-entry"><td>' +
		S(account.username).escapeHTML() + '</td><td>' +
		S(account.password).escapeHTML() + '</td><td>' +
		S(account.protocol).escapeHTML() + '</td><td>' +
		S(account.dns).escapeHTML() + '</td></tr>'
	);
}


function renderAccountList() {
	if (accounts.length > 5) {
		for (var i in accounts.slice(0,5)) {displayAccount(accounts[i])}
	} else {
		for (var i in accounts) {displayAccount(accounts[i])}
	}
}


function accountCycle() {
	if (accounts.length > 5) {
		// If this is the first time the accounts have gone above 5, then we will
		// need to set the initial value.
		if (account_id == null) {account_id = 5;}

		// Increment the account_id counter.
		account_id++;

		// If the account_id counter exceeds the number of elements in the
		// accounts array, then we will need to rotate the id to the 
		// beginning of the array.
		if (account_id > accounts.length - 1) {
			account_id = account_id - accounts.length;
		}
		console.log(account_id)

		// Now to remove the first entry and add the last entry into the
		// user view.
		$('.account-entry:first').remove();
		displayAccount(accounts[account_id]);
		console.log(accounts[account_id]);
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
	});
	$.getJSON('/accounts/list', function(account_list) {
		accounts = account_list;
		renderAccountList();
	});
	$.getJSON('/vulns/hosts', function(data) {hostVulnList(data)});
	$.getJSON('/vulns/vulns', function(data) {topVulnsList(data)});
	protoRefresh();
	setInterval(accountCycle, 1000);
})
