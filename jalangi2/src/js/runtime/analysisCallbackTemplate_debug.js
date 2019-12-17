/*
FROM jalangi2/src/js/runtime/analysisCallbackTemplate.js

// do not remove the following comment
// JALANGI DO NOT INSTRUMENT

 */


var sqlInvocations =[];
var exitPointMap = {};
var getFieldsMap = {};
var entryPointMap = {};
var entryPointValMap = {};
var passedEntry = false;
var path = require('path');
var format = require("string-template");
var polycrc = require('polycrc');
var constraints_solver = require('../../../../src/Insourcing')
var uuid = 0;
J$.mashallingLog ={};
// var insourcing = require('src/dummyInsourcing');
J$.sqlInvocationsMap ={};
var lineColumn = require("line-column");
J$.toRollback = false;
//J$.toRollback = false;
var colors = require("colors/safe");
var fs = require('fs');
var underscore = require('underscore');
var esprima = require('esprima');
var estraverse = require('estraverse');
const { parse } = require('json2csv');
//var csvData = parse(JSON.parse(JSON.stringify(args[1])));
var code = fs.readFileSync("./test1.json").toString();
var aaa = JSON.parse(code);
console.log(JSON.stringify(aaa));
//console.log("parsejson2csv", parse );
var NUM = 9999;
const { Parser } = require('node-sql-parser');
const sqlParser = new Parser();
//const save_table = 'SELECT * FROM recipes';
J$.SAVE_TABLE = "SELECT * FROM recipes";

var gen_rw_inputs={};

function aabbba(a1, b1) {
jalangiLabel1026:
    while (true) {
        try {
            J$.Fe(193, arguments.callee, this, arguments);
            arguments = J$.N(201, 'arguments', arguments, 4);
            a1 = J$.N(209, 'a1', a1, 4);
            b1 = J$.N(217, 'b1', b1, 4);
            J$.X1(161, JSRCI_var = J$.W(153, 'JSRCI_var', J$.R(145, 'a1', a1, 0), JSRCI_var, 2));
            J$.X1(185, JSRCI_ob = J$.W(177, 'JSRCI_ob', J$.R(169, 'b1', b1, 0), JSRCI_ob, 2));
        } catch (J$e) {
            J$.Ex(2969, J$e);
        } finally {
            if (J$.Fr(2977))
                continue jalangiLabel1026;
            else
                return J$.Ra();
        }
    }
}


