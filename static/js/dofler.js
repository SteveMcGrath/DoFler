var accounts = [];
var account_id = null;
var socket = io();
var flagged_images = [];


function addImage(image) {
	// Check to see if the image that was just sent to us is already being
	// displayed.  If it isn't, then we will add it to the view.
	var nsfw_ceiling = parseInt($('#nsfw-ceiling').val())
	if ($('img[src="/images/file/' + image.filename + '"]').length < 1
		&& ((nsfw_ceiling && image.nsfw <  nsfw_ceiling) || !nsfw_ceiling)
		&& flagged_images.indexOf(image.filename) > -1
	){
		if ($('#debug').is(':checked')){
			console.log(image.filename + ' + with nsfw score ' + image.nsfw + ' drawn')
		}
		$('#images').prepend('<img class="dofler-img" src="/images/file/' + image.filename + '" onclick="removeImage(' + image.filename + ')">');
	}else{
		if ($('#debug').is(':checked')){
			console.log(image.filename + ' + with nsfw score ' + image.nsfw + ' NOT drawn')
		}
	}

	// As we only want to display the latest 200 images, we will want to
	// remove the oldest images once this limit has been reached.
	if ($('.dofler-img').length > 100){
		$('.dofler-img:last').remove()
	}
}


function removeImage(filename) {
	if ($('#removable-images').is(':checked')) {
		$('img[src="/images/file/' + filename + '"]').remove()
		flagged_images.push(filename)
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


function protoRefresh(reporting = false) {
	// Get the top 5 protocols from the API and then generate the flot graph
	// based on the data returned.
	var url = '/stats/protocols/5'
	if (reporting) {url = '/stats/protoreport/10'}
	$.getJSON(url, function(protos) {
		$.plot('#proto-analysis', protos, 
			{xaxis: { mode: "time", position: "right", timezone: "browser"},
			legend: {position: "nw", backgroundColor: null, backgroundOpacity: 0}
		});
	})
}


function protoList() {
	$.getJSON('/stats/protolist', function(protos) {
		$.each(protos, function(key, proto) {
			$('#proto-list').append('<li class="list-group-item"><span class="badge">' + proto.count + '</span>' + proto.name + '</li>')
		})
	})
}


function displayAccount(account, clip=true) {
	$('#account-total').html(accounts.length);

	$('#accounts-list > tbody').append(
		'<tr class="account-entry"><td>' +
		S(account.username || '').escapeHTML().substring(0,15) 	+ '</td><td>' +
		S(account.password || '').escapeHTML().substring(0,15) 	+ '</td><td>' +
		S(account.protocol || '').escapeHTML() 					+ '</td><td>' +
		S(account.dns || '').escapeHTML().substring(0,15) 		+ '</td></tr>'
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


function report() {
	$(document).ready(function () {
		$.getJSON('/images/common', function(images) {
			$.each(images, function(key, image) {
				$('#image-table').append('<tr><td>' + image.count + '</td><td><img class="dofler-img" src="/images/file/' + image.filename + '"></td></tr>');
			})
		});
		$.getJSON('/accounts/list', function(accounts) {
			$.each(accounts, function(key, account) {
				addAccount(account);
				displayAccount(account);
			})
		});
		protoRefresh(true);
	})
}


function display() {
	socket.on('images', function(image) {
		addImage(image);
	})


	socket.on('accounts', function(account) {
		accounts.push(account);
	})


	socket.on('protocols', function(data){
		protoRefresh();
	})


	socket.on('vulnHosts', function(data){
		$.getJSON('/vulns/hosts', function(data) {hostVulnList(data)});
	})


	socket.on('topVulns', function(data){
		$.getJSON('/vulns/vulns', function(data) {topVulnsList(data)});
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
}