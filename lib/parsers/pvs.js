var config = require('config');
var httpreq = require('httpreq');
var web = require('../web');

function pvsParser() {
	// As the PVS os most likely using a self-signed certificate, we will
	// need to make sure we turn off Node's default behavior to check
	// the certificate validity.
	process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

	// All of the functions will be leveraging the host variable, which
	// is derrived from the configuration settings.
	var host = 'https://' + config.Monitoring.PVS.hostname + ':8835';

	function pvsData() {
		var token = null;
		// Initiate the login to the PVS API.
		httpreq.post(host + '/login', {
			parameters: {
				login: config.Monitoring.PVS.username,
				password: config.Monitoring.PVS.password,
				json: 1
			}
		}, function(err, res) {
			if (err) {
				console.log('PVS: ' + err);
			} else {
				// As it appears that we were able to login, lets to ahead
				// and set the token variable.
				var data = JSON.parse(res.body);
				token = data['reply']['contents']['token'];

				// Here what we'll be interfacing to is the top hosts
				// dashboard item.  Since the New PVS WebUI has formatted
				// most of the data all pretty for us already, we just
				// need to reformat it for our uses.
				httpreq.post(host + '/chart/data', {
					parameters: {
						chart_id: 1, 	// Chart 1 is the top hosts chart.
						start_time: -1,
						end_time: -1,
						json: 1,
						token: token
					}
				}, function(err, res) {
					if (err) {
						console.log('PVS: ' + err);
					} else {
						// Lets parse the JSON returned and put the data into
						// the hostCache variable and emit the information to
						// the WebUI.
						var data = JSON.parse(res.body);
						var raw = data['reply']['contents']['chart_data'];

						// The cooked variable will be storing our new dictionary
						// array.  The max variable is storing the maximum number
						// of vulnerabilities we have seen on a given host.  This
						// saves us having to compute this on the front-end.
						var cooked = [];
						var max = 0;
						var count = 0;
						for (var h in raw) {
							count++;
							if (count <= 5) {
								// First we pull the severity summaries and remove the
								// informationals.
								var sevs = raw[h]['data'];
								sevs.pop();

								// Next we will compute the total and compare that against
								// the max counter.  If our current counter is greater than
								// the max we have be storing, then we will replace the max
								// with the current counter.
								var sevcount = sevs.reduce(function(a, b) {return a + b}, 0);
								if (sevcount > max) {max = sevcount}

								// Add the newly cooked info into the array.
								cooked.push({
									host: h,
									crit: sevs[0],
									high: sevs[1],
									med: sevs[2],
									low: sevs[3]

								});
							}
						}
						var fullyCooked = {max: max, hosts: cooked};
						web.hostCache(fullyCooked);
						console.log('PVS: Updated Top Vulnerable Hosts Cache');
						web.io.emit('vulnHosts', fullyCooked);

						// Here what we'll be interfacing to is the top vulns
						// dashboard item.  Since the New PVS WebUI has formatted
						// most of the data all pretty for us already, we just
						// need to reformat it for our uses.
						httpreq.post(host + '/chart/data', {
							parameters: {
								chart_id: 2, 	// Chart 2 is the top vulns chart.
								start_time: -1,
								end_time: -1,
								json: 1,
								token: token
							}
						}, function(err, res) {
							if (err) {
								console.log('PVS: ' + err);
							} else {
								// Lets parse the JSON returned and put the data into
								// the hostCache variable and emit the information to
								// the WebUI.
								var data = JSON.parse(res.body);
								var raw = data['reply']['contents']['chart_data']
								var cooked = [];
								var count = 0;
								for (var vuln in raw) {
									count++
									if (count <= 5) {
										cooked.push({
											name: vuln,
											pluginId: raw[vuln]['id'],
											count: raw[vuln]['data'][0],
											severity: raw[vuln]['severity']
										});
									}
								}
								web.vulnCache(cooked);
								console.log('PVS: Updated Top Vulnerabilities Cache');
								web.io.emit('topVulns', cooked);

								// Initiate a logout from the API.  We need to make sure to do
								// this so that we don't keep sessions running to time out
								httpreq.post(host + '/logout', {parameters: {json: 1, token: token}})
							}
						})
					}
				})
			}
		});
		return token;
	}

	// Now as the PVS parser is purely API work, we will simply be running
	// over the appropriate API commands every 60 seconds.
	pvsData();
	setInterval(pvsData, 60000);
}

module.exports = { 
	parser: pvsParser
}