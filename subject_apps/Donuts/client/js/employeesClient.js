function abc(){
var tmpv0 = "select * from employee order by id asc";
var employee = alasql(tmpv0);
  var tmpv1 = employee;
var output = tmpv1;
return output;
}
function abc(input){
 var tmpv6 = input;
  var tmpv11 = "insert into employee (first_name,last_name,favorite_donut,shop_id) values(${tmpv6.first_name},${tmpv6.last_name},${tmpv6.favorite_donut},${tmpv6.shop_id})";
alasql(tmpv11);
var tmpv12 = "select * from employee";
var employee = alasql(tmpv20);
var tmpv13 = employee;
var output = tmpv21;
return output;
}
function abc(input){
	var tmpv6 = input;
	var tmpv7 = "select * from employee where id = ${tmpv6}";
	var employee = alasql(tmpv7);
   var tmpv9 = {
    employee:undefined};
    var tmpv24 = employee;
    tmpv9.employee = tmpv24;
var output = tmpv9;
return output;
}
function abc(input){
var tmpv6 = input;
  var tmpv19 = "delete from employee WHERE id = ${tmpv6}";
var employee = alasql(tmpv19);
var tmpv21 = employee;
var output = tmpv21;
return output;
}
function abc(input){
var tmpv6 = input;
var tmpv7 = input;
var tmpv15 = "update employee set first_name = ${tmpv6.first_name}, last_name = ${tmpv6.last_name}, favorite_donut = ${tmpv6.favorite_donut}, shop_id = ${tmpv6.shop_id} WHERE id = ${tmpv7.id}";
var employee = alasql(tmpv19);
var tmpv20 = "select * from employee";
var employee = alasql(tmpv20);
var tmpv21 = employee;
var output = tmpv21;
return output;
}

//add new employee
$(document).on('click', '.employee-add', function() {
  const $newEmployeeFirstName = $('#newEmployeeFirstName').val();
  const $newEmployeeLastName = $('#newEmployeeLastName').val();
  const $favorite_donut = $('#favorite_donut').val();
  const $shop_id = $('#shop_id').val();
  const payload = {
    first_name: $newEmployeeFirstName,
    last_name: $newEmployeeLastName,
    favorite_donut: $favorite_donut,
      shop_id:$shop_id
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

//fill in edit employee modal
$(document).on('click', '.employee-edit', function() {
  const $this = $(this);
  const employeeID = $this.attr('data-id');
  const first_name = $this.attr('data-first_name');
  const last_name = $this.attr('data-last_name');
  const email = $this.attr('data-email');
  $('#update-employee-first_name').val(first_name);
  $('#update-employee-last_name').val(last_name);
  $('#update-employee-email').val(email);
  $('#update-employee-id').val(employeeID);
});

// submit edit employee modal form
$(document).on('submit', '#modal-employee-form', function(event) {
  event.preventDefault();
  const $first_name = $('#update-employee-first_name').val();
  const $last_name = $('#update-employee-last_name').val();
  const $favorite_donut = $('#favorite_donut').val();
  const $shop_id = $('#shop_id').val();
  const payload = {
    first_name: $first_name,
    last_name: $last_name,
    favorite_donut: $favorite_donut,
      shop_id:$shop_id
  };
   const IS_SYNC = false;
if (IS_SYNC) {
   var data = abc(employeeID,payload);
  location.reload();
      $('#myModal').modal('toggle');
  return;
}//default: non-blocking async using Promise
else {
    new Promise((resolve, reject) => {
        var out_abcDe = abc(employeeID,payload);
        resolve(out_abcDe);
    }).then(
        res => {
            var data =res;
                $('#myModal').modal('toggle');
            location.reload();
        });
}
});

// delete employee button
$(document).on('click', '.employee-delete', function() {
  const answer = confirm('Are you sure?');
  if (answer) {
    const $this = $(this);
    const employeeID = $this.attr('data-id');
  const IS_SYNC = false;
if (IS_SYNC) {
   var data = abc(employeeID);
  location.reload();
  return;
}//default: non-blocking async using Promise
else {
    new Promise((resolve, reject) => {
        var out_abcDe = abc(employeeID);
        resolve(out_abcDe);
    }).then(
        res => {
            var data =res;
            location.reload();
        });
}
  }
});
$(document).on('click', 'get-shop-btn', function() {
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

$(document).on('click', 'get-shop-all', function() {
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