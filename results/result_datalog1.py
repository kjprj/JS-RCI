# -*- coding: utf-8 -*-
'''
    ported for z3 python2.7 from JS-dep;  with modified for undetected stmts
'''
from z3 import *
from termcolor import colored
import re
import os
import string
import random
import shutil
import urllib
import operator
import os

from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit import ast
parser = Parser()

def get_key(bin):
    for key, value in hashVar.items():
         if bin == value["bin"]:
             return key



def adaptinput(text, entry):
    # print "adaptinput   ", text, "    ",entry
    tree = parser.parse(text)
    for node in nodevisitor.visit(tree):
        #text = "var BROKERS = require(\'./mock-brokers\').data;"
        #-> var output = text;
        if isinstance(node, ast.VarDecl) and node.identifier.value==entry:
            return "\tvar "+node.identifier.value+"=input;"
        elif isinstance(node, ast.VarDecl) and node.identifier.value!=exit:
            return "\tvar "+node.identifier.value+"=input;"
    return ""

def adaptoutput(text, exit):
    tree = parser.parse(text)
    for node in nodevisitor.visit(tree):
        #text = "var BROKERS = require(\'./mock-brokers\').data;"
        #-> var output = text;
        if isinstance(node, ast.VarDecl) and node.identifier.value==exit:
            return "\tvar output="+exit+";"
        elif isinstance(node, ast.VarDecl) and node.identifier.value!=exit:
            return "\tvar output="+node.identifier.value+";"
    return ""


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


#z3 Fixedpoint Engine
fp = Fixedpoint()
fp.set(engine='datalog')

lineNum     = BitVecSort(24)
num         = BitVecSort(24)
var         = BitVecSort(24)
val         = BitVecSort(24)
mval        = BitVecSort(24)
obj         = BitVecSort(24)
prop        = BitVecSort(24)
jsfiles     = BitVecSort(24)
value       = BitVecSort(24)
evType      = BitVecSort(24)
uid         = BitVecSort(24)

Assign = Function('Assign', var, var, lineNum,  BoolSort()) # a = b # Assign (variable variable line#)
Load = Function('Load', var, prop, var, lineNum,  BoolSort())#; a.b = c #(declare-rel Load (var prop var lineNum))

#store,  a = b.c;
Store = Function('Store', var, var, prop, lineNum,  BoolSort()) #(declare-rel Store (var var prop lineNum))
Read1 = Function('Read1', var, lineNum,  BoolSort()) #(declare-rel Read1 (var lineNum))
Read2 = Function('Read2', var, prop, lineNum,  BoolSort()) #(declare-rel Read2 (var prop lineNum))
Write1 = Function('Write1', var, lineNum,  BoolSort()) #(declare-rel Write1 (var lineNum))
Write2 = Function('Write2', var, prop, lineNum,  BoolSort())#(declare-rel Write2 (var prop lineNum))
PtsTo = Function('PtsTo', var, obj, BoolSort()) #(declare-rel PtsTo (var obj))
HeapPtsTo = Function('HeapPtsTo', var, prop, obj, BoolSort())#(declare-rel HeapPtsTo (var prop obj))

#; Stmt (line# object)
#(declare-rel Stmt (lineNum obj))

fp.register_relation(Assign)
fp.register_relation(Store)
fp.register_relation(Load)
fp.register_relation(PtsTo)
fp.register_relation(HeapPtsTo)
fp.register_relation(Read1)
fp.register_relation(Read2)
fp.register_relation(Write1)
fp.register_relation(Write2)

Stmt        = Function('Stmt', lineNum, obj, BoolSort()) #(declare-rel Stmt (lineNum obj))
Formal      = Function('Formal', obj, num, var, BoolSort())#(declare-rel Formal (obj num var))
Actual      = Function('Actual', lineNum, num, var, BoolSort())#(declare-rel Actual (lineNum num var))
MethodRet   = Function('MethodRet', obj, var, BoolSort())#(declare-rel MethodRet(obj var))
CallRet     = Function('CallRet', lineNum, var, BoolSort())#(declare-rel CallRet (lineNum var))
Calls       = Function('Calls', obj, lineNum, BoolSort())#(declare-rel Calls (obj lineNum))

