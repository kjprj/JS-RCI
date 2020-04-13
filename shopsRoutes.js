var express = require('express');
var router = express.Router();
var knex = require('../db/knex');

/* GET home page. */
router.get('/', function(req, res) {
knex.raw("select * from shops order by id asc").then(function(shops){
  res.send(shops);
  });
});



router.get('/:id', function(req, res) {
  knex.raw("select * from shops where id = ${req.params.id}").then(function(shops){
    res.send(shops.rows);
  });
});


router.post('/', function(req,res){
  knex.raw("insert into shops (name,city) values(${req.body.name},${req.body.city})").then(function(){

    knex.raw("select * from shops").then(function(shops){
      res.send(shops);
    });
  });
});


router.delete('/:id',function(req,res){
  knex.raw("delete from shops WHERE id = ${req.params.id}").then(function(){
    knex.raw("select * from shops").then(function(shops){
    res.send(shops);
    });
  });
});



module.exports = router;
