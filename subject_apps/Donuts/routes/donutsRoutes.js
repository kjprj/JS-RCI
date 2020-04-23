//JS-RCI
var express = require('express');
var router = express.Router();
var knex = require('../db/knex');

/* GET home page. */

var tmpv2 = '/';
router.get(tmpv2, function(req, res) {
var tmpv0 = "select * from donuts";
knex.raw(tmpv0).then(function(donuts){
  var tmpv1 = donuts;
res.send(tmpv1);
  });
});

var tmpv5 = '/:id';
router.get(tmpv5, function(req, res) {
var tmpv00 = req.params;
var tmpv01 = tmpv00.id;
var tmpv3 = "select * from donuts where id ="+tmpv01;
knex.raw(tmpv3).then(function(donuts){
  var tmpv4 = donuts;
res.send(tmpv4);
  });
});




var tmpv9 = '/';
router.post(tmpv9, function(req,res){
    var tmpv33 = req.body;
    var tmpv6 = "insert into donuts (name,topping,price) values( '"+tmpv33.name+"' , '"+tmpv33.topping+"' , '"+tmpv33.price+" ')";
    knex.raw(tmpv6).then(function(){
    var tmpv7 = "select * from donuts";
    knex.raw(tmpv7).then(function(donuts){
        var tmpv8 = donuts;
        res.send(tmpv8);
    });
  });
});



var tmpv13 = '/:id';
router.patch(tmpv13, function(req, res) {
    var tmpv44 = req.body;
    console.log("tmpv44 ", tmpv44);
    var tmpv10 = "update donuts set name = '"+tmpv44.name+"', topping = '"+tmpv44.topping+"' WHERE id = "+tmpv44.id;
    knex.raw(tmpv10).then(function(){
        var tmpv11 = "select * from donuts";
        knex.raw(tmpv11).then(function(donuts){
            var tmpv12 = donuts;
            res.send(tmpv12);
    });
  });
});


var tmpv17 = '/:id';
router.delete(tmpv17,function(req,res){
    console.log("deleting??",req)
    var tmpv22 = req.params;
    var tmpv21 = tmpv22.id;
    var tmpv14 = "delete from donuts WHERE id ="+tmpv21;
    knex.raw(tmpv14).then(function(){
        var tmpv15 = "select * from donuts";
        knex.raw(tmpv15).then(function(donuts){
            var tmpv16 = donuts;
            res.send(tmpv16);
        });
      });
});

/****/
module.exports = router;