FuncDecl    = Function('FuncDecl',var, obj, lineNum, BoolSort())#(declare-rel FuncDecl (var obj lineNum))
Heap        = Function('Heap',var, obj, BoolSort())#(declare-rel Heap (var obj))
datadep     = Function('datadep',lineNum, lineNum, BoolSort()) #; data-dep (line# line#) #(declare-rel data-dep (lineNum lineNum))
controldep  = Function('controldep',lineNum, lineNum, BoolSort()) #; con-dep (line# line#) #(declare-rel control-dep (lineNum lineNum))
stmtdep     = Function('stmtdep',lineNum, lineNum, BoolSort()) #; stmt-dep (line# line#)#(declare-rel stmt-dep (lineNum lineNum))
calldep     = Function('calldep',var, var, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))

ref         = Function('ref',var, val, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))
ref2         = Function('ref',var, prop, val, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))

unMarshal   = Function('unMarshal',lineNum, var, val, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))
Marshal     = Function('Marshal',lineNum, var, val, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))

ExecutedStmts    = Function('ExecutedStmts',lineNum, uid, mval, val, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))
ExecutedUid    = Function('ExecutedUid',lineNum, uid, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))

ExecutedUMarshal    = Function('ExecutedUMarshal',lineNum, uid, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))


fp.register_relation(Stmt)
fp.register_relation(Formal)
fp.register_relation(Actual)
fp.register_relation(MethodRet)
fp.register_relation(CallRet)
fp.register_relation(Calls)
fp.register_relation(FuncDecl)
fp.register_relation(Heap)
fp.register_relation(datadep)
fp.register_relation(controldep)
fp.register_relation(stmtdep)
fp.register_relation(calldep)
fp.register_relation(ref)
fp.register_relation(ref2)
fp.register_relation(unMarshal)
fp.register_relation(Marshal)
fp.register_relation(ExecutedStmts)
fp.register_relation(ExecutedUid)
o1 = Const('o1',obj)
o2 = Const('o2',obj)
o3 = Const('o3',obj)
o4 = Const('o4',obj)

v1 = Const('v1',var)
v2 = Const('v2',var)
v3 = Const('v3',var)
v4 = Const('v4',var)
v5 = Const('v5',var)
v6 = Const('v6',var)

val1 = Const('val1',val)
val2 = Const('val2',val)

line1 = Const('line1',lineNum)
line2 = Const('line2',lineNum)
line3 = Const('line3',lineNum)
line4 = Const('line4',lineNum)

i1 = Const('i1',num)
f1 = Const('f1',prop)
f2 = Const('f2',prop)


uid1 = Const('uid1',uid)

#pointsTo rule
#(rule (=> (Heap v1 o1) (PtsTo v1 o1)))
#(rule (=> (and (Heap B A)) (PtsTo B A)))
fp.register_relation(PtsTo,Heap)
fp.declare_var(v1,o1)
fp.rule(PtsTo(v1,o1),Heap(v1,o1))

fp.register_relation(PtsTo,FuncDecl)
fp.declare_var(v1,o1,line1)
fp.rule(PtsTo(v1,o1),FuncDecl(v1,o1,line1))

fp.register_relation(PtsTo,PtsTo,Assign)
fp.declare_var(v1,line1,v2)
fp.rule(PtsTo(v2,o1),[PtsTo(v1,o1),Assign(v2,v1, line1)])

#fp.register_relation(PtsTo,Assign,Assign)
#fp.declare_var(v1,line1,v2)
#fp.rule(PtsTo(v2,o1),[PtsTo(v1,o1),Assign(v2,v1, line1)])

# Stmt rule
fp.register_relation(Stmt,calldep,Stmt)
fp.declare_var(line1,o2,o1)
fp.rule(Stmt(line1,o1),[Stmt(line1,o2),calldep(o1,o2)])

