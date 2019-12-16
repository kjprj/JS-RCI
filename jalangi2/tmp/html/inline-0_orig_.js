
/**
$(function() {
//    $("#search").click(function() {
        $.ajax({
            url: 'http://127.0.0.1:3001/users/search',
            data: {
                firstName: $('#firstName').val(),
                lastName: $('#lastName').val()
            },
            type: 'POST',
            success: function(data) {
                $('#results').text(JSON.stringify(data));
            },
	    datatype='jsonp'
        })
//    });
});
**/
/**
        console.log("started");
    $.ajax({
    //url: 'http://'+Migrator.domain+'/migrator/interp.php',   //proxy page
    //             url: 'http://128.173.239.239/migrator/interp.php',   //proxy page
    // url: 'http://128.173.239.239:1340',   //proxy page
    url: 'http://127.0.0.1:3001/users/search',
    type: 'GET',      //POST method
   // async: false,      //ajax sync
        // url: "/users/add",
        // method: "post",
        data: {name: "first guy",
            p1:"p1",
            p2:"p2",
            p3:"p3"
        },
    // data: '{name: "first guy"},
    // dataType : 'jsonp',   //you may use jsonp for cross origin request
    // data:'Migrator.getFunctionThisObject("'+funcName+'");'+funcName+' = '+functionString+';',
    success: function(msg) {
//   var stop = process.hrtime();
//   var stopstop = stop[0]*1e9 + stop[1];
 //  var startstart = start[0]*1e9 + start[1];
   // var aaa = (stopstop-startstart);
   // console.log("aaaa  "+aaa+"ns  ,"+aaa/1000000+"ms");
    console.log("success    "+msg);
    },
    dataType: "json"
    });
**/
   
