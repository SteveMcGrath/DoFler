var spawn = require('child_process').spawn;
var config = require('config');
var Stat = require('../models').Stat;
var parseXML = require('xml2js').parseString;
//var io = require('../web').io;

function dsniffParser() {

	function run() {
		console.log('Dsniff: Instantiating dsniff process.')

		var child = spawn('dsniff -i ' + config.Monitoring.interface, [], {shell: '/bin/bash'}
		);

		// When driftnet outputs data to standard output, we want to capture that
		// data, interpret it, and hand it off to the database.
		child.stdout.on('data', function(data) {
			console.log('DSniff: (stdout): ' + data.toString());
		})

		child.stderr.on('data', function(data) {
			console.log('DSniff: (stderr): ' + data.toString().replace(/(\r\n|\n|\r)/gm, ' '));
		})

		// If driftnet exists for some reason, log the event to the console
		// and then initiate a new instance to work from.
		child.on('close', function(code) {
			console.log('DSniff: child terminated with code ' + code);
			child = run()
		})

		child.on('error', function(error) {
			console.log('DSniff: Failed to start process');
		})
	}

	// Lets get this baby started!
	var child = run();
}

dsniffParser();

module.exports = { parser: dsniffParser}