var spawn = require('child_process').spawn;
var config = require('config');
var db = require('../models');
var md5File = require('md5');
var mv = require('mv');
var fs = require('fs');
var nude = require('nude');
var io = require('../web').io;

function driftnetParser() {
	// If the temporary path doesn't exist, then lets create it.
	if (!fs.existsSync(config.Monitoring.Driftnet.tmp)) {
		fs.mkdirSync(config.Monitoring.Driftnet.tmp);
	}

	// Returns a new driftnet child to work from.
	function run() {
		var child = spawn('driftnet', ['-a', '-i', config.Monitoring.interface, 
								  	   '-d', config.Monitoring.Driftnet.tmp]);
		console.log('Driftnet: Started child thread')

		// When driftnet outputs data to standard output, we want to capture that
		// data, interpret it, and hand it off to the database.
		child.stdout.on('data', function(data) {
			
			// First thing we went to do is strip out the line endings
			// from the output.
			var filenames = data.toString().split('\n');
			//var filenames = data.toString().replace(/(\r\n|\n|\r)/gm, '');

			// Next we will attempt to open the file that driftnet
			// output the location to.
			filenames.forEach(function (filename){
				//var filename = filenames[f];
				if (filename.length > 4){
					//console.log('Driftnet: found ' + filename);
					fs.readFile(filename, function(e, data) {
						if(e) {console.log('Driftnet: ' + e)} else {
							// If the file opened correctly, then we will compute
							// an md5 hash.  The ext regex is designed to get the
							// file extension from the filename.
							var hash = md5File(data);
							var ext = /(?:\.([^.]+))?$/.exec(filename)[1];
							if (ext == 'jpeg') {
								ext = 'jpg';
							}
							if (ext == 'tiff') {
								ext = 'tif';
							}
							var new_filename = hash + '.' + ext;

							// Next we will attempt to move the file to its new home.
							// If the file already exists, then the move will fail.
							mv(filename, config.AppServer.images + '/' + new_filename, 
										 {clobber: false}, function(err){
								if (err && err.code != 'EEXIST'){
									console.log('Driftnet: attempt to move ' + filename + ' failed. ' + err);
									fs.unlink(filename, function(err){});
								} else {
									if (err) {
										//console.log('Driftnet: ' + hash + ' already exists, so removing duplicate.')
										fs.unlink(filename, function(err){});
									}
									// Now lets query the database and see if an image exists
									// with the same md5sum as what we computed.  If there is
									// an existing image, then we'll increment the counter and
									// update the date timestamp.  If one doesn't exist, then
									// we will create a new image with the information we have.
									db.Image.findOrCreate({where: {hash: hash},
										defaults: {
											type: ext,
											filename: new_filename,
											url: 'DRIFTNET',
											count: 1
										}
									}).spread(function(image, created) {
										// We need to attempt to avoid double-counting if possible. as driftnet will
										// always fall behing ngrep here, we want to check to see if we already saw
										// the image within the last 10 seconds.  if we have, then dont bother to
										// to update.
										if (!(created) && ((new Date().getTime() - image.date.getTime()) >= 1000)){
											image.updateAttributes({
												count: image.count++,
												date: new Date()
											}).then(function(result){});
											io.emit('images', image);
											console.log('Driftnet: ' + image.filename + ' updated!');
										}// else {
										//	console.log('Driftnet: ngrep already got ' + image.hash);
										//}
										if (created) {
											nude.scan(config.AppServer.images + '/' + image.filename, function(res) {
												image.updateAttributes({
													nsfw: res,
													complete: true
												}).then(function(result){
													console.log('Driftnet: ' + image.filename + ' added to the database with nsfw score of ' + image.nsfw)
													if (!image.nsfw || !config.Monitoring.Driftnet.nsfw_filter) {
														io.emit('images', image);
													}
												})
											})
										}
									})
								}
							})
						}
					});
				}
			});
		})

		child.stderr.on('data', function(data) {
			console.log('Driftnet: (stderr)' + data.toString().replace(/(\r\n|\n|\r)/gm, ''));
		})

		// If driftnet exists for some reason, log the event to the console
		// and then initiate a new instance to work from.
		child.on('close', function(code) {
			console.log('Driftnet child terminated with code ' + code);
			child = run()
		})

		child.on('error', function(error) {
			console.log('Driftnet: Failed to start process');
		})
	}
	// Lets get this baby started!
	var child = run();
}

module.exports = { parser: driftnetParser }