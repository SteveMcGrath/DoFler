var Sequelize = require('sequelize');
var config = require('config');
var sequelize = new Sequelize(config.Database.uri, {logging: config.Database.logging});


var Image = sequelize.define('image', {
	id: {type: Sequelize.INTEGER, autoIncrement: true, primaryKey: true},
	hash: Sequelize.STRING(32),
	count: {type: Sequelize.INTEGER, defaultValue: 0},
	url: Sequelize.STRING,
	filename: Sequelize.STRING(42),
	date: {type: Sequelize.DATE, defaultValue: Sequelize.NOW},
})

var Account = sequelize.define('account', {
	id: {type: Sequelize.INTEGER, autoIncrement: true, primaryKey: true},
	username: Sequelize.STRING,
	password: Sequelize.STRING,
	information: Sequelize.STRING,
	protocol: Sequelize.STRING,
	parser: Sequelize.STRING
})

var Stat = sequelize.define('stat', {
	id: {type: Sequelize.INTEGER, autoIncrement: true, primaryKey: true},
	date: {type: Sequelize.DATE, defaultValue: Sequelize.NOW},
	count: {type: Sequelize.INTEGER, defaultValue: 0},
	transport: Sequelize.STRING
})

var Host = sequelize.define('host', {
	name: {type: Sequelize.STRING, unique: true, primaryKey: true},
	date: {type: Sequelize.DATE, defaultValue: Sequelize.NOW},
	count: {type: Sequelize.INTEGER, defaultValue: 0}
})


Image.sync();
Account.sync();
Stat.sync();
Host.sync();


module.exports = {
	Account: Account,
	Image: Image,
	Stat: Stat,
	Host: Host
}