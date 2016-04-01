var spawn = require('child_process').spawn;
var config = require('config');
var db = require('../models');
var md5File = require('md5');
var mv = require('mv');
var fs = require('fs');

function driftnetParser() {
	// If the temporary path doesn't exist, then lets create it.
	if (!fs.existsSync(config.Monitoring.Driftnet.tmp)) {
		fs.mkdirSync(config.Monitoring.Driftnet.tmp);
	}

	// Returns a new driftnet child to work from.
	function run() {
		return spawn('driftnet', ['-a', '-i', config.Monitoring.interface, 
								  '-d', config.Monitoring.Driftnet.tmp]);

		// When driftnet outputs data to standard output, we want to capture that
		// data, interpret it, and hand it off to the database.
		child.stdout.on('data', function(data) {
			
			// First thing we went to do is strip out the line endings
			// from the output.
			var filename = data.toString().replace(/(\r\n|\n|\r)/gm, '');
			console.log('Driftnet: found ' + filename)

			// Next we will attempt to open the file that driftnet
			// output the location to.
			fs.readFile(filename, function(e, data) {
				if(e) {console.log('Driftnet: ' + e)} else {
					// If the file opened correctly, then we will compute
					// an md5 hash.  The ext regex is designed to get the
					// file extension from the filename.
					var hash = md5(data)
					var ext = /(?:\.([^.]+))?$/.exec(filename)[1];
					var new_filename = hash + '.' + ext;

					// Next we will attempt to move the file to its new home.
					// If the file already exists, then the move will fail.
					mv(filename, config.AppServer.images + '/' + new_filename, 
								 {clobber: false}, function(err){
						if (err){
							console.log('Driftnet: attempt to move ' + filename + ' failed.')
							fs.unlink(filename, function(err){});
						} else {
							// Now lets query the database and see if an image exists
							// with the same md5sum as what we computed.  If there is
							// an existing image, then we'll increment the counter and
							// update the date timestamp.  If one doesn't exist, then
							// we will create a new image with the information we have.
							db.Image.findOrCreate({where: {hash: hash},
								defaults: {
									type: ext.exec(filename)[1],
									filename: new_filename,
									url: 'DRIFTNET',
									count: 1
								}
							}).spread(function(image, created) {
								image.updateAttributes({
									count: image.count++,
									date: db.Sequelize.NOW
								}).then(function(result){});
								if (created) {
									console.log('Driftnet: ' + image.filename + ' added to the database!')
								} else {
									console.log('Driftnet: ' + image.filename + ' updated!')
								}
							})
						}
					})
				}
			})
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