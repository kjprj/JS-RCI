var express = require('express');
var router = express.Router();
var knex = require('../db/knex');

/* GET home page. */


router.get('/', function(req, res, next) {
  knex.raw(`SELECT * from employees`).then(function(employees) {
    res.render('employees', {
      employees: employees.rows
    })
  });
});

router.post('/edit/:id', function(req, res) {
  knex.raw(`update employees set first_name = '${req.body.first_name}', last_name = '${req.body.last_name}', favorite_donut = ${req.body.favorite_donut} where id=${req.params.id}`).then(function() {
    knex.raw(`select * from employees`).then(function(employees) {
      res.render('employees', {
        employees: employees.rows
      })
    })
  })
})

module.exports = router;
