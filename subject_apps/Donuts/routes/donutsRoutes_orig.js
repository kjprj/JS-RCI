var express = require('express');
var router = express.Router();
var knex = require('../db/knex');

/* GET home page. */
router.get('/', function(req, res, next) {
knex.raw(`select * from donuts`).then(function(donuts){
  res.send(donuts.rows);
  });
});

router.get('/:id', function(req, res) {
//	console.log("donuts get by id", req.params.id);
knex.raw(`select * from donuts where id = ${req.params.id}`).then(function(donuts){
	//console.log(donuts);
//  var tmp0 = donuts;
  res.send(donuts);
  });
});


router.post('/', function(req,res){
knex.raw(`insert into donuts (name,topping,price) values('${req.body.name}','${req.body.topping}',${req.body.price})`).then(function(){

  knex.raw(`select * from donuts`).then(function(donuts){
    res.send(donuts.rows);
    });
  });
});


router.patch('/:id', function(req, res) {
knex.raw(`update donuts
  set
  name = '${req.body.name}',
  topping = '${req.body.topping}'
  WHERE id = ${req.params.id}
  `).then(function(){
    knex.raw(`select * from donuts`).then(function(donuts){
      res.send(donuts.rows);
    });
  });
});


router.delete('/:id',function(req,res){
  knex.raw(`delete from donuts WHERE id = ${req.params.id}`).then(function(){
    knex.raw(`select * from donuts`).then(function(donuts){
    res.send(donuts.rows);
    });
  });
});

module.exports = router;
