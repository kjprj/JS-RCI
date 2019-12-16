J$.iids = {"9":[1,1,51,1],"17":[1,1,51,1],"25":[1,1,51,1],"nBranches":0,"originalCodeFileName":"inline-0_orig_.js","instrumentedCodeFileName":"inline-0.js","code":"\n/**\n$(function() {\n//    $(\"#search\").click(function() {\n        $.ajax({\n            url: 'http://127.0.0.1:3001/users/search',\n            data: {\n                firstName: $('#firstName').val(),\n                lastName: $('#lastName').val()\n            },\n            type: 'POST',\n            success: function(data) {\n                $('#results').text(JSON.stringify(data));\n            },\n\t    datatype='jsonp'\n        })\n//    });\n});\n**/\n/**\n        console.log(\"started\");\n    $.ajax({\n    //url: 'http://'+Migrator.domain+'/migrator/interp.php',   //proxy page\n    //             url: 'http://128.173.239.239/migrator/interp.php',   //proxy page\n    // url: 'http://128.173.239.239:1340',   //proxy page\n    url: 'http://127.0.0.1:3001/users/search',\n    type: 'GET',      //POST method\n   // async: false,      //ajax sync\n        // url: \"/users/add\",\n        // method: \"post\",\n        data: {name: \"first guy\",\n            p1:\"p1\",\n            p2:\"p2\",\n            p3:\"p3\"\n        },\n    // data: '{name: \"first guy\"},\n    // dataType : 'jsonp',   //you may use jsonp for cross origin request\n    // data:'Migrator.getFunctionThisObject(\"'+funcName+'\");'+funcName+' = '+functionString+';',\n    success: function(msg) {\n//   var stop = process.hrtime();\n//   var stopstop = stop[0]*1e9 + stop[1];\n //  var startstart = start[0]*1e9 + start[1];\n   // var aaa = (stopstop-startstart);\n   // console.log(\"aaaa  \"+aaa+\"ns  ,\"+aaa/1000000+\"ms\");\n    console.log(\"success    \"+msg);\n    },\n    dataType: \"json\"\n    });\n**/\n   \n"};
jalangiLabel0:
    while (true) {
        try {
            J$.Se(9, 'inline-0.js', 'inline-0_orig_.js');
        } catch (J$e) {
            J$.Ex(17, J$e);
        } finally {
            if (J$.Sr(25)) {
                J$.L();
                continue jalangiLabel0;
            } else {
                J$.L();
                break jalangiLabel0;
            }
        }
    }
// JALANGI DO NOT INSTRUMENT
