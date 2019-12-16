J$.iids = {"9":[1,1,1,2],"17":[2,5,2,6],"25":[2,7,2,16],"33":[2,5,2,17],"41":[3,9,3,16],"49":[3,21,3,34],"57":[3,9,3,35],"59":[3,9,3,20],"65":[3,9,3,36],"73":[4,9,4,10],"81":[5,18,5,54],"89":[9,28,9,34],"97":[10,27,10,32],"105":[6,19,11,14],"113":[12,19,12,25],"121":[13,24,13,28],"129":[14,23,14,29],"137":[16,17,16,24],"145":[16,29,16,42],"153":[16,17,16,43],"155":[16,17,16,28],"161":[16,17,16,44],"169":[17,17,17,18],"177":[17,19,17,29],"185":[17,17,17,30],"193":[17,36,17,40],"201":[17,51,17,55],"209":[17,36,17,56],"211":[17,36,17,50],"217":[17,17,17,57],"219":[17,17,17,35],"225":[17,17,17,58],"233":[15,22,18,14],"241":[15,22,18,14],"249":[15,22,18,14],"257":[15,22,18,14],"265":[4,16,19,10],"273":[4,9,19,11],"275":[4,9,4,15],"281":[4,9,19,12],"289":[20,5,20,12],"297":[20,17,20,29],"305":[20,5,20,30],"307":[20,5,20,16],"313":[20,5,20,31],"321":[2,24,21,6],"329":[2,24,21,6],"337":[2,24,21,6],"345":[2,5,21,7],"347":[2,5,2,23],"353":[2,5,21,8],"361":[1,3,22,2],"369":[1,3,22,2],"377":[1,3,22,2],"385":[1,1,22,3],"393":[1,1,22,4],"401":[1,1,23,1],"409":[15,22,18,14],"417":[15,22,18,14],"425":[2,24,21,6],"433":[2,24,21,6],"441":[1,3,22,2],"449":[1,3,22,2],"457":[1,1,23,1],"465":[1,1,23,1],"nBranches":0,"originalCodeFileName":"tmp/html/js/search_orig_.js","instrumentedCodeFileName":"tmp/html/js/search.js","code":"$(function() {\n    $(\"#search\").click(function() {\n        console.log(\"test before\");\n        $.ajax({\n            url: 'http://127.0.0.1:3001/users/search',\n            data: {\n                //firstName: $('#firstName').val(),\n                //lastName: $('#lastName').val()\n                firstName: \"abcd\",\n                lastName: \"edf\"\n            },\n            type: 'POST',\n          crossDomain: true,\n            dataType: 'json',\n            success: function(data) {\n                console.log(\"sdfsafsafsf\");\n                $('#results').text(JSON.stringify(data));\n            }\n        });\n    console.log(\"test after\");\n    });\n});\n"};
jalangiLabel17:
    while (true) {
        try {
            J$.Se(401, 'tmp/html/js/search.js', 'tmp/html/js/search_orig_.js');
            J$.X1(393, J$.F(385, J$.R(9, '$', $, 2), 0)(J$.T(377, function () {
                jalangiLabel16:
                    while (true) {
                        try {
                            J$.Fe(361, arguments.callee, this, arguments);
                            arguments = J$.N(369, 'arguments', arguments, 4);
                            J$.X1(353, J$.M(345, J$.F(33, J$.R(17, '$', $, 2), 0)(J$.T(25, "#search", 21, false)), 'click', 0)(J$.T(337, function () {
                                jalangiLabel15:
                                    while (true) {
                                        try {
                                            J$.Fe(321, arguments.callee, this, arguments);
                                            arguments = J$.N(329, 'arguments', arguments, 4);
                                            J$.X1(65, J$.M(57, J$.R(41, 'console', console, 2), 'log', 0)(J$.T(49, "test before", 21, false)));
                                            J$.X1(281, J$.M(273, J$.R(73, '$', $, 2), 'ajax', 0)(J$.T(265, {
                                                url: J$.T(81, 'http://127.0.0.1:3001/users/search', 21, false),
                                                data: J$.T(105, {
                                                    firstName: J$.T(89, "abcd", 21, false),
                                                    lastName: J$.T(97, "edf", 21, false)
                                                }, 11, false),
                                                type: J$.T(113, 'POST', 21, false),
                                                crossDomain: J$.T(121, true, 23, false),
                                                dataType: J$.T(129, 'json', 21, false),
                                                success: J$.T(257, function (data) {
                                                    jalangiLabel14:
                                                        while (true) {
                                                            try {
                                                                J$.Fe(233, arguments.callee, this, arguments);
                                                                arguments = J$.N(241, 'arguments', arguments, 4);
                                                                data = J$.N(249, 'data', data, 4);
                                                                J$.X1(161, J$.M(153, J$.R(137, 'console', console, 2), 'log', 0)(J$.T(145, "sdfsafsafsf", 21, false)));
                                                                J$.X1(225, J$.M(217, J$.F(185, J$.R(169, '$', $, 2), 0)(J$.T(177, '#results', 21, false)), 'text', 0)(J$.M(209, J$.R(193, 'JSON', JSON, 2), 'stringify', 0)(J$.R(201, 'data', data, 0))));
                                                            } catch (J$e) {
                                                                J$.Ex(409, J$e);
                                                            } finally {
                                                                if (J$.Fr(417))
                                                                    continue jalangiLabel14;
                                                                else
                                                                    return J$.Ra();
                                                            }
                                                        }
                                                }, 12, false, 233)
                                            }, 11, false)));
                                            J$.X1(313, J$.M(305, J$.R(289, 'console', console, 2), 'log', 0)(J$.T(297, "test after", 21, false)));
                                        } catch (J$e) {
                                            J$.Ex(425, J$e);
                                        } finally {
                                            if (J$.Fr(433))
                                                continue jalangiLabel15;
                                            else
                                                return J$.Ra();
                                        }
                                    }
                            }, 12, false, 321)));
                        } catch (J$e) {
                            J$.Ex(441, J$e);
                        } finally {
                            if (J$.Fr(449))
                                continue jalangiLabel16;
                            else
                                return J$.Ra();
                        }
                    }
            }, 12, false, 361)));
        } catch (J$e) {
            J$.Ex(457, J$e);
        } finally {
            if (J$.Sr(465)) {
                J$.L();
                continue jalangiLabel17;
            } else {
                J$.L();
                break jalangiLabel17;
            }
        }
    }
// JALANGI DO NOT INSTRUMENT