# (rule (=> (and (PtsTo A B) (Actual C #x000000 A)) (Calls B C)))
fp.register_relation(Calls,Actual,PtsTo)
fp.declare_var(line1,o1,v1)
fp.rule(Calls(o1,line1),[PtsTo(v1,o1),Actual(line1,0,v1)])
#fp.rule(Calls(o1,line1),[Actual(line1,0,v1),PtsTo(v1,o1)])

fp.register_relation(Calls,Formal,Actual)
fp.declare_var(line1,o1,v1,i1,v2)
fp.rule(Assign(v1,v2,line1),[Calls(o1,line1),Formal(v1,i1, o1),Actual(line1,i1, v2)])

fp.register_relation(Assign,Calls,Formal,Actual)
fp.declare_var(v1,v2,line1,o1,i1,v2)
fp.rule(Assign(v1,v2,line1),[Calls(o1,line1),Formal(v1,i1, o1),Actual(line1,i1, v2)])


fp.register_relation(Read1,Calls,Formal,Actual)
fp.declare_var(v1,v2,line1,o1,i1,v2)
#fp.rule(Read1(v2,line1),[Calls(o1,line1),Formal(v1,i1, o1),Actual(line1,i1, v2)])
fp.rule(Read1(v2,line1),[Actual(line1,0, v1), Actual(line1,i1, v2)])

fp.register_relation(Write1,Calls,Formal,Actual)
fp.declare_var(v1,v2,line1,o1,i1,v2)
fp.rule(Write1(v1,line1),[Calls(o1,line1),Formal(v1,i1, o1),Actual(line1,i1, v2)])


fp.register_relation(Read1,Calls,Actual)
fp.declare_var(v1,v2,line1,o1,i1,v2)
fp.rule(Read1(v2,line1),[Calls(o1,line1),Actual(line1,i1, v2)])


fp.register_relation(Write1,Calls,Actual)
fp.declare_var(v1,v2,line1,o1,i1,v2)
fp.rule(Write1(v1,line1),[Calls(o1,line1),Actual(line1,i1, v2)])


fp.register_relation(Assign,Calls,MethodRet,CallRet)
fp.declare_var(v1,v2,line1,o1,i1,v2)
fp.rule(Assign(v2,v1,line1),[Calls(o1,line1),MethodRet(o1,v1),CallRet(line1,v2)])


fp.register_relation(Read1,Calls,MethodRet,CallRet)
fp.declare_var(v1,v2,line1,o1,v2)
fp.rule(Read1(v1,line1),[Calls(o1,line1),MethodRet(o1,v1),CallRet(line1,v2)])


fp.register_relation(Write1,Calls,MethodRet,CallRet)
fp.declare_var(v1,v2,line1,o1,v2)
fp.rule(Write1(v1,line1),[Calls(o1,line1),MethodRet(o1,v1),CallRet(line1,v2)])


fp.register_relation(datadep,Write1,Read1)
fp.declare_var(line1,line2,v1)
fp.rule(datadep(line1,line2),[Write1(v1,line1),Read1(v1,line2)])


fp.register_relation(unMarshal,Write1,ref)
fp.declare_var(line1,v1,val1)
fp.rule(unMarshal(line1, v1, val1),[Write1(v1,line1),ref(v1, val1)])




# fp.query(datadep(BitVecVal(1, lineNum),exitLine))

#Executed    = Function('Executed',lineNum, uid, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))


fp.register_relation(Marshal,Write1,ref)
fp.declare_var(line1,v1,val1,f1)
fp.rule(Marshal(line1, v1, val1),[Write1(v1,line1),ref(v1, val1)])
# fp.rule(Marshal(line1, v1, val1),[Read2(v1,f1,line1),ref2(v1, f1, val1)])

# fp.register_relation(Marshal,Read1,ref, Read2, ref2)
# fp.declare_var(line1,v1,val1,f1)
# fp.rule(Marshal(line1, v1, val1),[Read1(v1,line1),ref(v1, val1)])
# fp.rule(Marshal(line1, v1, val1),[Read2(v1,f1,line1),ref2(v1, f1, val1)])

