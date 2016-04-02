var config = require('config');
var driftnet = require('./driftnet').parser;
var tshark = require('./tshark').parser;
var ngrep = require('./ngrep').parser;
var pvs = require('./pvs').parser;
var ettercap = require('./ettercap').parser;

// For each parser, if autostart is set to true in the config
// file, then we will want to fire that parser up.
if (config.Monitoring.Driftnet.autostart) 	{ driftnet(); }
if (config.Monitoring.NGrep.autostart) 		{ ngrep(); }
if (config.Monitoring.TShark.autostart) 	{ tshark(); }
if (config.Monitoring.PVS.autostart)		{ pvs(); }
if (config.Monitoring.Ettercap.autostart)	{ ettercap(); }
