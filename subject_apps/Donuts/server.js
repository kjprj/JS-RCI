var path = require('path');
var express = require('express');
var bodyParser = require('body-parser');
var port = process.env.PORT || 8999;
var cors = require('cors');
var logger = require('morgan');
var knex = require('./db/knex');

var shops = require('./routes/shopsRoutes');
var donuts = require('./routes/donutsRoutes');
var employee = require('./routes/employeeRoutes');

var app = express();

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.use('/shops', shops);
app.use('/donuts',donuts);
app.use('/employee',employee);

app.get('/', function(req, res){ res.redirect('/shops')});

app.use(express.static(__dirname + '/public'));

app.listen(port, function() {
console.log("listening on port: ", port);
});
