J$.iids = {"8":[7,21,7,49],"9":[1,11,1,13],"10":[4,19,4,35],"16":[6,17,6,41],"17":[1,11,1,13],"18":[4,37,4,40],"24":[4,19,4,35],"25":[1,11,1,13],"33":[3,21,3,23],"34":[4,37,4,40],"41":[3,21,3,23],"42":[7,21,7,49],"49":[3,21,3,23],"57":[4,16,4,17],"65":[4,16,4,17],"73":[4,16,4,17],"81":[4,19,4,20],"89":[4,23,4,28],"97":[4,23,4,35],"113":[4,37,4,38],"121":[4,37,4,40],"137":[5,26,5,29],"145":[6,17,6,20],"153":[6,36,6,40],"161":[6,17,6,41],"163":[6,17,6,35],"169":[7,21,7,24],"177":[7,25,7,29],"185":[7,21,7,30],"193":[7,35,7,40],"201":[7,41,7,42],"209":[7,35,7,43],"217":[7,44,7,48],"225":[7,35,7,49],"233":[8,21,8,30],"241":[8,36,8,41],"249":[8,42,8,43],"257":[8,36,8,44],"265":[8,21,8,45],"267":[8,21,8,35],"273":[8,21,8,46],"281":[5,26,5,29],"289":[5,9,12,10],"297":[5,9,12,10],"305":[14,12,14,21],"313":[14,12,14,21],"321":[14,5,14,22],"329":[2,1,15,2],"337":[2,1,15,2],"345":[2,1,15,2],"353":[2,1,15,2],"361":[2,1,15,2],"369":[2,1,15,2],"377":[2,1,15,2],"385":[17,12,17,26],"393":[17,27,17,37],"401":[17,39,17,44],"409":[17,12,17,45],"417":[17,12,17,45],"425":[17,5,17,46],"433":[16,1,18,2],"441":[16,1,18,2],"449":[16,1,18,2],"457":[20,15,20,20],"465":[20,15,20,20],"473":[20,15,20,20],"481":[21,18,21,26],"489":[21,27,21,32],"497":[21,18,21,33],"505":[21,18,21,33],"513":[21,18,21,33],"521":[22,12,22,18],"529":[22,12,22,18],"537":[22,5,22,19],"545":[19,1,23,2],"553":[19,1,23,2],"561":[19,1,23,2],"569":[19,1,23,2],"577":[25,19,25,31],"585":[25,32,25,37],"593":[25,19,25,38],"601":[25,19,25,38],"609":[25,19,25,38],"617":[26,19,26,23],"625":[26,34,26,41],"633":[26,19,26,42],"635":[26,19,26,33],"641":[26,19,26,42],"649":[26,19,26,42],"657":[27,12,27,19],"665":[27,12,27,19],"673":[27,5,27,20],"681":[24,1,28,2],"689":[24,1,28,2],"697":[24,1,28,2],"705":[24,1,28,2],"713":[24,1,28,2],"721":[29,1,29,8],"729":[29,20,29,28],"737":[29,1,29,28],"745":[29,1,29,29],"753":[31,13,31,15],"761":[31,13,31,15],"769":[31,13,31,15],"777":[32,14,32,38],"785":[32,39,32,44],"793":[32,14,32,45],"801":[32,14,32,45],"809":[32,14,32,45],"817":[34,1,34,2],"825":[34,3,34,13],"833":[34,1,34,14],"841":[34,20,34,24],"849":[34,35,34,41],"857":[34,20,34,42],"859":[34,20,34,34],"865":[34,1,34,43],"867":[34,1,34,19],"873":[34,1,34,44],"881":[1,1,35,1],"889":[1,1,35,1],"897":[2,1,15,2],"905":[1,1,35,1],"913":[16,1,18,2],"921":[1,1,35,1],"929":[19,1,23,2],"937":[1,1,35,1],"945":[24,1,28,2],"953":[1,1,35,1],"961":[1,1,35,1],"969":[1,1,35,1],"977":[7,17,10,18],"985":[6,13,11,14],"993":[4,5,13,6],"1001":[4,5,13,6],"1009":[2,1,15,2],"1017":[2,1,15,2],"1025":[16,1,18,2],"1033":[16,1,18,2],"1041":[19,1,23,2],"1049":[19,1,23,2],"1057":[24,1,28,2],"1065":[24,1,28,2],"1073":[1,1,35,1],"1081":[1,1,35,1],"nBranches":6,"originalCodeFileName":"tmp/html/js/insourced_search_orig_.js","instrumentedCodeFileName":"tmp/html/js/insourced_search.js","code":"var users=[];\nfunction getObjsInArray(obj, array) {\n    var foundObjs = [];\n    for (var i=0; i < array.length; i++) {\n        for (var prop in obj) {\n            if (obj.hasOwnProperty(prop)) {\n                if (obj[prop] === array[i][prop]) {\n                    foundObjs.push(array[i]);\n                    break;\n                }\n            }\n        }\n    }\n    return foundObjs;\n}\nfunction getUsers(searchUser) {\n    return getObjsInArray(searchUser, users);\n}\nfunction users_search(input){\n    var input=input;\n    var output = getUsers(input);\n    return output;\n}\nfunction centralized_users_search(input) {\n    var output0 = users_search(input);\n    var output1 = JSON.stringify(output0);\n    return output1;\n}\nexports.getUsers = getUsers;\n\nvar input = {};\nvar output = centralized_users_search(input);\n\n$('#results').text(JSON.stringify(output));\n"};
jalangiLabel172:
    while (true) {
        try {
            J$.Se(881, 'tmp/html/js/insourced_search.js', 'tmp/html/js/insourced_search_orig_.js');
            function getObjsInArray(obj, array) {
                jalangiLabel168:
                    while (true) {
                        try {
                            J$.Fe(329, arguments.callee, this, arguments);
                            arguments = J$.N(337, 'arguments', arguments, 4);
                            obj = J$.N(345, 'obj', obj, 4);
                            array = J$.N(353, 'array', array, 4);
                            J$.N(361, 'foundObjs', foundObjs, 0);
                            J$.N(369, 'i', i, 0);
                            J$.N(377, 'prop', prop, 0);
                            var foundObjs = J$.X1(49, J$.W(41, 'foundObjs', J$.T(33, [], 10, false), foundObjs, 1));
                            for (var i = J$.X1(73, J$.W(65, 'i', J$.T(57, 0, 22, false), i, 1)); J$.X1(993, J$.C(24, J$.B(10, '<', J$.R(81, 'i', i, 0), J$.G(97, J$.R(89, 'array', array, 0), 'length', 0), 0))); J$.X1(1001, J$.B(34, '-', i = J$.W(121, 'i', J$.B(26, '+', J$.U(18, '+', J$.R(113, 'i', i, 0)), J$.T(105, 1, 22, false), 0), i, 0), J$.T(129, 1, 22, false), 0))) {
                                for (J$._tm_p in J$.H(281, J$.R(137, 'obj', obj, 0))) {
                                    var prop = J$.X1(297, J$.W(289, 'prop', J$._tm_p, prop, 1));
                                    {
                                        {
                                            if (J$.X1(985, J$.C(16, J$.M(161, J$.R(145, 'obj', obj, 0), 'hasOwnProperty', 0)(J$.R(153, 'prop', prop, 0))))) {
                                                if (J$.X1(977, J$.C(8, J$.B(42, '===', J$.G(185, J$.R(169, 'obj', obj, 0), J$.R(177, 'prop', prop, 0), 4), J$.G(225, J$.G(209, J$.R(193, 'array', array, 0), J$.R(201, 'i', i, 0), 4), J$.R(217, 'prop', prop, 0), 4), 0)))) {
                                                    J$.X1(273, J$.M(265, J$.R(233, 'foundObjs', foundObjs, 0), 'push', 0)(J$.G(257, J$.R(241, 'array', array, 0), J$.R(249, 'i', i, 0), 4)));
                                                    break;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            return J$.X1(321, J$.Rt(313, J$.R(305, 'foundObjs', foundObjs, 0)));
                        } catch (J$e) {
                            J$.Ex(1009, J$e);
                        } finally {
                            if (J$.Fr(1017))
                                continue jalangiLabel168;
                            else
                                return J$.Ra();
                        }
                    }
            }
            function getUsers(searchUser) {
                jalangiLabel169:
                    while (true) {
                        try {
                            J$.Fe(433, arguments.callee, this, arguments);
                            arguments = J$.N(441, 'arguments', arguments, 4);
                            searchUser = J$.N(449, 'searchUser', searchUser, 4);
                            return J$.X1(425, J$.Rt(417, J$.F(409, J$.R(385, 'getObjsInArray', getObjsInArray, 1), 0)(J$.R(393, 'searchUser', searchUser, 0), J$.R(401, 'users', users, 1))));
                        } catch (J$e) {
                            J$.Ex(1025, J$e);
                        } finally {
                            if (J$.Fr(1033))
                                continue jalangiLabel169;
                            else
                                return J$.Ra();
                        }
                    }
            }
            function users_search(input) {
                jalangiLabel170:
                    while (true) {
                        try {
                            J$.Fe(545, arguments.callee, this, arguments);
                            arguments = J$.N(553, 'arguments', arguments, 4);
                            input = J$.N(561, 'input', input, 4);
                            J$.N(569, 'output', output, 0);
                            var input = J$.X1(473, J$.W(465, 'input', J$.R(457, 'input', input, 0), input, 1));
                            var output = J$.X1(513, J$.W(505, 'output', J$.F(497, J$.R(481, 'getUsers', getUsers, 1), 0)(J$.R(489, 'input', input, 0)), output, 1));
                            return J$.X1(537, J$.Rt(529, J$.R(521, 'output', output, 0)));
                        } catch (J$e) {
                            J$.Ex(1041, J$e);
                        } finally {
                            if (J$.Fr(1049))
                                continue jalangiLabel170;
                            else
                                return J$.Ra();
                        }
                    }
            }
            function centralized_users_search(input) {
                jalangiLabel171:
                    while (true) {
                        try {
                            J$.Fe(681, arguments.callee, this, arguments);
                            arguments = J$.N(689, 'arguments', arguments, 4);
                            input = J$.N(697, 'input', input, 4);
                            J$.N(705, 'output0', output0, 0);
                            J$.N(713, 'output1', output1, 0);
                            var output0 = J$.X1(609, J$.W(601, 'output0', J$.F(593, J$.R(577, 'users_search', users_search, 1), 0)(J$.R(585, 'input', input, 0)), output0, 1));
                            var output1 = J$.X1(649, J$.W(641, 'output1', J$.M(633, J$.R(617, 'JSON', JSON, 2), 'stringify', 0)(J$.R(625, 'output0', output0, 0)), output1, 1));
                            return J$.X1(673, J$.Rt(665, J$.R(657, 'output1', output1, 0)));
                        } catch (J$e) {
                            J$.Ex(1057, J$e);
                        } finally {
                            if (J$.Fr(1065))
                                continue jalangiLabel171;
                            else
                                return J$.Ra();
                        }
                    }
            }
            J$.N(889, 'users', users, 0);
            getObjsInArray = J$.N(905, 'getObjsInArray', J$.T(897, getObjsInArray, 12, false, 329), 0);
            getUsers = J$.N(921, 'getUsers', J$.T(913, getUsers, 12, false, 433), 0);
            users_search = J$.N(937, 'users_search', J$.T(929, users_search, 12, false, 545), 0);
            centralized_users_search = J$.N(953, 'centralized_users_search', J$.T(945, centralized_users_search, 12, false, 681), 0);
            J$.N(961, 'input', input, 0);
            J$.N(969, 'output', output, 0);
            var users = J$.X1(25, J$.W(17, 'users', J$.T(9, [], 10, false), users, 3));
            J$.X1(745, J$.P(737, J$.R(721, 'exports', exports, 2), 'getUsers', J$.R(729, 'getUsers', getUsers, 1), 0));
            var input = J$.X1(769, J$.W(761, 'input', J$.T(753, {}, 11, false), input, 3));
            var output = J$.X1(809, J$.W(801, 'output', J$.F(793, J$.R(777, 'centralized_users_search', centralized_users_search, 1), 0)(J$.R(785, 'input', input, 1)), output, 3));
            J$.X1(873, J$.M(865, J$.F(833, J$.R(817, '$', $, 2), 0)(J$.T(825, '#results', 21, false)), 'text', 0)(J$.M(857, J$.R(841, 'JSON', JSON, 2), 'stringify', 0)(J$.R(849, 'output', output, 1))));
        } catch (J$e) {
            J$.Ex(1073, J$e);
        } finally {
            if (J$.Sr(1081)) {
                J$.L();
                continue jalangiLabel172;
            } else {
                J$.L();
                break jalangiLabel172;
            }
        }
    }
// JALANGI DO NOT INSTRUMENT
