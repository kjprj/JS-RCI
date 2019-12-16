function abc(){
var tmpv0 = "select * from donuts";
var donuts = alasql(tmpv0);
var tmpv1 = donuts;
var output = tmpv1;
return output;
}
function abc(input){
var tmpv3 = input;
var tmpv4 = tmpv3.name;
var tmpv9 = input;
var tmpv10 = tmpv9.topping;
var tmpv11 = input;
var tmpv12 = tmpv9.price;
var tmpv6 = "insert into donuts (name,topping,price) values(${tmpv4},${tmpv10},${tmpv12})"
alasql(tmpv6);
var tmpv7 = `select * from donuts`;
var donuts = alasql(tmpv7);
var tmpv8 = donuts;
var output = tmpv8;
return output;
}
function abc(input){
var tmpv01 = input;
var tmpv3 = `select * from donuts where id =`+tmpv01;
var donuts = alasql(tmpv3);
var tmpv4 = donuts;
var output = tmpv4;
return output;
}
function abc(input){
var tmpv3 = input;
var tmpv4 = tmpv3.name;
var tmpv9 = input;
var tmpv10 = tmpv9.topping;
var tmpv11 = input;
var tmpv12 = tmpv11.id;
var tmpv10 = "update donuts set name = ${tmpv4}, topping = ${tmpv10} WHERE id = ${tmpv12}"
alasql(tmpv10);
var tmpv15 = `select * from donuts`;
var donuts = alasql(tmpv15);
var tmpv16 = donuts;
var output = tmpv16;
return output;
}
function abc(input){
var tmpv01 = input;
var tmpv14 = `delete from donuts WHERE id =`+tmpv01;
var donuts = alasql(tmpv14);
var tmpv16 = donuts;
var output = tmpv16;
return output;
}
// submit edit donut modal form
$(document).on('submit', '#modal-donut-form', function(event) {
  event.preventDefault();
  const donutID = $('#update-donut-id').val();
  const IS_SYNC = false;
if (IS_SYNC) {
   var data = abc(donutID);
  location.reload();
  return;
}//default: non-blocking async using Promise
else {
    new Promise((resolve, reject) => {
        var out_abcDe = abc(donutID);
        resolve(out_abcDe);
    }).then(
        res => {
            var data =res;
            location.reload();
        });
}
});

//add new donut
$(document).on('click', '.donut-add', function() {
  const $newDonutName = $('#newDonutName').val();
  const $newDonutTopping = $('#newDonutTopping').val();
  const $newDonutPrice = $('#newDonutPrice').val();
  const payload = {
    donut_name: $newDonutName,
    topping: $newDonutTopping,
    price: $newDonutPrice
  };
  const IS_SYNC = false;
if (IS_SYNC) {
   var data = abc(payload);
  location.reload();
  return;
}//default: non-blocking async using Promise
else {
    new Promise((resolve, reject) => {
        var out_abcDe = abc(payload);
        resolve(out_abcDe);
    }).then(
        res => {
            var data =res;
            location.reload();
        });
}
});

//fill in edit donut modal
$(document).on('click', '.donut-edit', function() {
  const $this = $(this);
  const donutID = $this.attr('data-id');
  const topping = $this.attr('data-topping');
  const name = $this.attr('data-name');
  const price = $this.attr('data-price');
  $('#update-donut-name').val(name);
  $('#update-donut-topping').val(topping);
  $('#update-donut-price').val(price);
  $('#update-donut-id').val(donutID);
});

// submit edit donut modal form
$(document).on('submit', '#modal-donut-form', function(event) {
  event.preventDefault();
  const $name = $('#update-donut-name').val();
  const $price = $('#update-donut-price').val();
  const $topping = $('#update-donut-topping').val();
  const donutID = $('#update-donut-id').val();
  const payload = {
    name: $name,
    price: $price,
    topping: $topping
  };
    const IS_SYNC = false;
if (IS_SYNC) {
   var data = abc(payload);
    $('#myModal').modal('toggle');
  location.reload();
  return;
}//default: non-blocking async using Promise
else {
    new Promise((resolve, reject) => {
        var out_abcDe = abc(payload);
        resolve(out_abcDe);
    }).then(
        res => {
            var data =res;
             $('#myModal').modal('toggle');
            location.reload();
        });
}
});

// delete donut button
$(document).on('click', '.donut-delete', function() {
  const answer = confirm('Are you sure?');
  if (answer) {
    const $this = $(this);
    const donutID = $this.attr('data-id');
    const IS_SYNC = false;
if (IS_SYNC) {
   var data = abc(donutID);
    $('#myModal').modal('toggle');
  location.reload();
  return;
}//default: non-blocking async using Promise
else {
    new Promise((resolve, reject) => {
        var out_abcDe = abc(donutID);
        resolve(out_abcDe);
    }).then(
        res => {
            var data =res;
            location.reload();
        });
}
  }
});

$(document).on('click', 'get-donut-btn', function() {
    const $this = $(this);
    const shopID = $this.attr('data-id');
      const IS_SYNC = false;
if (IS_SYNC) {
   var data = abc(shopID);
  location.reload();
  return;
}//default: non-blocking async using Promise
else {
    new Promise((resolve, reject) => {
        var out_abcDe = abc(shopID);
        resolve(out_abcDe);
    }).then(
        res => {
            var data =res;
            location.reload();
        });
}
});

$(document).on('click', 'get-donut-all', function() {
  const IS_SYNC = false;
  if (IS_SYNC) {
   var data = abc();
  location.reload();
  return;
}//default: non-blocking async using Promise
else {
    new Promise((resolve, reject) => {
        var out_abcDe = abc();
        resolve(out_abcDe);
    }).then(
        res => {
            var data =res;
            location.reload();
        });
}
});