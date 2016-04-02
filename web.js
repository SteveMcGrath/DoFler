var config = require('config');
var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var db = require('./models');
var async = require('async');
var vulnCache = null;
var hostCache = null;


app.set('view engine', 'jade');
app.use('/static', express.static(config.AppServer.static));
app.use('/images/file', express.static(config.AppServer.images));


// A simple function to subtract 
Date.prototype.rmHours = function(h) {    
   this.setTime(this.getTime() - (h*60*60*1000)); 
   return this;   
}


app.get('/', function(req, res) {
	res.render('index', {
		version: '5.0a1',
		title: config.WebUI.title,
		slogan: config.WebUI.slogan
	});
})


app.get('/images/list', function(req, res) {
	db.Image.findAll({
		order: 'date DESC',
		limit: 200,
		raw: true
	}).then(function(images) {
		res.json(images.reverse());
	})
})


app.get('/accounts/list', function(req, res){
	db.Account.findAll().then(function(accounts) {
		res.json(accounts);
	})
})


app.get('/vulns/hosts', function(req, res) {res.json(hostCache);});
app.get('/vulns/vulns', function(req, res) {res.json(vulnCache);});


app.get('/stats/protocols/:limit', function(req, res) {
	db.Stat.findAll({
	  attributes: ['transport'],
	  order: [[db.sequelize.fn('COUNT', db.sequelize.col('count')), 'DESC']],
	  limit: parseInt(req.params.limit),
	  group: ['transport']
	}).then(function(protos){
	  var dLimit = new Date();
	  dLimit = dLimit.rmHours(8);

	  var protocols = []
	  async.each(protos, function (proto, next) {
	    db.Stat.findAll({
	      where: {
	        date: {gte: dLimit},
	        transport: proto.transport,
	      }
	    }).then(function(results) {
	      var d = [];
	      for (var a in results) {
	        d.push([results[a].date.getTime(), results[a].count]);
	      }

	      protocols.push({
	        label: proto.transport,
	        data: d
	      })

	      next()
	    })
	  }, function (error) {
	    res.json(protocols);
	  })
	})
})


http.listen(config.AppServer.port, function(){
	console.log('Application Web Server is listening on *:' + config.AppServer.port);
})


module.exports = {
	io: io,
	vulnCache: function(data) {vulnCache = data;},
	hostCache: function(data) {hostCache = data;}
}