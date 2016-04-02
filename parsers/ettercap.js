var spawn = require('child_process').spawn;
var config = require('config');
var Account = require('../models').Account;
var url = require('url');
var io = require('../web').io;

function ettercapParser() {

	function run() {
		console.log('Ettercap: Instantiating dsniff process.')

		var child = spawn('ettercap -Tzuqi ' + config.Monitoring.interface, [], {shell: '/bin/bash'});

		// Ettercap data capture...
		child.stdout.on('data', function(data) {
			// When we get new standard output, we want to check it against a couple of
			// regex patterns.
			var rdata = /USER: (.+?)  PASS: (.+?)  INFO: (.*)/gm
			var rproto = /^(.+?) :/gm
			var raw = rdata.exec(data.toString());
			var proto = rproto.exec(data.toString());

			// If both regex patterns yeidl useful data, then we will attempt to parse
			// the data into what we are looking for.
			if (raw && proto) {
				var username = raw[1];
				var password = raw[2].slice(0,3) + Array(raw[2].length - 2).join('*');
				var information = raw[3];
				var protocol = proto[1];
				var dns = url.parse(raw[3]).hostname;

				// Next we will search the database to see if we have seen this specific
				// account information before.  If we havent, then we will create a
				// new database object with the information we discovered and then inform
				// the WebUI of the new data.
				Account.findOne({
					where: {
						username: username,
						password: password,
						information: information,
						protocol: protocol
					}
				}).then(function(err, result) {
					if (!(result)) {
						Account.create({
							username: username,
							password: password,
							information: information,
							parser: 'ettercap',
							protocol: protocol,
							dns: dns
						});
						console.log('Ettercap: Added ' + username + ':' + password + ' account');
						io.emit('accounts', {
							username: username,
							password: password,
							information: information,
							parser: 'ettercap',
							protocol: protocol,
							dns: dns
						});
					}
				});
			}
		})

		child.stderr.on('data', function(data) {
			console.log('Ettercap: (stderr): ' + data.toString().replace(/(\r\n|\n|\r)/gm, ' '));
		})

		// If driftnet exists for some reason, log the event to the console
		// and then initiate a new instance to work from.
		child.on('close', function(code) {
			console.log('Ettercap: child terminated with code ' + code);
			child = run()
		})

		child.on('error', function(error) {
			console.log('Ettercap: Failed to start process');
		})
	}

	// Lets get this baby started!
	var child = run();
}


module.exports = { parser: ettercapParser}