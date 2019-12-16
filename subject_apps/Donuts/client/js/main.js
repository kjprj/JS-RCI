function abc(){
var tmpv0 = "select * from shops order by id asc";
var shops = alasql(tmpv0);
var tmpv1 = shops;
var output = tmpv1;
return output;
}
function abc(input){
var tmpv1 = input;
var tmpv6 = "insert into shops (name,city) values(${tmpv1.name},${tmpv1.city})";
var shops = alasql(tmpv6);
var output = tmpv21;
return output;
}
function abc(input){
var tmpv1 = input;
var tmpv3 = "select * from shops where id = ${tmpv1}"
var shops = alasql(tmpv3);
var output = tmpv21;
return output;
}
function abc(input){
var tmpv1 = input;
var tmpv3 = "delete from shops WHERE id = ${tmpv1}";
alasql(tmpv3);
var tmpv11 = "select * from shops";
var shops = alasql(tmpv11);
var tmpv12 = shops;
var output = tmpv12;
return output;
}
//click of open update modal
$(document).on('click', '.update-shop-btn', function() {
  const $this = $(this);
  const shopID = $this.attr('data-id');
  console.log(shopID);
  const city = $this.attr('data-city');
  const name = $this.attr('data-name');
  $('#update-shop-name').val(name);
  $('#update-shop-city').val(city);
  $('#update-shop-id').val(shopID);
});

// submit edit shop form
$(document).on('submit', '#modal-shop-form', function(event) {
  event.preventDefault();
  const $name = $('#update-shop-name').val();
  const $city = $('#update-shop-city').val();
  const shopID = $('#update-shop-id').val();
  const payload = {
    name: $name,
    city: $city
  };
   const IS_SYNC = false;
if (IS_SYNC) {
   var data = abc(shopID);
  location.reload();
  return;
}//default: non-blocking async using Promise
else {
    new Promise((resolve, reject) => {
        var out_abcDe = abc(shopID,payload);
        resolve(out_abcDe);
    }).then(
        res => {
            var data =res;
             $('#myModal').modal('toggle');
            location.reload();
        });
}
});
// delete shop button
$(document).on('click', '.delete-shop-btn', function() {
  const answer = confirm('Are you sure?');
  if (answer) {
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
  }
});
//list group form select employees
$(function () {
    $('.list-group.checked-list-box .list-group-item').each(function () {

        // Settings
        var $widget = $(this),
            $checkbox = $('<input type="checkbox" class="hidden" />'),
            color = ($widget.data('color') ? $widget.data('color') : "primary"),
            style = ($widget.data('style') == "button" ? "btn-" : "list-group-item-"),
            settings = {
                on: {
                    icon: 'glyphicon glyphicon-check'
                },
                off: {
                    icon: 'glyphicon glyphicon-unchecked'
                }
            };

        $widget.css('cursor', 'pointer')
        $widget.append($checkbox);

        // Event Handlers
        $widget.on('click', function () {
            $checkbox.prop('checked', !$checkbox.is(':checked'));
            $checkbox.triggerHandler('change');
            updateDisplay();
        });
        $checkbox.on('change', function () {
            updateDisplay();
        });

// Actions
        function updateDisplay() {
            var isChecked = $checkbox.is(':checked');

            // Set the button's state
            $widget.data('state', (isChecked) ? "on" : "off");

            // Set the button's icon
            $widget.find('.state-icon')
                .removeClass()
                .addClass('state-icon ' + settings[$widget.data('state')].icon);

// Update the button's color
            if (isChecked) {
                $widget.addClass(style + color + ' active');
            } else {
                $widget.removeClass(style + color + ' active');
            }
        }

// Initialization
        function init() {

            if ($widget.data('checked') == true) {
                $checkbox.prop('checked', !$checkbox.is(':checked'));
            }

            updateDisplay();

            // Inject the icon if applicable
            if ($widget.find('.state-icon').length == 0) {
                $widget.prepend('<span class="state-icon ' + settings[$widget.data('state')].icon + '"></span>');
            }
        }
        init();
    });
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