var Sequelize = require('sequelize');
var config = require('config');
var sequelize = new Sequelize(config.Database.uri, {logging: config.Database.logging});


var Image = sequelize.define('image', {
	hash: {type: Sequelize.STRING(32), unique: true, primaryKey: true},
	count: {type: Sequelize.INTEGER, defaultValue: 0},
	date: {type: Sequelize.DATE, defaultValue: Sequelize.NOW},
	content: Sequelize.BLOB
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
	count: Sequelize.INTEGER,
	transport: Sequelize.STRING
})


Image.sync();
Account.sync();
Stat.sync();

module.exports = {
	Account: Account,
	Image: Image,
	Stat: Stat
}