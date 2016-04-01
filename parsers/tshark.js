var spawn = require('child_process').spawn;
var config = require('config');
var Stat = require('../models').Stat;
var parseXML = require('xml2js').parseString;
var io = require('../web').io;

function tsharkParser() {
	var transports = {};	// Transport array for maintaining protocol counts.

	// As the transports array is keeping state of the current packet counts
	// for the various transports we have seen, we need to be able to schedule
	// routine checkpointing of the data and commiting that information to the
	// database.  We will run the checkpoiting every 60 seconds.
	setInterval(function() {
		// The first thing we need to do is copy the transports array and then
		// clear out the existing counters.
		var items = transports;
		transports = {};
		console.log('TShark: Initiating Checkpoint.')

		// As we are checkpointing every minute, we want to make sure that the
		// data is represented on a minute-by-minute basis, and not with a
		// higher fidelity than that.  So what we are doing here is creating the
		// ts variable with a date fidelity equal to the current minute.
		var d = new Date();
		var ts = new Date(d.getYear(), d.getMonth(), d.getDay(), d.getHours(), d.getMinutes());

		// Now we need to iterate through all of the keys in the array and
		// create a new database entry for each one.
		for (var key in items){
			console.log('TShark: Checkpointing ' + key + ' at ' + items[key])
			Stat.create({
				transport: key,
				count: items[key],
				date: ts
			});
		}
		io.emit('protocols', 'refresh');
	}, 60000);	// 60 second timer.

	// 
	function run() {
		var skip = true;		// The line skipping flag. Set to true until we encounter a packet.
		var raw_packet = '';	// The raw packet string. XML assembly happens on this variable.

		console.log('TShark: Instantiating tshark process.')

		// Yes this is a nasty looking spawn command.  Unfortunately because of how
		// TShark want to write to disk, we need to route the network information
		// into tshark through dumpcap by piping all of this madness together.  There
		// is an interesting chain of bugs I have filed with the wireshark devs based
		// on trying to figure all of this out:
		// 		https://bugs.wireshark.org/bugzilla/show_bug.cgi?id=9533
		// 		
		var child = spawn('dumpcap -i ' + config.Monitoring.interface + 
						' -P -w - | tshark -T psml -PS -l -r -', [], {shell: '/bin/bash'}
		);

		// When driftnet outputs data to standard output, we want to capture that
		// data, interpret it, and hand it off to the database.
		child.stdout.on('data', function(data) {
			
			// As Tshark is generating enough output to cause Node.js to buffer
			// the output, we want to make sure that we are parsing through the
			// line-by-line and reconstructing complete packet definitions.  So
			// we will split the output buffer based on carriage returns and
			// interact with each line.
			var lines = data.toString().split('\n');
			for (var i in lines) {

				// The first several lines output from TShark include the XML
				// definition and the schema for the PSML specification.  As
				// these lines are not important to use, we will want to simply
				// ignore them.  I'm using a rudimentary skip flag that is set
				// to true until we see a <packet> flag in the stream.
				if (skip) {
					if (lines[i].indexOf('<packet>') > -1){
						skip = false;
						console.log('TShark: Starting to process packet data.')
					}
				}
				if (!(skip)) {
					raw_packet = raw_packet.concat(lines[i])

					// New we need to see if the raw_packet is complete.  If it is, then
					// we will need to parse the raw_packet and attempt to marry it to
					// the data we have on hand.
					if (lines[i].indexOf('</packet>') > -1) {
						var pkt = raw_packet;
						raw_packet = ''
						parseXML(pkt, function(err, packet) {
							// The PSML specification is as such:
							//
							//	<structure>
							//		<section>N.</section> 
							//  	<section>Time</section> 
							//  	<section>Link Layer</section> 
							//  	<section>Network</section> 
							//  	<section>Transport</section> 
							//  	<section>Application</section>
							//		<section>(OPTIONAL) Other Information</section>
							//	</structure>
							// 
							// What we are looking for is the transport protocol, which
							// is the 5th section in the PSML spec.  We will take that
							// peice of information and then keep track fo the number of
							// packets we see with that transport.
							var transport = packet.packet.section[4];
							if (!(transport in transports)) {
								transports[transport] = 0;
							}
							transports[transport] += 1;
							//console.log('TShark: ' + transport + '++')
						});
					}				
				}
			}
		})

		child.stderr.on('data', function(data) {
			// What we are looking to do here is strip out the packet counters from entering
			// the console log.  We still want all other standard error entries to hit the
			// console log however, so a simple regex check to filter out the spammy data
			// should be all we need.
			var repkt = /Packets: (\d+)/g;
			if (!(repkt.exec(data.toString()))){
				console.log('TShark: (stderr): ' + data.toString().replace(/(\r\n|\n|\r)/gm, ' '));
			}
		})

		// If driftnet exists for some reason, log the event to the console
		// and then initiate a new instance to work from.
		child.on('close', function(code) {
			console.log('TShark: child terminated with code ' + code);
			child = run()
		})

		child.on('error', function(error) {
			console.log('TShark: Failed to start process');
		})
	}

	// Lets get this baby started!
	var child = run();
}

module.exports = { parser: tsharkParser}