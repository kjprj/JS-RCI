//var environment = process.env.NODE_ENV || 'development';
var environment = 'development';
var config = require('../knexfile.js')[environment];
module.exports = require('knex')(config);