# fp.fact(Read2(BitVecVal(2,prop),BitVecVal(17,var),BitVecVal(16736239,lineNum)))
# fp.fact(ref2(BitVecVal(17,var),BitVecVal(2,prop), BitVecVal(1999,val)))

fp.register_relation(ExecutedStmts,datadep,unMarshal, Marshal)
fp.declare_var(line1,line2,line3, v1,val1,uid1, val2, v2)
# fp.query(datadep(BitVecVal(1, lineNum),exitLine), Not(datadep(BitVecVal(3, lineNum),exitLine)))

fp.rule(ExecutedStmts(line1, uid1, val1, val2),
        [
             datadep(line1,line2), Marshal(line2, v1, val2),
             Not(datadep(line1,line3)), unMarshal(line3, v2, val1)
        ])

# fp.rule(Executed(line1, uid1, val1, val2),
#         [
#              datadep(line2,line1), unMarshal(line2, v1, val1),
#              Not(datadep(line3,line1)), unMarshal(line3, v2, val2)
#         ])


# fp.query(
#              datadep(line1,line2), Marshal(line2, v1, 1999),
#              Not(datadep(line1,line3)), unMarshal(line3, v2, 1888)
#         )

fp.register_relation(ExecutedUid,datadep,unMarshal, Marshal)
fp.declare_var(line1,line2,line3, v1,val1,uid1, val2, v2)
fp.rule(ExecutedUid(line1, uid1),
        [
             datadep(line2,line1), unMarshal(line2, v1, val1),
             Not(datadep(line3,line1)), Marshal(line3, v2, val2)
        ])


fp.register_relation(datadep,Load,Read2)
fp.declare_var(line1,line2,v1,v2,o1,f1)
fp.rule(datadep(line1,line2),[Load(v1,f1,v2,line1),Read2(o1,v1,line2)])

fp.register_relation(datadep,Write1,Read2)
fp.declare_var(line1,line2,v1,f1)
fp.rule(datadep(line1,line2),[Write1(v1,line1),Read2(v1,f1,line2)])


fp.register_relation(datadep,Assign,Read2)
fp.declare_var(line1,line2,v1,o1,o2)
fp.rule(datadep(line1,line2),[Assign(v1,o1,line1),Read2(o2,v1,line2)])


fp.register_relation(datadep,Load,Read2)
fp.declare_var(line1,line2,v1,v2,f1,f2)
fp.rule(datadep(line1,line2),[Load(v1,f1,v2,line1),Read2(v1,f2,line2)])


fp.register_relation(datadep,Write2,Read1,PtsTo)
fp.declare_var(line1,line2,v1,f1,o1,v2)
fp.rule(datadep(line1,line2),[Write2(v1,f1,line1),Read1(v1,line1),PtsTo(v1,o1),PtsTo(v2,o1)])

fp.register_relation(datadep,Write2,Read2)
fp.declare_var(line1,line2,v1,f1,o1,v2)
fp.rule(datadep(line1,line2),[Write2(v1,f1,line1),Read2(v1,f1,line2)])


fp.register_relation(datadep,Write1,Write1)
fp.declare_var(line1,line2,o1)
fp.rule(datadep(line1,line2),[Write1(o1,line1),Write1(o1,line2)])
'''
    fp.rule(datadep(line1,line2),[Write2(v1,f1,line1),Read2(v1,f1,line2)])
    fp.rule(datadep(line1,line2),[Write2(v1,f1,line1),Read2(v1,f1,line2),PtsTo(v1,o1),PtsTo(v2,o1)])
    fp.rule(datadep(line1,line3),[datadep(line1,line2),datadep(line2,line3)])
    '''

fp.register_relation(controldep,stmtdep)
fp.declare_var(line1,line2)
fp.rule(stmtdep(line1,line2),controldep(line1,line2))

fp.register_relation(stmtdep,datadep)
fp.declare_var(line1,line2)
fp.rule(datadep(line1,line2),stmtdep(line1,line2))

fp.register_relation(controldep,Actual,FuncDecl)
fp.declare_var(v1,o1,line1,line2)
fp.rule(controldep(line1,line2),[Actual(line1,BitVecVal(0,num), v1), FuncDecl(v1,o1,line2)])