(function (sandbox) {


sandbox.TraceWriter = function (traceFileName) {
        var Constants = sandbox.Constants;
        var Config = sandbox.Config;

        var bufferSize = 0;
        var buffer = [];
        var traceWfh;
        var fs = (!Constants.isBrowser) ? require('fs') : undefined;
        var trying = false;
        var cb;
        var remoteBuffer = [];
        var socket, isOpen = false;
        // if true, in the process of doing final trace dump,
        // so don't record any more events
        var tracingDone = false;

        function getFileHanlde() {
            if (traceWfh === undefined) {
                traceWfh = fs.openSync(traceFileName, 'w');
            }
            return traceWfh;
        }

        /**
         * @param {string} line
         */
        this.logToFile = function (line) {
            if (tracingDone) {
                // do nothing
                return;
            }
            var len = line.length;
            // we need this loop because it's possible that len >= Config.MAX_BUF_SIZE
            // TODO fast path for case where len < Config.MAX_BUF_SIZE?
            var start = 0, end = len < Config.MAX_BUF_SIZE ? len : Config.MAX_BUF_SIZE;
            while (start < len) {
                var chunk = line.substring(start, end);
                var curLen = end - start;
                if (bufferSize + curLen > Config.MAX_BUF_SIZE) {
                    this.flush();
                }
                buffer.push(chunk);
                bufferSize += curLen;
                start = end;
                end = (end + Config.MAX_BUF_SIZE < len) ? end + Config.MAX_BUF_SIZE : len;
            }
        };

        this.flush = function () {
            var msg;
            if (!Constants.isBrowser) {
                var length = buffer.length;
                for (var i = 0; i < length; i++) {
                    fs.writeSync(getFileHanlde(), buffer[i]);
                }
            } else {
                msg = buffer.join('');
                if (msg.length > 1) {
                    this.remoteLog(msg);
                }
            }
            bufferSize = 0;
            buffer = [];
        };


        function openSocketIfNotOpen() {
            if (!socket) {
                //console.log("Opening connection");
                socket = new WebSocket('ws://127.0.0.1:8080', 'log-protocol');
                socket.onopen = tryRemoteLog;
                socket.onmessage = tryRemoteLog2;
            }
        }

        /**
         * invoked when we receive a message over the websocket,
         * indicating that the last trace chunk in the remoteBuffer
         * has been received
         */
        function tryRemoteLog2() {
            trying = false;
            remoteBuffer.shift();
            if (remoteBuffer.length === 0) {
                if (cb) {
                    cb();
                    cb = undefined;
                }
            }
            tryRemoteLog();
        }

        this.onflush = function (callback) {
            if (remoteBuffer.length === 0) {
                if (callback) {
                    callback();
                }
            } else {
                cb = callback;
                tryRemoteLog();
            }
        };

        function tryRemoteLog() {
            isOpen = true;
            if (!trying && remoteBuffer.length > 0) {
                trying = true;
                socket.send(remoteBuffer[0]);
            }
        }

        this.remoteLog = function (message) {
            if (message.length > Config.MAX_BUF_SIZE) {
                throw new Error("message too big!!!");
            }
            remoteBuffer.push(message);
            openSocketIfNotOpen();
            if (isOpen) {
                tryRemoteLog();
            }
        };

        /**
         * stop recording the trace and flush everything
         */
        this.stopTracing = function () {
            tracingDone = true;
            this.flush();
        };
    }//end of 

       var traceWriter = new sandbox.TraceWriter("trace.log")
        //var logs = [];

        function logEvent(str) {
            traceWriter.logToFile(str+"\n");
	}
            //

	//console.log(colors.green("../../../../"+process.argv[11]));


	//var fileName = './copy/property-details.js';


        var MAX_STRING_LENGTH = 20;
	
	
	function IsJsonFormat(obj){
		try{
			var str = JSON.stringify(obj);
			return (typeof str === 'string');
		}catch(e){
			return false;
		}
	}

	function hasEqualInput(obj,output){
		for (var i in aaa){
			if(underscore.isEqual(aaa[i].client_params,obj) && underscore.isEqual(aaa[i].server_return,output)){
				return aaa[i].id;
			}
		}

		return undefined;

	}
	function hasEqual(obj){
		for (var i in aaa){
			if(underscore.isEqual(aaa[i].server_return,obj)){
				return aaa[i].id; 
			}
		}

		return undefined;
		
	}

        function getValue(v) {
            var type = typeof v;
	   // if(type ==='number' || (type === 'string' && type === parseInt(v))) return parseInt(v);
            if ((type === 'object' || type ==='function') && v!== null) {
                var shadowObj = sandbox.smemory.getShadowObjectOfObject(v);
                return type+"(id="+sandbox.smemory.getIDFromShadowObjectOrFrame(shadowObj)+")";
            } else {
                if (type === 'string' && v.length> MAX_STRING_LENGTH) {
                    v = v.substring(0,MAX_STRING_LENGTH)+"...";
                }
                return JSON.stringify(v);
            }
        }


   
    function MyAnalysis() {
       
        this.invokeFunPre = function (iid, f, base, args, isConstructor, isMethod, functionIid, functionSid) {
            var id = J$.getGlobalIID(iid);
            var location = J$.iidToLocation(id);
            var aaa = /\((.+):(.+):(.+):(.+):(.+)\)/g.exec(location);

            if(aaa !=null && aaa.length == 6 &&(!aaa[1].includes("node_modules"))){
                var code = fs.readFileSync(aaa[1]).toString();

                var pos = lineColumn(code).toIndex(aaa[2], aaa[3]);
                var end =  lineColumn(code).toIndex(aaa[4], aaa[5]);
                var fff = code.slice(pos, end);
                // var type = typeof args[0];
                if((typeof args[0]==='string')&& (args[0].includes("FROM")) ){
                    var sqlText = args[0].replace("?","-1");
                    var ast1 = "", tablename ="TABLE";
                    try{
                     //   console.log("sqlText", uuid, sqlText, location);
                        ast1 = sqlParser.astify(sqlText);
                        tablename = ast1.from[0].table;
                    //	console.log(ast1, "tablename", tablename);
                    } catch (e){}
                    var ast = esprima.parse(fff,{ loc: true, range: true });
                    var entry ={};
                    entry.sqlargvar=[];
                    if(ast.body[0].expression && ast.body[0].expression.arguments[0] && ast.body[0].expression.arguments[0])
                        entry.sqlargvar.push(ast.body[0].expression.arguments[0].name);

                    if(ast.body[0].expression && ast.body[0].expression.arguments[1] && ast.body[0].expression.arguments[1].elements && ast.body[0].expression.arguments[1].elements[0])
                        entry.sqlargvar.push(ast.body[0].expression.arguments[1].elements[0].name);

                    entry.pos = pos;
                    entry.end = end;
                    //entry.sqlvar = ast.body[0].expression.arguments[0].name;
                    entry.text = args[0];
                    entry.file = aaa[1];
                    entry.argf = "";
                    entry.tablename = tablename;
                    entry.uuid = uuid;

                    if(sqlInvocations.length==0)
                        sqlInvocations.push(entry);
                    J$.sqlInvocationsMap[location] ={};
                    J$.sqlInvocationsMap[location].flag=true;
                    J$.sqlInvocationsMap[location].entry=entry;
                    uuid++;
                }
	        }
            return {f: f, base: base, args: args, skip: false};
        };

        // this.invokeFun = function (iid, f, base, args, result, isConstructor, isMethod, functionIid, functionSid) {return {result: result};};
        // this.literal = function (iid, val, hasGetterSetter) {return {result: val};};
        // this.forinObject = function (iid, val) {return {result: val};};
        // this.declare = function (iid, name, val, isArgument, argumentIndex, isCatchParam) {return {result: val};};
        // this.getFieldPre = function (iid, base, offset, isComputed, isOpAssign, isMethodCall) {return {base: base, offset: offset, skip: false};};
        // this.getField = function (iid, base, offset, val, isComputed, isOpAssign, isMethodCall) {return {result: val};};
        // this.putFieldPre = function (iid, base, offset, val, isComputed, isOpAssign) {return {base: base, offset: offset, val: val, skip: false};};
        // this.putField = function (iid, base, offset, val, isComputed, isOpAssign) {return {result: val};};
        // this.read = function (iid, name, val, isGlobal, isScriptLocal) {return {result: val};};

        this.write = function (iid, name, val, lhs, isGlobal, isScriptLocal) {
            var id = J$.getGlobalIID(iid);
            var location = J$.iidToLocation(id);
            var aaa = /\((.+):(.+):(.+):(.+):(.+)\)/g.exec(location);
            var type_val = typeof val;
            if(!aaa[1].includes("node_modules") && J$.toRollback && aaa !=null && aaa.length == 6  && type_val !=='object' && type_val !=='function' && parseInt(val)){
            if(90000<parseInt(val) && parseInt(val) <99999) {
                    // console.log("process.cwd()",process.cwd())
                    if(sqlInvocations.length==0 || (sqlInvocations.length==1 && sqlInvocations.uuid<uuid)){
                        var code = fs.readFileSync(aaa[1]).toString();
                        var escodegen = require('escodegen');
                        var pos = lineColumn(code).toIndex(aaa[2], aaa[3]);
                        var end =  lineColumn(code).toIndex(aaa[4], aaa[5]);
                        var fff = code.slice(pos, end);

                        J$.mashallingLog.entry = {};
                        J$.mashallingLog.entry.filename =aaa[1].replace(process.cwd()+"/",'');
                        J$.mashallingLog.entry.filnenamerange = aaa[1].replace(process.cwd()+"/",'')+":"+pos+":"+end;
                        J$.mashallingLog.entry.range =[pos, end];
                        J$.mashallingLog.entry.value = val-90000;

                        var ast = esprima.parse(code,{ loc: true, range: true });
                        var identifers = [];
                        var entryfact = "";
                        estraverse.traverse(ast, {
                            enter: function (node, parent) {
                                node.parent = parent;
                            if (node.type =="Identifier" && node.range[0]>=pos && node.range[1]<=end){
                                // var findingnode=parent;
                                if(parent.parent && parent.parent.type=="VariableDeclarator" && parent.parent.id.name==name) {
                                    // console.log("EEEE", escodegen.generate(parent.parent), parent.parent.type, parent.parent.id.range);
                                    entryfact= format("fp.fact(ref(BitVecVal(hashVar[\"{0}\"][\"bin\"],var),BitVecVal({1},val)))",[J$.mashallingLog.entry.filename+":"+parent.parent.id.range[0]+":"+parent.parent.id.range[1],polycrc.crc24(JSON.stringify(val-90000))]);
                                    J$.mashallingLog.entry.value_sid =polycrc.crc24(JSON.stringify(val-90000));
                                }
                            }
                        }});

                        J$.mashallingLog.entry.rwfacts = entryfact;
                        console.log(colors.magenta("Entry Point Identifed"+"  WRITE(|"+val+"|)"));
                        // console.log(uuid, "<-ENTRYPOINT:",pos,end, fff,  name,location, "  WRITE(|"+val+"|)",J$.mashallingLog);
                        // entryPointMap[parseInt(val)] = location; //keep latest WRITE
                    }

                   if(!entryPointMap[parseInt(val)]){
                        entryPointMap[parseInt(val)] = location;
                    }//first visit
                // }

                    uuid++;
                        logEvent("<-ENTRYPOINT:", name,"  WRITE(|"+val+"|)", location);
                }else if(entryPointMap[parseInt(val)+9000]==location){
                         return {entry:location};
                         J$.entryCursor = uuid;
                         // console.log(uuid, "@@@@@@@@@            >>> ENTRYPOINT:", name,location,"  WRITE(|", entryPointMap[location],"->",val,"|)");
                }else{
                          //  console.log(colors.grey(uuid, "@@@@@@@@@            >>> ENTRYPOINT:", name,location,"  WRITE(|", entryPointMap[location],"->",val,"|)"));
                }
                //revisit
            	// }else if(getFieldsMap[location] && entryPointMap[location]){
                //         console.log(colors.green(uuid, "@@@<-ENTRYPOINT:", name,location, "  WRITE(|"+val+"|)"));
                // }

            }//entry points


             if(!aaa[1].includes("node_modules")&& aaa !=null && aaa.length == 6  && typeof val =="string" && val == "JSRCIInsourcing"){
                console.log(colors.magenta("@@@@@@@@@@@@@Starting Insourcing!!!"+constraints_solver(J$.mashallingLog)));
                // console.log(colors.green(J$.mashallingLog));
             }
            if(!aaa[1].includes("node_modules")&& aaa !=null && aaa.length == 6  && typeof val =="string" && val == "JSRCIRestore"){
                    //J$.toRollback = true;
                    console.log(colors.magenta("@@@@@@@@@@@@@JSRCIRestore"));

                    try {
                        if (J$.methods.m1 = !undefined) J$.methods.m1.query("SELECT * from recipes", function (error, results, fields) {
                            console.log("######", results);
                        });
                    }catch (e){}
                    for(var key in J$.rollbacks) {
                            //var value = objects[key];
                        try{
                    	console.log("J$.rollbacks."+key+"();");
                        eval("J$.rollbacks."+key+"();");

                        }catch(e){console.error("ERROR	J$.rollbacks."+key+"();");}
                    }

            }
				  //else if(aaa !=null && aaa.length == 6 && type_val ==='object' &&(!aaa[1].includes("node_modules"))){
				//  else if(aaa !=null && aaa.length == 6 && !aaa[1].includes("node_modules") && type_val ==='object' &&(hasEqual(val)!=undefined)){
             else if(!aaa[1].includes("node_modules")&& J$.toRollback && aaa !=null && aaa.length == 6 && type_val ==='object' &&(hasEqual(val)!=undefined)){

                 var code = fs.readFileSync(aaa[1]).toString();

                var pos = lineColumn(code).toIndex(aaa[2], aaa[3]);
                var end =  lineColumn(code).toIndex(aaa[4], aaa[5]);
                var fff = code.slice(pos, end);

                // ;
                var ast = esprima.parse(code,{ loc: true, range: true });
                var identifers = [];
                var newexitfact;

                var text="";
                if(identifers.length==2){
                   text= format("fp.fact(ref2(BitVecVal(hashVar[\"{0}\"][\"bin\"],var),BitVecVal(hashVar[\"{1}\"],prop),BitVecVal({2},val)))",[identifers[0],identifers[1], polycrc.crc24(JSON.stringify(val))]);
                    // var fact = "fp.fact(ref2(BitVecVal(hashVar[\""+identifers+"\"][\"bin\"],var),BitVecVal(hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:546:552"]["bin"],prop), BitVecVal(1999,val)))

                }
                    J$.currentOutput = val;
                    J$.mashallingLog.exit = {};
                    J$.mashallingLog.exit.filename =aaa[1].replace(process.cwd()+"/",'');
                    J$.mashallingLog.exit.filnenamerange = aaa[1].replace(process.cwd()+"/",'')+":"+pos+":"+end;
                    J$.mashallingLog.exit.range =[pos, end];
                    J$.mashallingLog.exit.val=JSON.stringify(val);



                    estraverse.traverse(ast, {
                    enter: function (node, parent) {
                        node.parent = parent;
        // if (node.type == 'FunctionExpression' || node.type == 'FunctionDeclaration')
        //     return estraverse.VisitorOption.Skip;
                    if (node.type =="Identifier" && node.range[0]>=pos && node.range[1]<=end){
                        identifers.push(aaa[1].replace(process.cwd()+"/",'')+":"+node.range[0]+":"+node.range[1]);
                        // if(node.parent)
                        // console.log("identifers.parent.type ", node.parent.parent);
                        if(parent.parent && parent.parent.type=="VariableDeclarator" && parent.parent.id.name==name) {
                            // console.log(escodegen.generate(parent.parent), parent.parent.type, parent.parent.id.range);
                        }


                       if(parent.parent && parent.parent.type=="VariableDeclarator" && parent.parent.id.name==name) {
                        // console.log("OOOOOOEEEE");
                        newexitfact= format("fp.fact(ref(BitVecVal(hashVar[\"{0}\"][\"bin\"],var),BitVecVal({1},val)))",[J$.mashallingLog.exit.filename+":"+parent.parent.id.range[0]+":"+parent.parent.id.range[1],polycrc.crc24(JSON.stringify(val))]);
                        J$.mashallingLog.exit.value_sid =polycrc.crc24(JSON.stringify(val));
                       }
                    }
                }});

                         // J$.mashallingLog.exit.rwfacts=text;
                    J$.mashallingLog.exit.rwfacts = newexitfact;
                 // console.log(text, uuid, "->EXITPOINT:", name, location,fff, lhs, "  WRITE OJB(|", JSON.stringify(val), "|)",typeof val,  hasEqual(val), "ENTRY??   ",J$.mashallingLog);
                 console.log(colors.magenta("Exit Point Identifed"+"  WRITE(|"+JSON.stringify(val)+"|)"));
                //if(IsJsonFormat(val)){

                // console.log(J$.entryCursor, uuid, "->EXITPOINT:", name, location, "  WRITE OJB(|", JSON.stringify(val), "|)",typeof val,  hasEqual(val));
                uuid++;
            /**
                if(!exitPointMap[hasEqual(val)]){

                    exitPointMap[hasEqual(val)] = "->EXITPOINT:", name, location, "  WRITE OJB(|", JSON.stringify(val), "|)",typeof val,  hasEqual(val);
                    console.log(uuid, "->EXITPOINT:", name, location, "  WRITE OJB(|", JSON.stringify(val), "|)",typeof val,  hasEqual(val));
                    uuid++;
                }else if(J$.toRollback){
                // console.log(colors.gray("       ->EXITPOINT:"), colors.red(name), colors.gray(location, "  WRITE OJB(|", JSON.stringify(val), "|)",typeof val,  hasEqual(val)));
                }

             **/
                logEvent("->EXITPOINT:", name, lhs, location, "  WRITE OJB(|", JSON.stringify(val), "|)");
                //}
             }


            return {result: val, test:"abcd"};
        };

        this._return = function (iid, val) {return {result: val};};
        this._throw = function (iid, val) {return {result: val};};
        this._with = function (iid, val) {return {result: val};};

        this.functionEnter = function (iid, f, dis, args) {


            var id = J$.getGlobalIID(iid);
            var location = J$.iidToLocation(id);
            var aaa = /\((.+):(.+):(.+):(.+):(.+)\)/g.exec(location);


        if(aaa !=null && aaa.length == 6 &&(!aaa[1].includes("node_modules"))){
		//if(aaa !=null && aaa.length == 6){

            var code = fs.readFileSync(aaa[1]).toString();
		    var pos = lineColumn(code).toIndex(aaa[2], aaa[3]);
		    var end = lineColumn(code).toIndex(aaa[4], aaa[5]);
		    // var fff = code.slice(lineColumn(code).toIndex(aaa[2], aaa[3]), lineColumn(code).toIndex(aaa[4], aaa[5]));
	       	

		for(var e in sqlInvocations){
			if(args && args[1]  && sqlInvocations[e].pos < pos && sqlInvocations[e].end > end && sqlInvocations[e].text.includes("FROM")) {var JSRCI_var;NUM = NUM+100;

				console.log("!!!!!!!!!!!1		functionEnter() arg	",sqlInvocations[e], sqlInvocations,
				JSON.parse(JSON.stringify(args[1]),"\n" ,sqlInvocations[e]),
				// J$.methods.f689, "J$.sqlInvocationsMap",
				// J$.sqlInvocationsMap,
				"J$$$$$$$$$$",//J$.snapshots[0],//Object.getOwnPropertyNames(J$),
				'\n', sqlInvocations[e].text, sqlInvocations[e].sqlargvar
				//,J$.rollbacks
				);
				/**
				J$.toRollback = true;
				try {
                    if (J$.methods.m1 = !undefined) J$.methods.m1.query("SELECT * from recipes", function (error, results, fields) {
                        console.log("######", results)
                    });
                }catch (e){}
				for(var key in J$.rollbacks) {
    					//var value = objects[key];
					try{
				//	console.log("J$.rollbacks."+key+"();");
					eval("J$.rollbacks."+key+"();");

					}catch(e){console.error("ERROR	J$.rollbacks."+key+"();");}
				}
**/
			//	J$.methods.f689('SELECT * FROM `recipes`','',function (error, results, fields) {console.log("####",results);});
			//	console.log(J$.methods.f689.toString());
				//J$.rollbacks.f137({aaaa:2141241, afsafsaf:1231313123213});
				//J$.rollbacks.f137();
				//aabbba(3333,{aaaa:898989898});

/**        J$.X1(265, J$.F(257, J$.R(225, 'aaa', aaa, 1), 0)(J$.T(233, 99999, 22, false), J$.T(249, {
                degh: J$.T(241, 2, 22, false)
            }, 11, false)));

**/				logEvent(sqlInvocations[e].text);
				logEvent(JSON.stringify(args[1]));
				logEvent(sqlInvocations[e].sqlvar);
				console.log("var result=alasql("+sqlInvocations[e].sqlargvar[0]+");");
				logEvent("var result=alasql("+sqlInvocations[e].sqlargvar[0]+");");
				console.log("");
				try{
					var csvData = parse(JSON.parse(JSON.stringify(args[1])));
					var dataarr = csvData.split("\n");
				for (var i =0; i< dataarr.length; i++){
					if(i==0){
						console.log("alasql(CREATE TABLE "+sqlInvocations[e].tablename+");");
						logEvent("alasql(CREATE TABLE "+sqlInvocations[e].tablename+");");
					}else{
						console.log("alasql(INSERT ("+dataarr[i]+") INTO ("+dataarr[0]+"));");
						logEvent("alasql(INSERT ("+dataarr[i]+") INTO ("+dataarr[0]+"));");
					}
				}
				}catch(e){
					//console.log(e);
				}
				//remove it
				sqlInvocations.splice(e, 1); 
			}
				
		}
		
        	//  console.log("invokeFun", result, "\n", aaa[1]);
	}

                  //  var id = J$.getGlobalIID(iid);
                  //            	  var location = J$.iidToLocation(id);
        	  //var aaa = /\((.+):(.+):(.+):(.+):(.+)\)/g.exec(location);
        	  //console.log("functionEnter", args,"   @@@@@@ " ,location, "\n");
        };

        /**
         * This callback is called when the execution of a function body completes
         *
         * @param {number} iid - Static unique instruction identifier of this callback
         * @param {*} returnVal - The value returned by the function
         * @param {{exception:*} | undefined} wrappedExceptionVal - If this parameter is an object, the function
         * execution has thrown an uncaught exception and the exception is being stored in the <tt>exception</tt>
         * property of the parameter
         * @returns {{returnVal: *, wrappedExceptionVal: *, isBacktrack: boolean}}  If an object is returned, then the
         * actual <tt>returnVal</tt> and <tt>wrappedExceptionVal.exception</tt> are replaced with that from the
         * returned object. If an object is returned and the property <tt>isBacktrack</tt> is set, then the control-flow
         * returns to the beginning of the function body instead of returning to the caller.  The property
         * <tt>isBacktrack</tt> can be set to <tt>true</tt> to repeatedly execute the function body as in MultiSE
         * symbolic execution.
         */
        this.functionExit = function (iid, returnVal, wrappedExceptionVal) {
            return {returnVal: returnVal, wrappedExceptionVal: wrappedExceptionVal, isBacktrack: false};
        };

        /**
         * This callback is called before the execution of a JavaScript file
         *
         * @param {number} iid - Static unique instruction identifier of this callback
         * @param {string} instrumentedFileName - Name of the instrumented script file
         * @param {string} originalFileName - Name of the original script file
         */
        this.scriptEnter = function (iid, instrumentedFileName, originalFileName) {
        };

        /**
         * This callback is called when the execution of a JavaScript file completes
         *
         * @param {number} iid - Static unique instruction identifier of this callback
         * @param {{exception:*} | undefined} wrappedExceptionVal - If this parameter is an object, the script
         * execution has thrown an uncaught exception and the exception is being stored in the <tt>exception</tt>
         * property of the parameter
         * @returns {{wrappedExceptionVal: *, isBacktrack: boolean}} - If an object is returned, then the
         * actual <tt>wrappedExceptionVal.exception</tt> is replaced with that from the
         * returned object. If an object is returned and the property <tt>isBacktrack</tt> is set, then the control-flow
         * returns to the beginning of the script body.  The property
         * <tt>isBacktrack</tt> can be set to <tt>true</tt> to repeatedly execute the script body as in MultiSE
         * symbolic execution.
         */
        this.scriptExit = function (iid, wrappedExceptionVal) {
            return {wrappedExceptionVal: wrappedExceptionVal, isBacktrack: false};
        };

        /**
         * This callback is called before a binary operation. Binary operations include  +, -, *, /, %, &, |, ^,
         * <<, >>, >>>, <, >, <=, >=, ==, !=, ===, !==, instanceof, delete, in.  No callback for <code>delete x</code>
         * because this operation cannot be performed reflectively.
         *
         * @param {number} iid - Static unique instruction identifier of this callback
         * @param {string} op - Operation to be performed
         * @param {*} left - Left operand
         * @param {*} right - Right operand
         * @param {boolean} isOpAssign - True if the binary operation is part of an expression of the form
         * <code>x op= e</code>
         * @param {boolean} isSwitchCaseComparison - True if the binary operation is part of comparing the discriminant
         * with a consequent in a switch statement.
         * @param {boolean} isComputed - True if the operation is of the form <code>delete x[p]</code>, and false
         * otherwise (even if the operation if of the form <code>delete x.p</code>)
         * @returns {{op: string, left: *, right: *, skip: boolean}|undefined} - If an object is returned and the
         * <tt>skip</tt> property is true, then the binary operation is skipped.  Original <tt>op</tt>, <tt>left</tt>,
         * and <tt>right</tt> are replaced with that from the returned object if an object is returned.
         */
        this.binaryPre = function (iid, op, left, right, isOpAssign, isSwitchCaseComparison, isComputed) {
            return {op: op, left: left, right: right, skip: false};
        };

        /**
         * This callback is called after a binary operation. Binary operations include  +, -, *, /, %, &, |, ^,
         * <<, >>, >>>, <, >, <=, >=, ==, !=, ===, !==, instanceof, delete, in.
         *
         * @param {number} iid - Static unique instruction identifier of this callback
         * @param {string} op - Operation to be performed
         * @param {*} left - Left operand
         * @param {*} right - Right operand
         * @param {*} result - The result of the binary operation
         * @param {boolean} isOpAssign - True if the binary operation is part of an expression of the form
         * <code>x op= e</code>
         * @param {boolean} isSwitchCaseComparison - True if the binary operation is part of comparing the discriminant
         * with a consequent in a switch statement.
         * @param {boolean} isComputed - True if the operation is of the form <code>delete x[p]</code>, and false
         * otherwise (even if the operation if of the form <code>delete x.p</code>)
         * @returns {{result: *}|undefined} - If an object is returned, the result of the binary operation is
         * replaced with the value stored in the <tt>result</tt> property of the object.
         */
        this.binary = function (iid, op, left, right, result, isOpAssign, isSwitchCaseComparison, isComputed) {
            return {result: result};
        };

        /**
         * This callback is called before a unary operation. Unary operations include  +, -, ~, !, typeof, void.
         *
         * @param {number} iid - Static unique instruction identifier of this callback
         * @param {string} op - Operation to be performed
         * @param {*} left - Left operand
         * @returns {{op: *, left: *, skip: boolean} | undefined} If an object is returned and the
         * <tt>skip</tt> property is true, then the unary operation is skipped.  Original <tt>op</tt> and <tt>left</tt>
         * are replaced with that from the returned object if an object is returned.
         */
        this.unaryPre = function (iid, op, left) {
            return {op: op, left: left, skip: false};
        };

        /**
         * This callback is called after a unary operation. Unary operations include  +, -, ~, !, typeof, void.
         *
         * @param {number} iid - Static unique instruction identifier of this callback
         * @param {string} op - Operation to be performed
         * @param {*} left - Left operand
         * @param {*} result - The result of the unary operation
         * @returns {{result: *}|undefined} - If an object is returned, the result of the unary operation is
         * replaced with the value stored in the <tt>result</tt> property of the object.
         *
         */
        this.unary = function (iid, op, left, result) {
            return {result: result};
        };

        /**
         * This callback is called after a condition check before branching. Branching can happen in various statements
         * including if-then-else, switch-case, while, for, ||, &&, ?:.
         *
         * @param {number} iid - Static unique instruction identifier of this callback
         * @param {*} result - The value of the conditional expression
         * @returns {{result: *}|undefined} - If an object is returned, the result of the conditional expression is
         * replaced with the value stored in the <tt>result</tt> property of the object.
         */
        this.conditional = function (iid, result) {
            return {result: result};
        };

        /**
         * This callback is called before a string passed as an argument to eval or Function is instrumented.
         *
         * @param {number} iid - Static unique instruction identifier of this callback
         * @param {*} code - Code that is going to get instrumented
         * @param {boolean} isDirect - true if this is a direct call to eval
         * @returns {{code: *, skip: boolean}} - If an object is returned and the
         * <tt>skip</tt> property is true, then the instrumentation of <tt>code</tt> is skipped.
         * Original <tt>code</tt> is replaced with that from the returned object if an object is returned.
         */
        this.instrumentCodePre = function (iid, code, isDirect) {
		
            return {code: code, skip: false};
        };

        /**
         * This callback is called after a string passed as an argument to eval or Function is 
	 console.log("instrumentCodePre");instrumented.
         *
         * @param {number} iid - Static unique instruction identifier of this callback
         * @param {*} newCode - Instrumented code
         * @param {Object} newAst - The AST of the instrumented code
         * @param {boolean} isDirect - true if this is a direct call to eval
         * @returns {{result: *}|undefined} - If an object is returned, the instrumented code is
         * replaced with the value stored in the <tt>result</tt> property of the object.
         */
        this.instrumentCode = function (iid, newCode, newAst, isDirect) {
		//console.log("instrumentCodePre",newCode);
            return {result: newCode};
        };

        /**
         * This callback is called when an expression is evaluated and its value is discarded.  For example, this
         * callback is called when an expression statement completes its execution.
         *
         * @param {number} iid - Static unique instruction identifier of this callback
         * @returns {undefined} - Any return value is ignored
         */
        this.endExpression = function (iid) {
        };

        /**
         * This callback is called when an execution terminates in node.js.  In a browser environment, the callback is
         * called if ChainedAnalyses.js or ChainedAnalysesNoCheck.js is used and Alt-Shift-T is pressed.
         *
         * @returns {undefined} - Any return value is ignored
         */
        this.endExecution = function () {
	traceWriter.stopTracing();
	console.log("endExecution");
        };

        /**
         * This callback is called only when instrumented with J$.Config.ENABLE_SAMPLING = true
         * This callback is called before the body of a function, method, or constructor is executed
         * if returns true, instrumented function body is executed, else uninstrumented function body is executed
         * @param {number} iid - Static unique instruction identifier of this callback
         * @param {function} f - The function whose body is being executed
         * @param {number} functionIid - The iid (i.e. the unique instruction identifier) where the function was created
         * @param {number} functionSid - The sid (i.e. the unique script identifier) where the function was created
         * {@link MyAnalysis#functionEnter} when the function <tt>f</tt> is executed.  The <tt>functionIid</tt> can be
         * treated as the static identifier of the function <tt>f</tt>.  Note that a given function code block can
         * create several function objects, but each such object has a common <tt>functionIid</tt>, which is the iid
         * that is passed to {@link MyAnalysis#functionEnter} when the function executes.
         * @returns {boolean} - If true is returned the instrumented function body is executed, otherwise the
         * uninstrumented function body is executed.
         */
        this.runInstrumentedFunctionBody = function (iid, f, functionIid, functionSid) {
            return false;
        };

        /**
         * onReady is useful if your analysis is running on node.js (i.e., via the direct.js or jalangi.js commands)
         * and needs to complete some asynchronous initialization before the instrumented program starts.  In such a
         * case, once the initialization is complete, invoke the cb function to start execution of the instrumented
         * program.
         *
         * Note that this callback is not useful in the browser, as Jalangi has no control over when the
         * instrumented program runs there.
         * @param cb
         */
        this.onReady = function (cb) {
            console.log("this.onReady");
            cb();
            J$.toRollback = true;
        };
    }

    sandbox.analysis = new MyAnalysis();
})(J$);



