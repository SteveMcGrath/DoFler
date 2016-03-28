var spawn = require('child_process').spawn;
var config = require('config');
var httpreq = require('httpreq');
var db = require('../models');
var md5 = require('md5');
var fs = require('fs');

function ngrepParser() {
	function run() {
		// These are the image extensions we will be looking for
		var imageExtensions = [
			'gif', 'jpg', 'jpeg', 'png', 'svg', 'bmp', 'tif', 'tiff', 'pdf'
		];
		
		console.log('NGrep: Instantiating ngrep process.')

		// This is the command to monitor port 80 and get the header information
		// for every HTTP call thats being made.	
		var child = spawn('ngrep -d ' + config.Monitoring.interface + 
						' -W byline -qilw \'get\' tcp dst port 80', [], {shell: '/bin/bash'}
		);

		// When ngrep outputs data to standard output, we want to capture that
		// data, interpret it, and hand it off to the database.
		child.stdout.on('data', function(data) {
			var entry = data.toString();

			// The two peices of information that we want to pull out of the header
			// data are as follows:  The DNS address and the URL path.
			var host = /Host\: (.*)\./gm.exec(entry);
			var path = /GET (.*) HTTP/gm.exec(entry);

			// The only reason to continue further is if we were able to properly
			// extract both a valid host and a path.
			if (path && host) {
				// Lets next try to reconstruct the URL and the file extension
				// from the information we have on hand.
				var url = ('http://' + host[1] + path[1]);
				var url_nq = ('http://' + host[1] + path[1].split('?').shift());
				var ext = /(?:\.([^.]+))?$/.exec(path[1].split('?').shift())[1];

				// If we were able to extract the file extension from the path,
				// then we will want to do some basic normalization to the extension
				if (ext) {
					ext = ext.toLowerCase();
					if (imageExtensions.indexOf(ext) > -1) {
						// If the extension is a valid image extension, then we will
						// want to query the database to see if we have seen that
						// URL path used before.  If we have, then we will just
						// increment the date timestamp and the counter.
						db.Image.findOne({where: {url: url_nq}}).then(function(image){
							if (image) {
								image.count += 1;
								// As an attempt to make sure that the front-end isn't
								// getting spammed with the same image over and over,
								// we will only update the date timestamp (which in
								// turn will allow it to be refreshed on the webui)
								// if we haven't seen the image for 60 seconds.
								if ((new Date().getTime() - image.date.getTime()) >= 60000) {
									image.date = new Date();
								}
								if (!image.url){
									image.url = url_nq;
								}
								image.save();
							} else {
								// As we havent seen the image in the database, we will
								// then download the file, compute the MD5 hash, then
								// store the file with the MD5 hash as the filename.
								httpreq.get(url, {binary: true}, function(err, res){
									if (err) {
										console.log('NGrep: download error - ' + err);
									} else {
										var hash = md5(res.body);
										var filename = hash + '.' + ext;
										// Attempt to write the file...
										fs.writeFile(config.AppServer.images + '/' + filename, res.body, function(err) {
											if (err) {
												console.log('NGrep: file save error - ' + err);
											} else {
												// Creating a new image object and inserting it into the database...
												db.Image.create({
													hash: hash,
													filename: filename,
													url: url_nq,
													count: 1
												}).then(function(image){
													if (image) {
														console.log('NGrep: ' + image.filename + ' created from ' + image.url);
													}
												})
											}
										})
									}
								})
							}
						})
					}
				}
			}
		})

		child.stderr.on('data', function(data) {
			console.log('NGrep: (stderr): ' + data.toString().replace(/(\r\n|\n|\r)/gm, ' '));
		})

		// If ngrep exits for some reason, log the event to the console
		// and then initiate a new instance to work from.
		child.on('close', function(code) {
			console.log('NGrep: child terminated with code ' + code);
			child = run()
		})

		child.on('error', function(error) {
			console.log('NGrep: Failed to start process');
		})
	}

	// Lets get this baby started!
	var child = run();
}

// Now to check to see if we actually want to start the parser and fire it up if we do.
if (config.Monitoring.NGrep.autostart){
	ngrepParser();
}