fp.register_relation(controldep,controldep)
fp.declare_var(line1,line2,line3)
fp.rule(controldep(line1,line3),[controldep(line1,line2),controldep(line2,line3)])


fp.register_relation(controldep,datadep)
fp.declare_var(line1,line2)
fp.rule(controldep(line1,line2),datadep(line1,line2))

# fp.register_relation(datadep,datadep)
# fp.declare_var(line1,line2)
# fp.rule(datadep(line1,line2),datadep(line2,line1))



# fp.register_relation(controldep,stmtdep)
# fp.declare_var(line1,line2)
# fp.rule(stmtdep(line1,line2),controldep(line1,line2))

# fp.register_relation(stmtdep,datadep)
# fp.declare_var(line1,line2)
# fp.rule(datadep(line1,line2),stmtdep(line1,line2))

fp.register_relation(datadep,datadep)
fp.declare_var(line1,line2,line3)
fp.rule(datadep(line1,line3),[datadep(line1,line2),datadep(line2,line3)])

code={};
hashVar={};
requires={};
oline={};
globals={};
lines={};
ranges={};

#VariableDecl: var knex = require('../db/knex');
code[1000]="var knex = require('../db/knex');"
fp.fact(Write1(BitVecVal(1001,var),BitVecVal(1000,lineNum)))
fp.fact(Write1(BitVecVal(1001,var),BitVecVal(1000,lineNum)))
fp.fact(Heap(BitVecVal(1002,var),BitVecVal(1004,obj)))
fp.fact(Assign(BitVecVal(1001,var),BitVecVal(1005,obj),BitVecVal(1000,lineNum)))
#VariableDecl: var tmpv5 = '/:id';
code[1006]="var tmpv5 = '/:id';"
fp.fact(Write1(BitVecVal(1007,var),BitVecVal(1006,lineNum)))
fp.fact(Heap(BitVecVal(1008,var),BitVecVal(1010,obj)))
fp.fact(Assign(BitVecVal(1007,var),BitVecVal(1011,obj),BitVecVal(1006,lineNum)))
#CallExpression: router.get(tmpv5, function(req, res) {\nvar tmpv00 = req.params;\nvar tmpv01 = tmpv00.id;\nvar tmpv3 = \"select * from donuts where id =\" + tmpv01;\nknex.raw(tmpv3).then(function(donuts){\n    var tmpv4 = donuts;\n    res.send(tmpv4);\n  });\n});
code[1012]="router.get(tmpv5, function(req, res) {\nvar tmpv00 = req.params;\nvar tmpv01 = tmpv00.id;\nvar tmpv3 = \"select * from donuts where id =\" + tmpv01;\nknex.raw(tmpv3).then(function(donuts){\n    var tmpv4 = donuts;\n    res.send(tmpv4);\n  });\n});"
fp.fact(Actual(BitVecVal(1012,lineNum), BitVecVal(0,num), BitVecVal(1013,var)))
fp.fact(Heap(BitVecVal(1007,var),BitVecVal(1017,obj)))
fp.fact(Actual(BitVecVal(1012,lineNum), BitVecVal(1,num), BitVecVal(1007,var)))
#VariableDecl: var tmpv00 = req.params;
code[1018]="var tmpv00 = req.params;"
fp.fact(Write1(BitVecVal(1019,var),BitVecVal(1018,lineNum)))
fp.fact(Read2(BitVecVal(1020,var), BitVecVal(1022,prop), BitVecVal(1018,lineNum)))
fp.fact(Load(BitVecVal(1019,var),BitVecVal(1020,var), BitVecVal(1021,prop),BitVecVal(1018,lineNum)))
#VariableDecl: var tmpv01 = tmpv00.id;
code[1023]="var tmpv01 = tmpv00.id;"
fp.fact(Write1(BitVecVal(1024,var),BitVecVal(1023,lineNum)))
fp.fact(Read2(BitVecVal(1019,var), BitVecVal(1026,prop), BitVecVal(1023,lineNum)))
fp.fact(Load(BitVecVal(1024,var),BitVecVal(1019,var), BitVecVal(1025,prop),BitVecVal(1023,lineNum)))
#VariableDecl: var tmpv3 = \"select * from donuts where id =\" + tmpv01;
code[1027]="var tmpv3 = \"select * from donuts where id =\" + tmpv01;"
fp.fact(Write1(BitVecVal(1028,var),BitVecVal(1027,lineNum)))
fp.fact(Write1(BitVecVal(1028,var),BitVecVal(1027,lineNum)))
fp.fact(Heap(BitVecVal(1029,var),BitVecVal(1031,obj)))
fp.fact(Assign(BitVecVal(1028,var),BitVecVal(1032,obj),BitVecVal(1027,lineNum)))
fp.fact(Write1(BitVecVal(1028,var),BitVecVal(1027,lineNum)))
fp.fact(Read1(BitVecVal(1033,var),BitVecVal(1027,lineNum)))
fp.fact(Assign(BitVecVal(1028,var),BitVecVal(1024,obj),BitVecVal(1027,lineNum)))
#CallExpression: knex.raw(tmpv3).then(function(donuts){\n    var tmpv4 = donuts;\n    res.send(tmpv4);\n  });
code[1033]="knex.raw(tmpv3).then(function(donuts){\n    var tmpv4 = donuts;\n    res.send(tmpv4);\n  });"
#transform sql
fp.fact(Actual(BitVecVal(1033,lineNum), BitVecVal(0,num), BitVecVal(100100,var)))
code[1033]="var donuts = alasql(tmpppp);"
fp.fact(Heap(BitVecVal(1028,var),BitVecVal(1037,obj)))
fp.fact(Actual(BitVecVal(1033,lineNum), BitVecVal(1,num), BitVecVal(1028,var)))
#VariableDecl: var tmpv4 = donuts;
code[1038]="var tmpv4 = donuts;"
fp.fact(Write1(BitVecVal(1039,var),BitVecVal(1038,lineNum)))
fp.fact(Read1(BitVecVal(1040,var),BitVecVal(1038,lineNum)))
fp.fact(Assign(BitVecVal(1039,var),BitVecVal(1040,obj),BitVecVal(1038,lineNum)))
#CallExpression: res.send(tmpv4);
code[1041]="res.send(tmpv4);"
fp.fact(Actual(BitVecVal(1041,lineNum), BitVecVal(0,num), BitVecVal(1042,var)))
fp.fact(Heap(BitVecVal(1039,var),BitVecVal(1046,obj)))
fp.fact(Actual(BitVecVal(1041,lineNum), BitVecVal(1,num), BitVecVal(1039,var)))







