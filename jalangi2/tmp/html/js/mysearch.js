J$.iids = {"9":[1,1,1,2],"10":[18,29,18,65],"17":[2,5,2,6],"25":[2,7,2,16],"33":[2,5,2,17],"41":[3,9,3,16],"49":[3,21,3,34],"57":[3,9,3,35],"59":[3,9,3,20],"65":[3,9,3,36],"73":[4,9,4,10],"81":[6,18,6,52],"89":[12,21,12,22],"97":[7,19,13,14],"105":[14,19,14,24],"113":[15,24,15,28],"121":[16,23,16,29],"129":[18,17,18,24],"137":[18,29,18,44],"145":[18,45,18,49],"153":[18,60,18,64],"161":[18,45,18,65],"163":[18,45,18,59],"169":[18,17,18,66],"171":[18,17,18,28],"177":[18,17,18,67],"185":[19,17,19,18],"193":[19,19,19,29],"201":[19,17,19,30],"209":[19,36,19,40],"217":[19,51,19,55],"225":[19,36,19,56],"227":[19,36,19,50],"233":[19,17,19,57],"235":[19,17,19,35],"241":[19,17,19,58],"249":[17,22,20,14],"257":[17,22,20,14],"265":[17,22,20,14],"273":[17,22,20,14],"281":[4,16,21,10],"289":[4,9,21,11],"291":[4,9,4,15],"297":[4,9,21,12],"305":[22,5,22,12],"313":[22,17,22,29],"321":[22,5,22,30],"323":[22,5,22,16],"329":[22,5,22,31],"337":[2,24,23,6],"345":[2,24,23,6],"353":[2,24,23,6],"361":[2,5,23,7],"363":[2,5,2,23],"369":[2,5,23,8],"377":[1,3,24,2],"385":[1,3,24,2],"393":[1,3,24,2],"401":[1,1,24,3],"409":[1,1,24,4],"417":[1,1,25,1],"425":[17,22,20,14],"433":[17,22,20,14],"441":[2,24,23,6],"449":[2,24,23,6],"457":[1,3,24,2],"465":[1,3,24,2],"473":[1,1,25,1],"481":[1,1,25,1],"nBranches":0,"originalCodeFileName":"tmp/html/js/mysearch_orig_.js","instrumentedCodeFileName":"tmp/html/js/mysearch.js","code":"$(function() {\n    $(\"#search\").click(function() {\n        console.log(\"test before\");\n        $.ajax({\n            //url: 'http://127.0.0.1:3001/users/search',\n            url: 'http://127.0.0.1:3000/brokers/id',\n            data: {\n                //firstName: $('#firstName').val(),\n                //lastName: $('#lastName').val()\n                //firstName: \"abcd\",\n                //lastName: \"edf\"\n                id: 4\n            },\n            type: 'GET',\n          crossDomain: true,\n            dataType: 'json',\n            success: function(data) {\n                console.log(\"sdfsafsafsf\\n\"+JSON.stringify(data));\n                $('#results').text(JSON.stringify(data));\n            }\n        });\n    console.log(\"test after\");\n    });\n});\n"};
jalangiLabel13:
    while (true) {
        try {
            J$.Se(417, 'tmp/html/js/mysearch.js', 'tmp/html/js/mysearch_orig_.js');
            J$.X1(409, J$.F(401, J$.R(9, '$', $, 2), 0)(J$.T(393, function () {
                jalangiLabel12:
                    while (true) {
                        try {
                            J$.Fe(377, arguments.callee, this, arguments);
                            arguments = J$.N(385, 'arguments', arguments, 4);
                            J$.X1(369, J$.M(361, J$.F(33, J$.R(17, '$', $, 2), 0)(J$.T(25, "#search", 21, false)), 'click', 0)(J$.T(353, function () {
                                jalangiLabel11:
                                    while (true) {
                                        try {
                                            J$.Fe(337, arguments.callee, this, arguments);
                                            arguments = J$.N(345, 'arguments', arguments, 4);
                                            J$.X1(65, J$.M(57, J$.R(41, 'console', console, 2), 'log', 0)(J$.T(49, "test before", 21, false)));
                                            J$.X1(297, J$.M(289, J$.R(73, '$', $, 2), 'ajax', 0)(J$.T(281, {
                                                url: J$.T(81, 'http://127.0.0.1:3000/brokers/id', 21, false),
                                                data: J$.T(97, {
                                                    id: J$.T(89, 4, 22, false)
                                                }, 11, false),
                                                type: J$.T(105, 'GET', 21, false),
                                                crossDomain: J$.T(113, true, 23, false),
                                                dataType: J$.T(121, 'json', 21, false),
                                                success: J$.T(273, function (data) {
                                                    jalangiLabel10:
                                                        while (true) {
                                                            try {
                                                                J$.Fe(249, arguments.callee, this, arguments);
                                                                arguments = J$.N(257, 'arguments', arguments, 4);
                                                                data = J$.N(265, 'data', data, 4);
                                                                J$.X1(177, J$.M(169, J$.R(129, 'console', console, 2), 'log', 0)(J$.B(10, '+', J$.T(137, "sdfsafsafsf\n", 21, false), J$.M(161, J$.R(145, 'JSON', JSON, 2), 'stringify', 0)(J$.R(153, 'data', data, 0)), 0)));
                                                                J$.X1(241, J$.M(233, J$.F(201, J$.R(185, '$', $, 2), 0)(J$.T(193, '#results', 21, false)), 'text', 0)(J$.M(225, J$.R(209, 'JSON', JSON, 2), 'stringify', 0)(J$.R(217, 'data', data, 0))));
                                                            } catch (J$e) {
                                                                J$.Ex(425, J$e);
                                                            } finally {
                                                                if (J$.Fr(433))
                                                                    continue jalangiLabel10;
                                                                else
                                                                    return J$.Ra();
                                                            }
                                                        }
                                                }, 12, false, 249)
                                            }, 11, false)));
                                            J$.X1(329, J$.M(321, J$.R(305, 'console', console, 2), 'log', 0)(J$.T(313, "test after", 21, false)));
                                        } catch (J$e) {
                                            J$.Ex(441, J$e);
                                        } finally {
                                            if (J$.Fr(449))
                                                continue jalangiLabel11;
                                            else
                                                return J$.Ra();
                                        }
                                    }
                            }, 12, false, 337)));
                        } catch (J$e) {
                            J$.Ex(457, J$e);
                        } finally {
                            if (J$.Fr(465))
                                continue jalangiLabel12;
                            else
                                return J$.Ra();
                        }
                    }
            }, 12, false, 377)));
        } catch (J$e) {
            J$.Ex(473, J$e);
        } finally {
            if (J$.Sr(481)) {
                J$.L();
                continue jalangiLabel13;
            } else {
                J$.L();
                break jalangiLabel13;
            }
        }
    }
// JALANGI DO NOT INSTRUMENT
