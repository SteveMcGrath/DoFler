var config = require('config');
var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var db = require('./models');


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
		res.send(images.reverse());
	})
})


app.get('/stats/protocols/:limit', function(req, res) {
	db.Stat.findAll({
		attributes: ['transport'],
		order: [[db.sequelize.fn('COUNT', db.sequelize.col('count')), 'DESC']],
		limit: parseInt(req.params.limit),
		group: ['transport']
	}).then(function(protos){
		var dLimit = new Date();
		dLimit = dLimit.rmHours(8);
		for (var i in protos) {
			db.Stat.findAll({
				where: {
					date: {gte: dLimit},
					transport: protos[i].transport,
				}
			}).then(function(results) {
				var d = [];
				for (var a in results) {
					d.push([results[a].date, results[a].count]);
				}
				res.write(JSON.stringify({
					label: protos[i].transport,
					data: d
				}));
			}).done();
		}
	}).done(function(){
		res.end();
	});
})


module.exports = {
	io: io
}


http.listen(3000, function(){
	console.log('listening on *:3000');
})