fp.fact(controldep(BitVecVal(1018,lineNum),BitVecVal(1023,lineNum)))

fp.fact(controldep(BitVecVal(1023,lineNum),BitVecVal(1027,lineNum)))

fp.fact(controldep(BitVecVal(1027,lineNum),BitVecVal(1033,lineNum)))

fp.fact(controldep(BitVecVal(1033,lineNum),BitVecVal(1038,lineNum)))

fp.fact(controldep(BitVecVal(1038,lineNum),BitVecVal(1041,lineNum)))

hashVar["donutsRoutes.js:299:332"]={"bin":1000, "name":"var knex = require('../db/knex');"};
hashVar["donutsRoutes.js:303:307"]={"bin":1001, "name":"knex"};
hashVar["donutsRoutes.js:572:591"]={"bin":1006, "name":"var tmpv5 = '/:id';"};
hashVar["donutsRoutes.js:576:581"]={"bin":1007, "name":"tmpv5"};
hashVar["donutsRoutes.js:592:829"]={"bin":1012, "name":"router.get(tmpv5, function(req, res) {\nvar tmpv00 = req.params;\nvar tmpv01 = tmpv00.id;\nvar tmpv3 = \"select * from donuts where id =\" + tmpv01;\nknex.raw(tmpv3).then(function(donuts){\n    var tmpv4 = donuts;\n    res.send(tmpv4);\n  });\n});"};
hashVar["donutsRoutes.js:592:598"]={"bin":1013, "name":"router"};
hashVar["donutsRoutes.js:603:608"]={"bin":1007, "name":"tmpv5"};
hashVar["2tempHash"]={"bin":1017, "name":"2tempHash"};
hashVar["donutsRoutes.js:631:655"]={"bin":1018, "name":"var tmpv00 = req.params;"};
hashVar["donutsRoutes.js:635:641"]={"bin":1019, "name":"tmpv00"};
hashVar["donutsRoutes.js:644:647"]={"bin":1020, "name":"req"};
hashVar["donutsRoutes.js:644:654"]={"bin":1021, "name":"req.params"};
hashVar["donutsRoutes.js:648:654"]={"bin":1022, "name":"params"};
hashVar["donutsRoutes.js:656:679"]={"bin":1023, "name":"var tmpv01 = tmpv00.id;"};
hashVar["donutsRoutes.js:660:666"]={"bin":1024, "name":"tmpv01"};
hashVar["donutsRoutes.js:669:675"]={"bin":1019, "name":"tmpv00"};
hashVar["donutsRoutes.js:669:678"]={"bin":1025, "name":"tmpv00.id"};
hashVar["donutsRoutes.js:676:678"]={"bin":1026, "name":"id"};
hashVar["donutsRoutes.js:680:735"]={"bin":1027, "name":"var tmpv3 = \"select * from donuts where id =\" + tmpv01;"};
hashVar["donutsRoutes.js:684:689"]={"bin":1028, "name":"tmpv3"};
hashVar["donutsRoutes.js:728:734"]={"bin":1024, "name":"tmpv01"};
hashVar["donutsRoutes.js:736:825"]={"bin":1033, "name":"knex.raw(tmpv3).then(function(donuts){\n    var tmpv4 = donuts;\n    res.send(tmpv4);\n  });"};
hashVar["donutsRoutes.js:736:740"]={"bin":1001, "name":"knex"};
hashVar["donutsRoutes.js:745:750"]={"bin":1028, "name":"tmpv3"};
hashVar["4tempHash"]={"bin":1037, "name":"4tempHash"};
hashVar["donutsRoutes.js:779:798"]={"bin":1038, "name":"var tmpv4 = donuts;"};
hashVar["donutsRoutes.js:783:788"]={"bin":1039, "name":"tmpv4"};
hashVar["donutsRoutes.js:791:797"]={"bin":1040, "name":"donuts"};
hashVar["donutsRoutes.js:803:819"]={"bin":1041, "name":"res.send(tmpv4);"};
hashVar["donutsRoutes.js:803:806"]={"bin":1042, "name":"res"};
hashVar["donutsRoutes.js:812:817"]={"bin":1039, "name":"tmpv4"};
hashVar["5tempHash"]={"bin":1046, "name":"5tempHash"};


