var express = require('express');
var router = express.Router();
var knex = require('../db/knex');

/* GET home page. */
router.get('/', function(req, res, next) {
knex.raw("select * from employee").then(function(employee){
  res.send(employee.rows);
  });
});


router.get('/employee', function(req, res) {
knex.raw("select * from employee order by id asc").then(function(employee){
  res.render("employeeViews/allEmployees", {
    employee:employee.rows});
  });
});

router.get('/employee/:id', function(req, res) {
knex.raw("select * from employee where id = ${req.params.id}").then(function(employee){
  res.render('employeeViews/allEmployees',{
    employee:employee.rows});
  });
});


router.post('/', function(req,res){
  knex.raw("insert into employee (first_name,last_name,favorite_donut,shop_id) values(${req.body.first_name},${req.body.last_name},${req.body.favorite_donut},${req.body.shop_id})").then(function(){

    knex.raw("select * from employee").then(function(employee){
      res.send(employee.rows);
    });
  });
});


router.patch('/:id', function(req, res) {
knex.raw("update employee set first_name = ${req.body.first_name}, last_name = ${req.body.last_name}, favorite_donut = ${req.body.favorite_donut}, shop_id = ${req.body.shop_id} WHERE id = ${req.params.id}"
  ).then(function(){
    knex.raw("select * from employee").then(function(employee){
      res.send(employee.rows);
    });
  });
});

router.delete('/:id',function(req,res){
  knex.raw("delete from employee WHERE id = ${req.params.id}").then(function(){
    knex.raw("select * from employee").then(function(employee){
    res.send(employee.rows);
    });
  });
});

module.exports = router;