fp.query(PtsTo)
v_ex = fp.get_answer()
print colored( "PtsTo***********",'blue'), v_ex


fp.query(Actual)
v_ex = fp.get_answer()
print colored( "Actual***********",'red'), v_ex

fp.query(Calls)
v_ex = fp.get_answer()
print colored( "Calls***********",'green'), v_ex

boundToExtractFunction = 1041;
fp.fact(ref(BitVecVal(1024,var),BitVecVal(3062344,val)))
fp.fact(ref(BitVecVal(1039,var),BitVecVal(2348502,val)))

exitLine = Const('exit', lineNum)
fp.declare_var(exitLine)

fp.query(unMarshal(line2, v1, 3062344))
v_ex = fp.get_answer()
unmarshal_stmt = v_ex.arg(1).arg(1).as_long()
unmarshal_stmt_start = get_key(unmarshal_stmt).split(":")[1]
print colored("*********** Constraint Solving Started::::",'magenta')
print colored( "unMarshal***********",'blue'), unmarshal_stmt, unmarshal_stmt_start
#
#
fp.query(Marshal(line2, v1, 2348502))
v_ex = fp.get_answer()
# print "Marshal***********  ", colored(v_ex,'blue'), v_ex


# fp.fact(Load(BitVecVal(27,var),BitVecVal(2,prop), BitVecVal(17,var),BitVecVal(16736239,lineNum)))
# fp.fact(ref2(BitVecVal(17,var),BitVecVal(2,prop), BitVecVal(1999,val)))

marshal_stmt = v_ex.arg(1).arg(1).as_long()
loadedVar = v_ex.arg(0).arg(1).as_long()
marshal_stmt_start = get_key(marshal_stmt).split(":")[1]
print colored("Marshal***********  ",'blue') , marshal_stmt, marshal_stmt_start
print "LoadedVar??  ", loadedVar
# fp.fact(Load(BitVecVal(1028,var),BitVecVal(1001,var), BitVecVal(1020,prop),BitVecVal(1027,lineNum)))


fp.query(datadep(exitLine,unmarshal_stmt))
v_ex = fp.get_answer()
# print "@@@@@@@@@@@@***********  ", v_ex


fp.query(datadep(exitLine,marshal_stmt))
v_ex = fp.get_answer()
# print "@@@@@@@@@@@@***********  ", v_ex

# fp.query(Load)
# v_ex = fp.get_answer()
# print "######################LoadOrAssignVar", v_ex

fp.query(ExecutedStmts(exitLine, 12313, 3062344, 2348502))
v_ex = fp.get_answer()
print colored("ExecutedStmts***********  ",'blue')
print v_ex
uid = "abcDe"

jscode="//JS-RCI generated\n"

extract_ftn={};
extract_globals={};
extract_others={};

for x in range(0, v_ex.num_args()):
    myposition = get_key(v_ex.arg(x).arg(1).as_long()).split(":")[1];
    if myposition<unmarshal_stmt_start or myposition>marshal_stmt_start:
        extract_globals[myposition]= v_ex.arg(x).arg(1).as_long();
    else:
        extract_ftn[myposition]=v_ex.arg(x).arg(1).as_long();

# print "extract_ftn", extract_ftn
# print "extract_others", extract_others

print colored("Extracting Functions***********  ",'magenta')

for key in sorted(extract_globals.keys()):
    if extract_globals[key] > boundToExtractFunction:
        # print colored(code[extract_globals[key]], 'cyan')
        otherfilename = get_key(extract_globals[key]).split(":")[0]
        # print otherfilename
        if otherfilename in extract_others:
            extract_others[otherfilename].append(code[extract_globals[key]]);
        else:
            extract_others[otherfilename] = [];
            extract_others[otherfilename].append(code[extract_globals[key]]);
    else:
        print colored(code[extract_globals[key]], 'blue')
        jscode +=code[extract_globals[key]]+"\n"


# print "extract_others", extract_others
print colored("function "+uid+"(input){","yellow")
jscode +="function "+uid+"(input){"+"\n"
adaptedIn = adaptinput(code[unmarshal_stmt],"id")
print colored(adaptedIn, 'blue')
jscode +=adaptedIn+"\n"
for key in sorted(extract_ftn.keys()):
    print colored("\t" + code[extract_ftn[key]], 'yellow')
    jscode += "\t"+code[extract_ftn[key]] + "\n"

print colored(adaptoutput(code[marshal_stmt], loadedVar), 'blue')
jscode +=adaptoutput(code[marshal_stmt], loadedVar) +"\n"
print colored("\treturn output;\n}","yellow")
jscode +="\treturn output;\n}"

if os.path.isdir("./results"):
    f=open("results/"+uid+".js", "w")
    f.write(jscode)
else:
    f=open("./"+uid+".js", "w")
    f.write(jscode)

# print extract_others
for key in extract_others:
    # print key, extract_others[key]
    if os.path.isdir("./results"):
        f = open("results/"+key, "w")
    else:
        f = open("./" + key, "w")
    txt = "//JS-RCI generated\n"
    for stmt in extract_others[key]:
        txt +=stmt
    f.write(txt)
    print colored("//depenent statements in File "+key+"\n"+txt, 'cyan')


print colored("Extracting Functions DONE!***********  \n See generated JS files in results folder, abcDe.js is entry",'magenta')

