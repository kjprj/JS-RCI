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
ref2         = Function('ref2',var, prop, val, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))
refs         = Function('refs',lineNum, val, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))

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
fp.register_relation(refs)

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


fp.register_relation(unMarshal,refs)
fp.declare_var(line1,v1,val1)
fp.rule(unMarshal(line1, 0, val1),refs(line1, val1))


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
sqlstmts=[];

#VariableDecl: var PROPERTIES = require('./mock-properties').data;
code[1000]="var PROPERTIES = require('./mock-properties').data;"
fp.fact(Write1(BitVecVal(1001,var),BitVecVal(1000,lineNum)))
fp.fact(Read2(BitVecVal(1002,var), BitVecVal(1004,prop), BitVecVal(1000,lineNum)))
fp.fact(Load(BitVecVal(1001,var),BitVecVal(1002,var), BitVecVal(1003,prop),BitVecVal(1000,lineNum)))
#functionDeclaration: findAll
code[1005]="function findAll(req, res, next) {\n    console.log(1);\n    var tmpv0 = PROPERTIES;\n    res.json(tmpv0);\n}"
fp.fact(FuncDecl(BitVecVal(1006,var),BitVecVal(1007,obj),BitVecVal(1005,lineNum)))
fp.fact(Formal(BitVecVal(1007,obj),BitVecVal(1008,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1007,obj),BitVecVal(1009,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1007,obj),BitVecVal(1010,obj),BitVecVal(3,obj)))
#CallExpression: console.log(1);
code[1011]="console.log(1);"
fp.fact(Actual(BitVecVal(1011,lineNum), BitVecVal(0,num), BitVecVal(1012,var)))
fp.fact(Heap(BitVecVal(1016,var),BitVecVal(1017,obj)))
fp.fact(Actual(BitVecVal(1011,lineNum), BitVecVal(1,num), BitVecVal(1016,var)))
#VariableDecl: var tmpv0 = PROPERTIES;
code[1018]="var tmpv0 = PROPERTIES;"
fp.fact(Write1(BitVecVal(1019,var),BitVecVal(1018,lineNum)))
fp.fact(Read1(BitVecVal(1001,var),BitVecVal(1018,lineNum)))
fp.fact(Assign(BitVecVal(1019,var),BitVecVal(1001,obj),BitVecVal(1018,lineNum)))
#CallExpression: res.json(tmpv0);
code[1020]="res.json(tmpv0);"
fp.fact(Actual(BitVecVal(1020,lineNum), BitVecVal(0,num), BitVecVal(1009,var)))
fp.fact(Heap(BitVecVal(1019,var),BitVecVal(1024,obj)))
fp.fact(Actual(BitVecVal(1020,lineNum), BitVecVal(1,num), BitVecVal(1019,var)))
#functionDeclaration: findById
code[1026]="function findById(req, res, next) {\n    var temp4 = req.params;\n    var idd2 = temp4.id;\n    var temp5 = idd2-1;\n    var temp6 = PROPERTIES[temp5];\n    var tmpv1 = temp6;\n    res.json(tmpv1);\n}"
fp.fact(FuncDecl(BitVecVal(1027,var),BitVecVal(1028,obj),BitVecVal(1026,lineNum)))
fp.fact(Formal(BitVecVal(1028,obj),BitVecVal(1029,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1028,obj),BitVecVal(1030,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1028,obj),BitVecVal(1031,obj),BitVecVal(3,obj)))
#VariableDecl: var temp4 = req.params;
code[1032]="var temp4 = req.params;"
fp.fact(Write1(BitVecVal(1033,var),BitVecVal(1032,lineNum)))
fp.fact(Read2(BitVecVal(1029,var), BitVecVal(1035,prop), BitVecVal(1032,lineNum)))
fp.fact(Load(BitVecVal(1033,var),BitVecVal(1029,var), BitVecVal(1034,prop),BitVecVal(1032,lineNum)))
#VariableDecl: var idd2 = temp4.id;
code[1036]="var idd2 = temp4.id;"
fp.fact(Write1(BitVecVal(1037,var),BitVecVal(1036,lineNum)))
fp.fact(Read2(BitVecVal(1033,var), BitVecVal(1039,prop), BitVecVal(1036,lineNum)))
fp.fact(Load(BitVecVal(1037,var),BitVecVal(1033,var), BitVecVal(1038,prop),BitVecVal(1036,lineNum)))
#VariableDecl: var temp5 = idd2-1;
code[1040]="var temp5 = idd2-1;"
fp.fact(Write1(BitVecVal(1041,var),BitVecVal(1040,lineNum)))
fp.fact(Write1(BitVecVal(1041,var),BitVecVal(1040,lineNum)))
fp.fact(Read1(BitVecVal(1042,var),BitVecVal(1040,lineNum)))
fp.fact(Assign(BitVecVal(1041,var),BitVecVal(1037,obj),BitVecVal(1040,lineNum)))
fp.fact(Write1(BitVecVal(1041,var),BitVecVal(1040,lineNum)))
fp.fact(Heap(BitVecVal(1042,var),BitVecVal(1044,obj)))
fp.fact(Assign(BitVecVal(1041,var),BitVecVal(1045,obj),BitVecVal(1040,lineNum)))
#VariableDecl: var temp6 = PROPERTIES[temp5];
code[1046]="var temp6 = PROPERTIES[temp5];"
fp.fact(Write1(BitVecVal(1047,var),BitVecVal(1046,lineNum)))
fp.fact(Read2(BitVecVal(1001,var), BitVecVal(1041,prop), BitVecVal(1046,lineNum)))
fp.fact(Load(BitVecVal(1047,var),BitVecVal(1001,var), BitVecVal(1048,prop),BitVecVal(1046,lineNum)))
#VariableDecl: var tmpv1 = temp6;
code[1049]="var tmpv1 = temp6;"
fp.fact(Write1(BitVecVal(1050,var),BitVecVal(1049,lineNum)))
fp.fact(Read1(BitVecVal(1051,var),BitVecVal(1049,lineNum)))
fp.fact(Assign(BitVecVal(1050,var),BitVecVal(1047,obj),BitVecVal(1049,lineNum)))
#CallExpression: res.json(tmpv1);
code[1051]="res.json(tmpv1);"
fp.fact(Actual(BitVecVal(1051,lineNum), BitVecVal(0,num), BitVecVal(1030,var)))
fp.fact(Heap(BitVecVal(1050,var),BitVecVal(1055,obj)))
fp.fact(Actual(BitVecVal(1051,lineNum), BitVecVal(1,num), BitVecVal(1050,var)))
#functionDeclaration: findById
code[1056]="function findById(req, res, next) {\n     var tmpv13 = req.params;\n     var id = tmpv13.id;\n     var tmpv10 = id - 1;\n     var tmpv2 = PROPERTIES[tmpv10];\n     res.json(tmpv2);\n}"
fp.fact(FuncDecl(BitVecVal(1027,var),BitVecVal(1028,obj),BitVecVal(1056,lineNum)))
fp.fact(Formal(BitVecVal(1028,obj),BitVecVal(1057,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1028,obj),BitVecVal(1058,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1028,obj),BitVecVal(1059,obj),BitVecVal(3,obj)))
#VariableDecl: var tmpv13 = req.params;
code[1060]="var tmpv13 = req.params;"
fp.fact(Write1(BitVecVal(1061,var),BitVecVal(1060,lineNum)))
fp.fact(Read2(BitVecVal(1057,var), BitVecVal(1063,prop), BitVecVal(1060,lineNum)))
fp.fact(Load(BitVecVal(1061,var),BitVecVal(1057,var), BitVecVal(1062,prop),BitVecVal(1060,lineNum)))
#VariableDecl: var id = tmpv13.id;
code[1064]="var id = tmpv13.id;"
fp.fact(Write1(BitVecVal(1065,var),BitVecVal(1064,lineNum)))
fp.fact(Read2(BitVecVal(1061,var), BitVecVal(1067,prop), BitVecVal(1064,lineNum)))
fp.fact(Load(BitVecVal(1065,var),BitVecVal(1061,var), BitVecVal(1066,prop),BitVecVal(1064,lineNum)))
#VariableDecl: var tmpv10 = id - 1;
code[1068]="var tmpv10 = id - 1;"
fp.fact(Write1(BitVecVal(1069,var),BitVecVal(1068,lineNum)))
fp.fact(Write1(BitVecVal(1069,var),BitVecVal(1068,lineNum)))
fp.fact(Read1(BitVecVal(1070,var),BitVecVal(1068,lineNum)))
fp.fact(Assign(BitVecVal(1069,var),BitVecVal(1065,obj),BitVecVal(1068,lineNum)))
fp.fact(Write1(BitVecVal(1069,var),BitVecVal(1068,lineNum)))
fp.fact(Heap(BitVecVal(1070,var),BitVecVal(1072,obj)))
fp.fact(Assign(BitVecVal(1069,var),BitVecVal(1073,obj),BitVecVal(1068,lineNum)))
#VariableDecl: var tmpv2 = PROPERTIES[tmpv10];
code[1074]="var tmpv2 = PROPERTIES[tmpv10];"
fp.fact(Write1(BitVecVal(1075,var),BitVecVal(1074,lineNum)))
fp.fact(Read2(BitVecVal(1001,var), BitVecVal(1069,prop), BitVecVal(1074,lineNum)))
fp.fact(Load(BitVecVal(1075,var),BitVecVal(1001,var), BitVecVal(1076,prop),BitVecVal(1074,lineNum)))
#CallExpression: res.json(tmpv2);
code[1077]="res.json(tmpv2);"
fp.fact(Actual(BitVecVal(1077,lineNum), BitVecVal(0,num), BitVecVal(1058,var)))
fp.fact(Heap(BitVecVal(1075,var),BitVecVal(1081,obj)))
fp.fact(Actual(BitVecVal(1077,lineNum), BitVecVal(1,num), BitVecVal(1075,var)))
#functionDeclaration: getFavorites
code[1082]="function getFavorites(req, res, next) {\n    var tmpv3 = favorites;\n    res.json(tmpv3);\n}"
fp.fact(FuncDecl(BitVecVal(1083,var),BitVecVal(1084,obj),BitVecVal(1082,lineNum)))
fp.fact(Formal(BitVecVal(1084,obj),BitVecVal(1085,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1084,obj),BitVecVal(1086,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1084,obj),BitVecVal(1087,obj),BitVecVal(3,obj)))
#VariableDecl: var tmpv3 = favorites;
code[1088]="var tmpv3 = favorites;"
fp.fact(Write1(BitVecVal(1089,var),BitVecVal(1088,lineNum)))
fp.fact(Read1(BitVecVal(1090,var),BitVecVal(1088,lineNum)))
fp.fact(Assign(BitVecVal(1089,var),BitVecVal(1090,obj),BitVecVal(1088,lineNum)))
#CallExpression: res.json(tmpv3);
code[1091]="res.json(tmpv3);"
fp.fact(Actual(BitVecVal(1091,lineNum), BitVecVal(0,num), BitVecVal(1086,var)))
fp.fact(Heap(BitVecVal(1089,var),BitVecVal(1095,obj)))
fp.fact(Actual(BitVecVal(1091,lineNum), BitVecVal(1,num), BitVecVal(1089,var)))
#functionDeclaration: favorite
code[1096]="function favorite(req, res, next) {\n    var property = req.body;\n    var exists = false;\n    for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }\n    }\n    if (!exists) var tmpv4 = property;\n    favorites.push(tmpv4);\n    var tmpv5 = \"success\";\n    res.send(tmpv5)\n}"
fp.fact(FuncDecl(BitVecVal(1097,var),BitVecVal(1098,obj),BitVecVal(1096,lineNum)))
fp.fact(Formal(BitVecVal(1098,obj),BitVecVal(1099,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1098,obj),BitVecVal(1100,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1098,obj),BitVecVal(1101,obj),BitVecVal(3,obj)))
#VariableDecl: var property = req.body;
code[1102]="var property = req.body;"
fp.fact(Write1(BitVecVal(1103,var),BitVecVal(1102,lineNum)))
fp.fact(Read2(BitVecVal(1099,var), BitVecVal(1105,prop), BitVecVal(1102,lineNum)))
fp.fact(Load(BitVecVal(1103,var),BitVecVal(1099,var), BitVecVal(1104,prop),BitVecVal(1102,lineNum)))
#VariableDecl: var exists = false;
code[1106]="var exists = false;"
fp.fact(Write1(BitVecVal(1107,var),BitVecVal(1106,lineNum)))
fp.fact(Heap(BitVecVal(1108,var),BitVecVal(1110,obj)))
fp.fact(Assign(BitVecVal(1107,var),BitVecVal(1111,obj),BitVecVal(1106,lineNum)))
code[1112]="for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }\n    }"
fp.fact(controldep(BitVecVal(1113,lineNum),BitVecVal(1112,lineNum)))
fp.fact(controldep(BitVecVal(1114,lineNum),BitVecVal(1112,lineNum)))
fp.fact(controldep(BitVecVal(1115,lineNum),BitVecVal(1112,lineNum)))
#VariableDecl: var i = 0
code[1113]="var i = 0"
fp.fact(Write1(BitVecVal(1116,var),BitVecVal(1113,lineNum)))
fp.fact(Heap(BitVecVal(1117,var),BitVecVal(1119,obj)))
fp.fact(Assign(BitVecVal(1116,var),BitVecVal(1120,obj),BitVecVal(1113,lineNum)))
#BinaryExpression: i < favorites.length
code[1114]="i < favorites.length"
fp.fact(Read1(BitVecVal(1121,var),BitVecVal(1114,lineNum)))
fp.fact(Assign(BitVecVal(0,var),BitVecVal(1116,obj),BitVecVal(1114,lineNum)))
fp.fact(Read2(BitVecVal(1121,var), BitVecVal(1123,prop), BitVecVal(1114,lineNum)))
fp.fact(Load(BitVecVal(0,var),BitVecVal(1121,var), BitVecVal(1122,prop),BitVecVal(1114,lineNum)))
#UpdateExpression: i++
code[1115]="i++"
fp.fact(Write1(BitVecVal(1116,var),BitVecVal(1115,lineNum)))
fp.fact(Read1(BitVecVal(1124,var),BitVecVal(1115,lineNum)))
fp.fact(Assign(BitVecVal(1116,var),BitVecVal(1116,obj),BitVecVal(1115,lineNum)))
code[1124]="if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }"
fp.fact(controldep(BitVecVal(1125,lineNum),BitVecVal(1124,lineNum)))
#BinaryExpression: favorites[i].id === property.id
code[1125]="favorites[i].id === property.id"
fp.fact(Read2(BitVecVal(1126,var), BitVecVal(1116,prop), BitVecVal(1125,lineNum)))
fp.fact(Load(BitVecVal(0,var),BitVecVal(1126,var), BitVecVal(1127,prop),BitVecVal(1125,lineNum)))
fp.fact(Read2(BitVecVal(1103,var), BitVecVal(1129,prop), BitVecVal(1125,lineNum)))
fp.fact(Load(BitVecVal(0,var),BitVecVal(1103,var), BitVecVal(1128,prop),BitVecVal(1125,lineNum)))
#Assignment: exists = true;"
code[1130]="exists = true;"
fp.fact(Write1(BitVecVal(1107,var),BitVecVal(1130,lineNum)))
fp.fact(Heap(BitVecVal(1131,var),BitVecVal(1133,obj)))
fp.fact(Assign(BitVecVal(1107,var),BitVecVal(1134,obj),BitVecVal(1130,lineNum)))
code[1136]="if (!exists) var tmpv4 = property;"
fp.fact(controldep(BitVecVal(1137,lineNum),BitVecVal(1136,lineNum)))
#VariableDecl: var tmpv4 = property;
code[1138]="var tmpv4 = property;"
fp.fact(Write1(BitVecVal(1139,var),BitVecVal(1138,lineNum)))
fp.fact(Read1(BitVecVal(1140,var),BitVecVal(1138,lineNum)))
fp.fact(Assign(BitVecVal(1139,var),BitVecVal(1103,obj),BitVecVal(1138,lineNum)))
#CallExpression: favorites.push(tmpv4);
code[1140]="favorites.push(tmpv4);"
fp.fact(Actual(BitVecVal(1140,lineNum), BitVecVal(0,num), BitVecVal(1141,var)))
fp.fact(Heap(BitVecVal(1139,var),BitVecVal(1145,obj)))
fp.fact(Actual(BitVecVal(1140,lineNum), BitVecVal(1,num), BitVecVal(1139,var)))
#VariableDecl: var tmpv5 = \"success\";
code[1146]="var tmpv5 = \"success\";"
fp.fact(Write1(BitVecVal(1147,var),BitVecVal(1146,lineNum)))
fp.fact(Heap(BitVecVal(1148,var),BitVecVal(1150,obj)))
fp.fact(Assign(BitVecVal(1147,var),BitVecVal(1151,obj),BitVecVal(1146,lineNum)))
#CallExpression: res.send(tmpv5)
code[1152]="res.send(tmpv5)"
fp.fact(Actual(BitVecVal(1152,lineNum), BitVecVal(0,num), BitVecVal(1100,var)))
fp.fact(Heap(BitVecVal(1147,var),BitVecVal(1156,obj)))
fp.fact(Actual(BitVecVal(1152,lineNum), BitVecVal(1,num), BitVecVal(1147,var)))
#functionDeclaration: unfavorite
code[1157]="function unfavorite(req, res, next) {\n    var tmpv14 = req.params;\nvar id = tmpv14.id;\n    for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }\n    }\n    var tmpv8 = favorites;\nres.json(tmpv8)\n}"
fp.fact(FuncDecl(BitVecVal(1158,var),BitVecVal(1159,obj),BitVecVal(1157,lineNum)))
fp.fact(Formal(BitVecVal(1159,obj),BitVecVal(1160,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1159,obj),BitVecVal(1161,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1159,obj),BitVecVal(1162,obj),BitVecVal(3,obj)))
#VariableDecl: var tmpv14 = req.params;
code[1163]="var tmpv14 = req.params;"
fp.fact(Write1(BitVecVal(1164,var),BitVecVal(1163,lineNum)))
fp.fact(Read2(BitVecVal(1160,var), BitVecVal(1166,prop), BitVecVal(1163,lineNum)))
fp.fact(Load(BitVecVal(1164,var),BitVecVal(1160,var), BitVecVal(1165,prop),BitVecVal(1163,lineNum)))
#VariableDecl: var id = tmpv14.id;
code[1167]="var id = tmpv14.id;"
fp.fact(Write1(BitVecVal(1168,var),BitVecVal(1167,lineNum)))
fp.fact(Read2(BitVecVal(1164,var), BitVecVal(1170,prop), BitVecVal(1167,lineNum)))
fp.fact(Load(BitVecVal(1168,var),BitVecVal(1164,var), BitVecVal(1169,prop),BitVecVal(1167,lineNum)))
code[1171]="for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }\n    }"
fp.fact(controldep(BitVecVal(1172,lineNum),BitVecVal(1171,lineNum)))
fp.fact(controldep(BitVecVal(1173,lineNum),BitVecVal(1171,lineNum)))
fp.fact(controldep(BitVecVal(1174,lineNum),BitVecVal(1171,lineNum)))
#VariableDecl: var i = 0
code[1172]="var i = 0"
fp.fact(Write1(BitVecVal(1175,var),BitVecVal(1172,lineNum)))
fp.fact(Heap(BitVecVal(1176,var),BitVecVal(1178,obj)))
fp.fact(Assign(BitVecVal(1175,var),BitVecVal(1179,obj),BitVecVal(1172,lineNum)))
#BinaryExpression: i < favorites.length
code[1173]="i < favorites.length"
fp.fact(Read1(BitVecVal(1180,var),BitVecVal(1173,lineNum)))
fp.fact(Assign(BitVecVal(0,var),BitVecVal(1175,obj),BitVecVal(1173,lineNum)))
fp.fact(Read2(BitVecVal(1180,var), BitVecVal(1182,prop), BitVecVal(1173,lineNum)))
fp.fact(Load(BitVecVal(0,var),BitVecVal(1180,var), BitVecVal(1181,prop),BitVecVal(1173,lineNum)))
#UpdateExpression: i++
code[1174]="i++"
fp.fact(Write1(BitVecVal(1175,var),BitVecVal(1174,lineNum)))
fp.fact(Read1(BitVecVal(1183,var),BitVecVal(1174,lineNum)))
fp.fact(Assign(BitVecVal(1175,var),BitVecVal(1175,obj),BitVecVal(1174,lineNum)))
code[1183]="if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }"
fp.fact(controldep(BitVecVal(1184,lineNum),BitVecVal(1183,lineNum)))
#BinaryExpression: favorites[i].id == id
code[1184]="favorites[i].id == id"
fp.fact(Read2(BitVecVal(1185,var), BitVecVal(1175,prop), BitVecVal(1184,lineNum)))
fp.fact(Load(BitVecVal(0,var),BitVecVal(1185,var), BitVecVal(1186,prop),BitVecVal(1184,lineNum)))
fp.fact(Read1(BitVecVal(1187,var),BitVecVal(1184,lineNum)))
fp.fact(Assign(BitVecVal(0,var),BitVecVal(1168,obj),BitVecVal(1184,lineNum)))
#VariableDecl: var tmpv6 = i;
code[1187]="var tmpv6 = i;"
fp.fact(Write1(BitVecVal(1188,var),BitVecVal(1187,lineNum)))
fp.fact(Read1(BitVecVal(1189,var),BitVecVal(1187,lineNum)))
fp.fact(Assign(BitVecVal(1188,var),BitVecVal(1175,obj),BitVecVal(1187,lineNum)))
#VariableDecl: var tmpv7 = 1;
code[1189]="var tmpv7 = 1;"
fp.fact(Write1(BitVecVal(1190,var),BitVecVal(1189,lineNum)))
fp.fact(Heap(BitVecVal(1191,var),BitVecVal(1193,obj)))
fp.fact(Assign(BitVecVal(1190,var),BitVecVal(1194,obj),BitVecVal(1189,lineNum)))
#CallExpression: favorites.splice(tmpv6, tmpv7);
code[1195]="favorites.splice(tmpv6, tmpv7);"
fp.fact(Actual(BitVecVal(1195,lineNum), BitVecVal(0,num), BitVecVal(1196,var)))
fp.fact(Heap(BitVecVal(1188,var),BitVecVal(1200,obj)))
fp.fact(Actual(BitVecVal(1195,lineNum), BitVecVal(1,num), BitVecVal(1188,var)))
fp.fact(Heap(BitVecVal(1190,var),BitVecVal(1204,obj)))
fp.fact(Actual(BitVecVal(1195,lineNum), BitVecVal(2,num), BitVecVal(1190,var)))
#VariableDecl: var tmpv8 = favorites;
code[1206]="var tmpv8 = favorites;"
fp.fact(Write1(BitVecVal(1207,var),BitVecVal(1206,lineNum)))
fp.fact(Read1(BitVecVal(1208,var),BitVecVal(1206,lineNum)))
fp.fact(Assign(BitVecVal(1207,var),BitVecVal(1208,obj),BitVecVal(1206,lineNum)))
#CallExpression: res.json(tmpv8)
code[1209]="res.json(tmpv8)"
fp.fact(Actual(BitVecVal(1209,lineNum), BitVecVal(0,num), BitVecVal(1161,var)))
fp.fact(Heap(BitVecVal(1207,var),BitVecVal(1213,obj)))
fp.fact(Actual(BitVecVal(1209,lineNum), BitVecVal(1,num), BitVecVal(1207,var)))
#functionDeclaration: like
code[1214]="function like(req, res, next) {\n    var property = req.body;\n    var tmpv11 = property.id - 1;\nPROPERTIES[tmpv11].likes++;\n    var tmpv12 = property.id - 1;\nvar tmpv9 = PROPERTIES[tmpv12].likes;\nres.json(tmpv9);\n}"
fp.fact(FuncDecl(BitVecVal(1215,var),BitVecVal(1216,obj),BitVecVal(1214,lineNum)))
fp.fact(Formal(BitVecVal(1216,obj),BitVecVal(1217,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1216,obj),BitVecVal(1218,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1216,obj),BitVecVal(1219,obj),BitVecVal(3,obj)))
#VariableDecl: var property = req.body;
code[1220]="var property = req.body;"
fp.fact(Write1(BitVecVal(1221,var),BitVecVal(1220,lineNum)))
fp.fact(Read2(BitVecVal(1217,var), BitVecVal(1223,prop), BitVecVal(1220,lineNum)))
fp.fact(Load(BitVecVal(1221,var),BitVecVal(1217,var), BitVecVal(1222,prop),BitVecVal(1220,lineNum)))
#VariableDecl: var tmpv11 = property.id - 1;
code[1224]="var tmpv11 = property.id - 1;"
fp.fact(Write1(BitVecVal(1225,var),BitVecVal(1224,lineNum)))
fp.fact(Write1(BitVecVal(1225,var),BitVecVal(1224,lineNum)))
fp.fact(Read2(BitVecVal(1221,var), BitVecVal(1227,prop), BitVecVal(1224,lineNum)))
fp.fact(Load(BitVecVal(1225,var),BitVecVal(1221,var), BitVecVal(1226,prop),BitVecVal(1224,lineNum)))
fp.fact(Write1(BitVecVal(1225,var),BitVecVal(1224,lineNum)))
fp.fact(Heap(BitVecVal(1228,var),BitVecVal(1230,obj)))
fp.fact(Assign(BitVecVal(1225,var),BitVecVal(1231,obj),BitVecVal(1224,lineNum)))
#UpdateExpression: PROPERTIES[tmpv11].likes++;
code[1232]="PROPERTIES[tmpv11].likes++;"
fp.fact(Write2(BitVecVal(1001,obj),BitVecVal(1225,var), BitVecVal(1232,lineNum)))
fp.fact(Read2(BitVecVal(1001,var), BitVecVal(1225,prop), BitVecVal(1232,lineNum)))
fp.fact(Load(BitVecVal(1234,var),BitVecVal(1233,prop), BitVecVal(1233,var),BitVecVal(1232,lineNum)))
fp.fact(Store(BitVecVal(1076,var),BitVecVal(1001,prop), BitVecVal(1233,var), BitVecVal(1232,lineNum)))
#VariableDecl: var tmpv12 = property.id - 1;
code[1235]="var tmpv12 = property.id - 1;"
fp.fact(Write1(BitVecVal(1236,var),BitVecVal(1235,lineNum)))
fp.fact(Write1(BitVecVal(1236,var),BitVecVal(1235,lineNum)))
fp.fact(Read2(BitVecVal(1221,var), BitVecVal(1238,prop), BitVecVal(1235,lineNum)))
fp.fact(Load(BitVecVal(1236,var),BitVecVal(1221,var), BitVecVal(1237,prop),BitVecVal(1235,lineNum)))
fp.fact(Write1(BitVecVal(1236,var),BitVecVal(1235,lineNum)))
fp.fact(Heap(BitVecVal(1239,var),BitVecVal(1241,obj)))
fp.fact(Assign(BitVecVal(1236,var),BitVecVal(1242,obj),BitVecVal(1235,lineNum)))
#VariableDecl: var tmpv9 = PROPERTIES[tmpv12].likes;
code[1243]="var tmpv9 = PROPERTIES[tmpv12].likes;"
fp.fact(Write1(BitVecVal(1244,var),BitVecVal(1243,lineNum)))
fp.fact(Read2(BitVecVal(1001,var), BitVecVal(1236,prop), BitVecVal(1243,lineNum)))
fp.fact(Load(BitVecVal(1244,var),BitVecVal(1001,var), BitVecVal(1245,prop),BitVecVal(1243,lineNum)))
#CallExpression: res.json(tmpv9);
code[1246]="res.json(tmpv9);"
fp.fact(Actual(BitVecVal(1246,lineNum), BitVecVal(0,num), BitVecVal(1218,var)))
fp.fact(Heap(BitVecVal(1244,var),BitVecVal(1250,obj)))
fp.fact(Actual(BitVecVal(1246,lineNum), BitVecVal(1,num), BitVecVal(1244,var)))
#Assignment: exports.findAll = findAll;"
code[1251]="exports.findAll = findAll;"
fp.fact(Write2(BitVecVal(1252,obj),BitVecVal(1253,var), BitVecVal(1251,lineNum)))
fp.fact(Read1(BitVecVal(1254,var),BitVecVal(1251,lineNum)))
fp.fact(Store(BitVecVal(3567,var),BitVecVal(1007,var), BitVecVal(1254,prop), BitVecVal(1251,lineNum)))
#Assignment: exports.findById = findById;"
code[1255]="exports.findById = findById;"
fp.fact(Write2(BitVecVal(1256,obj),BitVecVal(1257,var), BitVecVal(1255,lineNum)))
fp.fact(Read1(BitVecVal(1258,var),BitVecVal(1255,lineNum)))
fp.fact(Store(BitVecVal(1252,var),BitVecVal(1028,var), BitVecVal(1258,prop), BitVecVal(1255,lineNum)))
#Assignment: exports.getFavorites = getFavorites;"
code[1259]="exports.getFavorites = getFavorites;"
fp.fact(Write2(BitVecVal(1260,obj),BitVecVal(1261,var), BitVecVal(1259,lineNum)))
fp.fact(Read1(BitVecVal(1262,var),BitVecVal(1259,lineNum)))
fp.fact(Store(BitVecVal(1256,var),BitVecVal(1084,var), BitVecVal(1262,prop), BitVecVal(1259,lineNum)))
#Assignment: exports.favorite = favorite;"
code[1263]="exports.favorite = favorite;"
fp.fact(Write2(BitVecVal(1264,obj),BitVecVal(1265,var), BitVecVal(1263,lineNum)))
fp.fact(Read1(BitVecVal(1266,var),BitVecVal(1263,lineNum)))
fp.fact(Store(BitVecVal(1260,var),BitVecVal(1098,var), BitVecVal(1266,prop), BitVecVal(1263,lineNum)))
#Assignment: exports.unfavorite = unfavorite;"
code[1267]="exports.unfavorite = unfavorite;"
fp.fact(Write2(BitVecVal(1268,obj),BitVecVal(1269,var), BitVecVal(1267,lineNum)))
fp.fact(Read1(BitVecVal(1270,var),BitVecVal(1267,lineNum)))
fp.fact(Store(BitVecVal(1264,var),BitVecVal(1159,var), BitVecVal(1270,prop), BitVecVal(1267,lineNum)))
#Assignment: exports.like = like;"
code[1271]="exports.like = like;"
fp.fact(Write2(BitVecVal(1272,obj),BitVecVal(1273,var), BitVecVal(1271,lineNum)))
fp.fact(Read1(BitVecVal(1274,var),BitVecVal(1271,lineNum)))
fp.fact(Store(BitVecVal(1268,var),BitVecVal(1216,var), BitVecVal(1274,prop), BitVecVal(1271,lineNum)))






fp.fact(controldep(BitVecVal(1011,lineNum),BitVecVal(1018,lineNum)))

fp.fact(controldep(BitVecVal(1018,lineNum),BitVecVal(1020,lineNum)))


fp.fact(controldep(BitVecVal(1032,lineNum),BitVecVal(1036,lineNum)))

fp.fact(controldep(BitVecVal(1036,lineNum),BitVecVal(1040,lineNum)))

fp.fact(controldep(BitVecVal(1040,lineNum),BitVecVal(1046,lineNum)))

fp.fact(controldep(BitVecVal(1046,lineNum),BitVecVal(1049,lineNum)))

fp.fact(controldep(BitVecVal(1049,lineNum),BitVecVal(1051,lineNum)))



fp.fact(controldep(BitVecVal(1060,lineNum),BitVecVal(1064,lineNum)))

fp.fact(controldep(BitVecVal(1064,lineNum),BitVecVal(1068,lineNum)))

fp.fact(controldep(BitVecVal(1068,lineNum),BitVecVal(1074,lineNum)))

fp.fact(controldep(BitVecVal(1074,lineNum),BitVecVal(1077,lineNum)))



fp.fact(controldep(BitVecVal(1088,lineNum),BitVecVal(1091,lineNum)))



fp.fact(controldep(BitVecVal(1102,lineNum),BitVecVal(1106,lineNum)))



fp.fact(controldep(BitVecVal(1112,lineNum),BitVecVal(1124,lineNum)))

fp.fact(controldep(BitVecVal(1124,lineNum),BitVecVal(1130,lineNum)))

fp.fact(controldep(BitVecVal(1112,lineNum),BitVecVal(1136,lineNum)))

fp.fact(controldep(BitVecVal(1136,lineNum),BitVecVal(1138,lineNum)))

fp.fact(controldep(BitVecVal(1136,lineNum),BitVecVal(1140,lineNum)))

fp.fact(controldep(BitVecVal(1140,lineNum),BitVecVal(1146,lineNum)))

fp.fact(controldep(BitVecVal(1146,lineNum),BitVecVal(1152,lineNum)))



fp.fact(controldep(BitVecVal(1163,lineNum),BitVecVal(1167,lineNum)))



fp.fact(controldep(BitVecVal(1171,lineNum),BitVecVal(1183,lineNum)))

fp.fact(controldep(BitVecVal(1183,lineNum),BitVecVal(1187,lineNum)))

fp.fact(controldep(BitVecVal(1187,lineNum),BitVecVal(1189,lineNum)))

fp.fact(controldep(BitVecVal(1189,lineNum),BitVecVal(1195,lineNum)))

fp.fact(controldep(BitVecVal(1171,lineNum),BitVecVal(1206,lineNum)))

fp.fact(controldep(BitVecVal(1206,lineNum),BitVecVal(1209,lineNum)))



fp.fact(controldep(BitVecVal(1220,lineNum),BitVecVal(1224,lineNum)))

fp.fact(controldep(BitVecVal(1224,lineNum),BitVecVal(1232,lineNum)))

fp.fact(controldep(BitVecVal(1232,lineNum),BitVecVal(1235,lineNum)))

fp.fact(controldep(BitVecVal(1235,lineNum),BitVecVal(1243,lineNum)))

fp.fact(controldep(BitVecVal(1243,lineNum),BitVecVal(1246,lineNum)))







hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:16:67"]={"bin":1000, "name":"var PROPERTIES = require('./mock-properties').data;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:20:30"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:33:61"]={"bin":1002, "name":"require('./mock-properties')"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:33:66"]={"bin":1003, "name":"require('./mock-properties').data"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:62:66"]={"bin":1004, "name":"data"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:91:196"]={"bin":1005, "name":"function findAll(req, res, next) {\n    console.log(1);\n    var tmpv0 = PROPERTIES;\n    res.json(tmpv0);\n}"};
hashVar["O_findAll"]={"bin":1006, "name":"O_findAll"};
hashVar["findAll"]={"bin":1007, "name":"findAll"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:108:111"]={"bin":1008, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:113:116"]={"bin":1009, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:118:122"]={"bin":1010, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:130:145"]={"bin":1011, "name":"console.log(1);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:130:137"]={"bin":1012, "name":"console"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:142:143"]={"bin":1016, "name":"1"};
hashVar["0tempHash"]={"bin":1017, "name":"0tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:150:173"]={"bin":1018, "name":"var tmpv0 = PROPERTIES;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:154:159"]={"bin":1019, "name":"tmpv0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:162:172"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:178:194"]={"bin":1020, "name":"res.json(tmpv0);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:178:181"]={"bin":1009, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:187:192"]={"bin":1019, "name":"tmpv0"};
hashVar["1tempHash"]={"bin":1024, "name":"1tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:196:197"]={"bin":1025, "name":";"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:200:393"]={"bin":1026, "name":"function findById(req, res, next) {\n    var temp4 = req.params;\n    var idd2 = temp4.id;\n    var temp5 = idd2-1;\n    var temp6 = PROPERTIES[temp5];\n    var tmpv1 = temp6;\n    res.json(tmpv1);\n}"};
hashVar["O_findById"]={"bin":1027, "name":"O_findById"};
hashVar["findById"]={"bin":1028, "name":"findById"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:218:221"]={"bin":1029, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:223:226"]={"bin":1030, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:228:232"]={"bin":1031, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:240:263"]={"bin":1032, "name":"var temp4 = req.params;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:244:249"]={"bin":1033, "name":"temp4"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:252:255"]={"bin":1029, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:252:262"]={"bin":1034, "name":"req.params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:256:262"]={"bin":1035, "name":"params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:268:288"]={"bin":1036, "name":"var idd2 = temp4.id;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:272:276"]={"bin":1037, "name":"idd2"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:279:284"]={"bin":1033, "name":"temp4"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:279:287"]={"bin":1038, "name":"temp4.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:285:287"]={"bin":1039, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:293:312"]={"bin":1040, "name":"var temp5 = idd2-1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:297:302"]={"bin":1041, "name":"temp5"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:305:309"]={"bin":1037, "name":"idd2"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:317:347"]={"bin":1046, "name":"var temp6 = PROPERTIES[temp5];"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:321:326"]={"bin":1047, "name":"temp6"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:329:339"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:329:346"]={"bin":1048, "name":"PROPERTIES[temp5]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:340:345"]={"bin":1041, "name":"temp5"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:352:370"]={"bin":1049, "name":"var tmpv1 = temp6;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:356:361"]={"bin":1050, "name":"tmpv1"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:364:369"]={"bin":1047, "name":"temp6"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:375:391"]={"bin":1051, "name":"res.json(tmpv1);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:375:378"]={"bin":1030, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:384:389"]={"bin":1050, "name":"tmpv1"};
hashVar["3tempHash"]={"bin":1055, "name":"3tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:423:600"]={"bin":1056, "name":"function findById(req, res, next) {\n     var tmpv13 = req.params;\n     var id = tmpv13.id;\n     var tmpv10 = id - 1;\n     var tmpv2 = PROPERTIES[tmpv10];\n     res.json(tmpv2);\n}"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:441:444"]={"bin":1057, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:446:449"]={"bin":1058, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:451:455"]={"bin":1059, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:464:488"]={"bin":1060, "name":"var tmpv13 = req.params;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:468:474"]={"bin":1061, "name":"tmpv13"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:477:480"]={"bin":1057, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:477:487"]={"bin":1062, "name":"req.params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:481:487"]={"bin":1063, "name":"params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:494:513"]={"bin":1064, "name":"var id = tmpv13.id;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:498:500"]={"bin":1065, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:503:509"]={"bin":1061, "name":"tmpv13"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:503:512"]={"bin":1066, "name":"tmpv13.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:510:512"]={"bin":1067, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:519:539"]={"bin":1068, "name":"var tmpv10 = id - 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:523:529"]={"bin":1069, "name":"tmpv10"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:532:534"]={"bin":1065, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:545:576"]={"bin":1074, "name":"var tmpv2 = PROPERTIES[tmpv10];"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:549:554"]={"bin":1075, "name":"tmpv2"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:557:567"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:557:575"]={"bin":1076, "name":"PROPERTIES[tmpv10]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:568:574"]={"bin":1069, "name":"tmpv10"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:582:598"]={"bin":1077, "name":"res.json(tmpv2);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:582:585"]={"bin":1058, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:591:596"]={"bin":1075, "name":"tmpv2"};
hashVar["5tempHash"]={"bin":1081, "name":"5tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:604:693"]={"bin":1082, "name":"function getFavorites(req, res, next) {\n    var tmpv3 = favorites;\n    res.json(tmpv3);\n}"};
hashVar["O_getFavorites"]={"bin":1083, "name":"O_getFavorites"};
hashVar["getFavorites"]={"bin":1084, "name":"getFavorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:626:629"]={"bin":1085, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:631:634"]={"bin":1086, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:636:640"]={"bin":1087, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:648:670"]={"bin":1088, "name":"var tmpv3 = favorites;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:652:657"]={"bin":1089, "name":"tmpv3"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:660:669"]={"bin":1090, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:675:691"]={"bin":1091, "name":"res.json(tmpv3);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:675:678"]={"bin":1086, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:684:689"]={"bin":1089, "name":"tmpv3"};
hashVar["6tempHash"]={"bin":1095, "name":"6tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:695:1056"]={"bin":1096, "name":"function favorite(req, res, next) {\n    var property = req.body;\n    var exists = false;\n    for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }\n    }\n    if (!exists) var tmpv4 = property;\n    favorites.push(tmpv4);\n    var tmpv5 = \"success\";\n    res.send(tmpv5)\n}"};
hashVar["O_favorite"]={"bin":1097, "name":"O_favorite"};
hashVar["favorite"]={"bin":1098, "name":"favorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:713:716"]={"bin":1099, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:718:721"]={"bin":1100, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:723:727"]={"bin":1101, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:735:759"]={"bin":1102, "name":"var property = req.body;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:739:747"]={"bin":1103, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:750:753"]={"bin":1099, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:750:758"]={"bin":1104, "name":"req.body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:754:758"]={"bin":1105, "name":"body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:764:783"]={"bin":1106, "name":"var exists = false;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:768:774"]={"bin":1107, "name":"exists"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:788:941"]={"bin":1112, "name":"for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }\n    }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:793:802"]={"bin":1113, "name":"var i = 0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:804:824"]={"bin":1114, "name":"i < favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:826:829"]={"bin":1115, "name":"i++"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:797:798"]={"bin":1116, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:804:805"]={"bin":1116, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:808:817"]={"bin":1121, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:808:824"]={"bin":1122, "name":"favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:818:824"]={"bin":1123, "name":"length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:826:827"]={"bin":1116, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:841:935"]={"bin":1124, "name":"if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:845:876"]={"bin":1125, "name":"favorites[i].id === property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:845:854"]={"bin":1126, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:845:857"]={"bin":1127, "name":"favorites[i]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:855:856"]={"bin":1116, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:865:873"]={"bin":1103, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:865:876"]={"bin":1128, "name":"property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:874:876"]={"bin":1129, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:892:906"]={"bin":1130, "name":"exists = true;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:892:898"]={"bin":1107, "name":"exists"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:919:925"]={"bin":1135, "name":"break;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:946:980"]={"bin":1136, "name":"if (!exists) var tmpv4 = property;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:950:957"]={"bin":1137, "name":"!exists"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:959:980"]={"bin":1138, "name":"var tmpv4 = property;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:963:968"]={"bin":1139, "name":"tmpv4"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:971:979"]={"bin":1103, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:985:1007"]={"bin":1140, "name":"favorites.push(tmpv4);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:985:994"]={"bin":1141, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1000:1005"]={"bin":1139, "name":"tmpv4"};
hashVar["10tempHash"]={"bin":1145, "name":"10tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1012:1034"]={"bin":1146, "name":"var tmpv5 = \"success\";"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1016:1021"]={"bin":1147, "name":"tmpv5"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1039:1054"]={"bin":1152, "name":"res.send(tmpv5)"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1039:1042"]={"bin":1100, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1048:1053"]={"bin":1147, "name":"tmpv5"};
hashVar["12tempHash"]={"bin":1156, "name":"12tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1058:1385"]={"bin":1157, "name":"function unfavorite(req, res, next) {\n    var tmpv14 = req.params;\nvar id = tmpv14.id;\n    for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }\n    }\n    var tmpv8 = favorites;\nres.json(tmpv8)\n}"};
hashVar["O_unfavorite"]={"bin":1158, "name":"O_unfavorite"};
hashVar["unfavorite"]={"bin":1159, "name":"unfavorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1078:1081"]={"bin":1160, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1083:1086"]={"bin":1161, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1088:1092"]={"bin":1162, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1100:1124"]={"bin":1163, "name":"var tmpv14 = req.params;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1104:1110"]={"bin":1164, "name":"tmpv14"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1113:1116"]={"bin":1160, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1113:1123"]={"bin":1165, "name":"req.params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1117:1123"]={"bin":1166, "name":"params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1125:1144"]={"bin":1167, "name":"var id = tmpv14.id;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1129:1131"]={"bin":1168, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1134:1140"]={"bin":1164, "name":"tmpv14"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1134:1143"]={"bin":1169, "name":"tmpv14.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1141:1143"]={"bin":1170, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1149:1340"]={"bin":1171, "name":"for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }\n    }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1154:1163"]={"bin":1172, "name":"var i = 0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1165:1185"]={"bin":1173, "name":"i < favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1187:1190"]={"bin":1174, "name":"i++"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1158:1159"]={"bin":1175, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1165:1166"]={"bin":1175, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1169:1178"]={"bin":1180, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1169:1185"]={"bin":1181, "name":"favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1179:1185"]={"bin":1182, "name":"length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1187:1188"]={"bin":1175, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1202:1334"]={"bin":1183, "name":"if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1206:1227"]={"bin":1184, "name":"favorites[i].id == id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1206:1215"]={"bin":1185, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1206:1218"]={"bin":1186, "name":"favorites[i]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1216:1217"]={"bin":1175, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1225:1227"]={"bin":1168, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1243:1257"]={"bin":1187, "name":"var tmpv6 = i;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1247:1252"]={"bin":1188, "name":"tmpv6"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1255:1256"]={"bin":1175, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1259:1273"]={"bin":1189, "name":"var tmpv7 = 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1263:1268"]={"bin":1190, "name":"tmpv7"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1274:1305"]={"bin":1195, "name":"favorites.splice(tmpv6, tmpv7);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1274:1283"]={"bin":1196, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1291:1296"]={"bin":1188, "name":"tmpv6"};
hashVar["15tempHash"]={"bin":1200, "name":"15tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1298:1303"]={"bin":1190, "name":"tmpv7"};
hashVar["16tempHash"]={"bin":1204, "name":"16tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1318:1324"]={"bin":1205, "name":"break;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1345:1367"]={"bin":1206, "name":"var tmpv8 = favorites;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1349:1354"]={"bin":1207, "name":"tmpv8"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1357:1366"]={"bin":1208, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1368:1383"]={"bin":1209, "name":"res.json(tmpv8)"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1368:1371"]={"bin":1161, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1377:1382"]={"bin":1207, "name":"tmpv8"};
hashVar["17tempHash"]={"bin":1213, "name":"17tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1387:1600"]={"bin":1214, "name":"function like(req, res, next) {\n    var property = req.body;\n    var tmpv11 = property.id - 1;\nPROPERTIES[tmpv11].likes++;\n    var tmpv12 = property.id - 1;\nvar tmpv9 = PROPERTIES[tmpv12].likes;\nres.json(tmpv9);\n}"};
hashVar["O_like"]={"bin":1215, "name":"O_like"};
hashVar["like"]={"bin":1216, "name":"like"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1401:1404"]={"bin":1217, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1406:1409"]={"bin":1218, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1411:1415"]={"bin":1219, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1423:1447"]={"bin":1220, "name":"var property = req.body;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1427:1435"]={"bin":1221, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1438:1441"]={"bin":1217, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1438:1446"]={"bin":1222, "name":"req.body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1442:1446"]={"bin":1223, "name":"body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1452:1481"]={"bin":1224, "name":"var tmpv11 = property.id - 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1456:1462"]={"bin":1225, "name":"tmpv11"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1465:1473"]={"bin":1221, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1465:1476"]={"bin":1226, "name":"property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1474:1476"]={"bin":1227, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1482:1509"]={"bin":1232, "name":"PROPERTIES[tmpv11].likes++;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1482:1492"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1493:1499"]={"bin":1225, "name":"tmpv11"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1482:1500"]={"bin":1233, "name":"PROPERTIES[tmpv11]"};
hashVar["ttemp0"]={"bin":1234, "name":"ttemp0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1514:1543"]={"bin":1235, "name":"var tmpv12 = property.id - 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1518:1524"]={"bin":1236, "name":"tmpv12"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1527:1535"]={"bin":1221, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1527:1538"]={"bin":1237, "name":"property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1536:1538"]={"bin":1238, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1544:1581"]={"bin":1243, "name":"var tmpv9 = PROPERTIES[tmpv12].likes;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1548:1553"]={"bin":1244, "name":"tmpv9"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1556:1566"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1556:1574"]={"bin":1245, "name":"PROPERTIES[tmpv12]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1567:1573"]={"bin":1236, "name":"tmpv12"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1582:1598"]={"bin":1246, "name":"res.json(tmpv9);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1582:1585"]={"bin":1218, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1591:1596"]={"bin":1244, "name":"tmpv9"};
hashVar["20tempHash"]={"bin":1250, "name":"20tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1602:1628"]={"bin":1251, "name":"exports.findAll = findAll;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1602:1609"]={"bin":1252, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1610:1617"]={"bin":1253, "name":"findAll"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1620:1627"]={"bin":1254, "name":"findAll"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1629:1657"]={"bin":1255, "name":"exports.findById = findById;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1629:1636"]={"bin":1256, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1637:1645"]={"bin":1257, "name":"findById"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1648:1656"]={"bin":1258, "name":"findById"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1658:1694"]={"bin":1259, "name":"exports.getFavorites = getFavorites;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1658:1665"]={"bin":1260, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1666:1678"]={"bin":1261, "name":"getFavorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1681:1693"]={"bin":1262, "name":"getFavorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1695:1723"]={"bin":1263, "name":"exports.favorite = favorite;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1695:1702"]={"bin":1264, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1703:1711"]={"bin":1265, "name":"favorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1714:1722"]={"bin":1266, "name":"favorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1724:1756"]={"bin":1267, "name":"exports.unfavorite = unfavorite;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1724:1731"]={"bin":1268, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1732:1742"]={"bin":1269, "name":"unfavorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1745:1755"]={"bin":1270, "name":"unfavorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1757:1777"]={"bin":1271, "name":"exports.like = like;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1757:1764"]={"bin":1272, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1765:1769"]={"bin":1273, "name":"like"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1772:1776"]={"bin":1274, "name":"like"};
#Assignment: exports.data = [\n        {\n            id: 1,\n            city: 'Boston',\n            state: 'MA',\n            price: '$475,000',\n            title: 'Condominium Redefined',\n            beds: 2,\n            baths: 2,\n            likes: 5,\n            broker: {\n                id: 1,\n                name: \"Caroline Kingsley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/caroline_kingsley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house08wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house08sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 2,\n            city: 'Cambridge',\n            state: 'MA',\n            price: '$1,200,000',\n            title: 'Ultimate Sophistication',\n            beds: 5,\n            baths: 4,\n            likes: 2,\n            broker: {\n                id: 2,\n                name: \"Michael Jones\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/michael_jones.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house02wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house02sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 3,\n            city: 'Boston',\n            state: 'MA',\n            price: '$650,000',\n            title: 'Seaport District Retreat',\n            beds: 3,\n            baths: 2,\n            likes: 6,\n            broker: {\n                id: 3,\n                name: \"Jonathan Bradley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jonathan_bradley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house09wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house09sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 4,\n            city: 'Boston',\n            state: 'MA',\n            price: '$875,000',\n            title: 'Modern City Living',\n            beds: 3,\n            baths: 2,\n            likes: 12,\n            broker: {\n                id: 4,\n                name: \"Jennifer Wu\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jennifer_wu.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house14.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house14sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 5,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$425,000',\n            title: 'Urban Efficiency',\n            beds: 4,\n            baths: 2,\n            likes: 5,\n            broker: {\n                id: 5,\n                name: \"Olivia Green\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/olivia_green.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house03wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house03sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 6,\n            city: 'Boston',\n            state: 'MA',\n            price: '$550,000',\n            title: 'Waterfront in the City',\n            beds: 3,\n            baths: 2,\n            likes: 14,\n            broker: {\n                id: 6,\n                name: \"Miriam Aupont\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/miriam_aupont.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house05wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house05sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 7,\n            city: 'Brookline',\n            state: 'MA',\n            zip: '02420',\n            price: '$850,000',\n            title: 'Suburban Extravaganza',\n            beds: 5,\n            baths: 4,\n            likes: 5,\n            broker: {\n                id: 7,\n                name: \"Michelle Lambert\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/michelle_lambert.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house07wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house07sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 8,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$925,000',\n            title: 'Contemporary Luxury',\n            beds: 6,\n            baths: 6,\n            sqft: 950,\n            likes: 8,\n            broker: {\n                id: 8,\n                name: \"Victor Oachoa\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/victor_ochoa.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house12wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house12sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 9,\n            city: 'Cambridge',\n            state: 'MA',\n            zip: '02420',\n            price: '$550,000',\n            title: 'Heart of Harvard Square',\n            beds: 5,\n            baths: 4,\n            likes: 9,\n            broker: {\n                id: 1,\n                name: \"Caroline Kingsley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/caroline_kingsley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house10.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house10sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 10,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$375,000',\n            title: 'Architectural Details',\n            beds: 2,\n            baths: 2,\n            likes: 10,\n            broker: {\n                id: 2,\n                name: \"Michael Jones\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/michael_jones.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house11wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house11sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 11,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$495,000',\n            title: 'Modern Elegance',\n            beds: 2,\n            baths: 2,\n            likes: 16,\n            broker: {\n                id: 3,\n                name: \"Jonathan Bradley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jonathan_bradley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house13wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house13sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 12,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$625,000',\n            title: 'Stunning Colonial',\n            beds: 4,\n            baths: 2,\n            likes: 9,\n            broker: {\n                id: 4,\n                name: \"Jennifer Wu\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jennifer_wu.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house06wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house06sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 13,\n            city: 'Cambridge',\n            state: 'MA',\n            zip: '02420',\n            price: '$430,000',\n            title: 'Quiet Retreat',\n            beds: 5,\n            baths:4,\n            likes: 18,\n            broker: {\n                id: 5,\n                name: \"Olivia Green\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/olivia_green.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house04.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house04sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 14,\n            city: 'Cambridge',\n            state: 'MA',\n            zip: '01742',\n            price: '$450,000',\n            title: 'Victorian Revival',\n            beds: 4,\n            baths:3,\n            sqft: 3800,\n            likes: 10,\n            broker: {\n                id: 6,\n                name: \"Miriam Aupont\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/miriam_aupont.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house01wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house01sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        }\n    ];"
code[1275]="exports.data = [\n        {\n            id: 1,\n            city: 'Boston',\n            state: 'MA',\n            price: '$475,000',\n            title: 'Condominium Redefined',\n            beds: 2,\n            baths: 2,\n            likes: 5,\n            broker: {\n                id: 1,\n                name: \"Caroline Kingsley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/caroline_kingsley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house08wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house08sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 2,\n            city: 'Cambridge',\n            state: 'MA',\n            price: '$1,200,000',\n            title: 'Ultimate Sophistication',\n            beds: 5,\n            baths: 4,\n            likes: 2,\n            broker: {\n                id: 2,\n                name: \"Michael Jones\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/michael_jones.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house02wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house02sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 3,\n            city: 'Boston',\n            state: 'MA',\n            price: '$650,000',\n            title: 'Seaport District Retreat',\n            beds: 3,\n            baths: 2,\n            likes: 6,\n            broker: {\n                id: 3,\n                name: \"Jonathan Bradley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jonathan_bradley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house09wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house09sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 4,\n            city: 'Boston',\n            state: 'MA',\n            price: '$875,000',\n            title: 'Modern City Living',\n            beds: 3,\n            baths: 2,\n            likes: 12,\n            broker: {\n                id: 4,\n                name: \"Jennifer Wu\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jennifer_wu.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house14.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house14sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 5,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$425,000',\n            title: 'Urban Efficiency',\n            beds: 4,\n            baths: 2,\n            likes: 5,\n            broker: {\n                id: 5,\n                name: \"Olivia Green\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/olivia_green.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house03wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house03sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 6,\n            city: 'Boston',\n            state: 'MA',\n            price: '$550,000',\n            title: 'Waterfront in the City',\n            beds: 3,\n            baths: 2,\n            likes: 14,\n            broker: {\n                id: 6,\n                name: \"Miriam Aupont\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/miriam_aupont.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house05wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house05sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 7,\n            city: 'Brookline',\n            state: 'MA',\n            zip: '02420',\n            price: '$850,000',\n            title: 'Suburban Extravaganza',\n            beds: 5,\n            baths: 4,\n            likes: 5,\n            broker: {\n                id: 7,\n                name: \"Michelle Lambert\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/michelle_lambert.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house07wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house07sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 8,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$925,000',\n            title: 'Contemporary Luxury',\n            beds: 6,\n            baths: 6,\n            sqft: 950,\n            likes: 8,\n            broker: {\n                id: 8,\n                name: \"Victor Oachoa\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/victor_ochoa.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house12wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house12sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 9,\n            city: 'Cambridge',\n            state: 'MA',\n            zip: '02420',\n            price: '$550,000',\n            title: 'Heart of Harvard Square',\n            beds: 5,\n            baths: 4,\n            likes: 9,\n            broker: {\n                id: 1,\n                name: \"Caroline Kingsley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/caroline_kingsley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house10.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house10sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 10,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$375,000',\n            title: 'Architectural Details',\n            beds: 2,\n            baths: 2,\n            likes: 10,\n            broker: {\n                id: 2,\n                name: \"Michael Jones\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/michael_jones.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house11wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house11sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 11,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$495,000',\n            title: 'Modern Elegance',\n            beds: 2,\n            baths: 2,\n            likes: 16,\n            broker: {\n                id: 3,\n                name: \"Jonathan Bradley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jonathan_bradley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house13wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house13sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 12,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$625,000',\n            title: 'Stunning Colonial',\n            beds: 4,\n            baths: 2,\n            likes: 9,\n            broker: {\n                id: 4,\n                name: \"Jennifer Wu\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jennifer_wu.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house06wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house06sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 13,\n            city: 'Cambridge',\n            state: 'MA',\n            zip: '02420',\n            price: '$430,000',\n            title: 'Quiet Retreat',\n            beds: 5,\n            baths:4,\n            likes: 18,\n            broker: {\n                id: 5,\n                name: \"Olivia Green\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/olivia_green.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house04.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house04sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 14,\n            city: 'Cambridge',\n            state: 'MA',\n            zip: '01742',\n            price: '$450,000',\n            title: 'Victorian Revival',\n            beds: 4,\n            baths:3,\n            sqft: 3800,\n            likes: 10,\n            broker: {\n                id: 6,\n                name: \"Miriam Aupont\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/miriam_aupont.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house01wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house01sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        }\n    ];"
fp.fact(Write2(BitVecVal(1276,obj),BitVecVal(1277,var), BitVecVal(1275,lineNum)))
fp.fact(Heap(BitVecVal(1278,var),BitVecVal(1280,obj)))
fp.fact(Store(BitVecVal(1272,var),BitVecVal(1004,var), BitVecVal(1281,prop), BitVecVal(1275,lineNum)))




hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:16:67"]={"bin":1000, "name":"var PROPERTIES = require('./mock-properties').data;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:20:30"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:33:61"]={"bin":1002, "name":"require('./mock-properties')"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:33:66"]={"bin":1003, "name":"require('./mock-properties').data"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:62:66"]={"bin":1004, "name":"data"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:91:196"]={"bin":1005, "name":"function findAll(req, res, next) {\n    console.log(1);\n    var tmpv0 = PROPERTIES;\n    res.json(tmpv0);\n}"};
hashVar["O_findAll"]={"bin":1006, "name":"O_findAll"};
hashVar["findAll"]={"bin":1007, "name":"findAll"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:108:111"]={"bin":1008, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:113:116"]={"bin":1009, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:118:122"]={"bin":1010, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:130:145"]={"bin":1011, "name":"console.log(1);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:130:137"]={"bin":1012, "name":"console"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:142:143"]={"bin":1016, "name":"1"};
hashVar["0tempHash"]={"bin":1017, "name":"0tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:150:173"]={"bin":1018, "name":"var tmpv0 = PROPERTIES;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:154:159"]={"bin":1019, "name":"tmpv0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:162:172"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:178:194"]={"bin":1020, "name":"res.json(tmpv0);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:178:181"]={"bin":1009, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:187:192"]={"bin":1019, "name":"tmpv0"};
hashVar["1tempHash"]={"bin":1024, "name":"1tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:196:197"]={"bin":1025, "name":";"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:200:393"]={"bin":1026, "name":"function findById(req, res, next) {\n    var temp4 = req.params;\n    var idd2 = temp4.id;\n    var temp5 = idd2-1;\n    var temp6 = PROPERTIES[temp5];\n    var tmpv1 = temp6;\n    res.json(tmpv1);\n}"};
hashVar["O_findById"]={"bin":1027, "name":"O_findById"};
hashVar["findById"]={"bin":1028, "name":"findById"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:218:221"]={"bin":1029, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:223:226"]={"bin":1030, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:228:232"]={"bin":1031, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:240:263"]={"bin":1032, "name":"var temp4 = req.params;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:244:249"]={"bin":1033, "name":"temp4"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:252:255"]={"bin":1029, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:252:262"]={"bin":1034, "name":"req.params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:256:262"]={"bin":1035, "name":"params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:268:288"]={"bin":1036, "name":"var idd2 = temp4.id;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:272:276"]={"bin":1037, "name":"idd2"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:279:284"]={"bin":1033, "name":"temp4"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:279:287"]={"bin":1038, "name":"temp4.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:285:287"]={"bin":1039, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:293:312"]={"bin":1040, "name":"var temp5 = idd2-1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:297:302"]={"bin":1041, "name":"temp5"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:305:309"]={"bin":1037, "name":"idd2"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:317:347"]={"bin":1046, "name":"var temp6 = PROPERTIES[temp5];"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:321:326"]={"bin":1047, "name":"temp6"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:329:339"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:329:346"]={"bin":1048, "name":"PROPERTIES[temp5]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:340:345"]={"bin":1041, "name":"temp5"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:352:370"]={"bin":1049, "name":"var tmpv1 = temp6;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:356:361"]={"bin":1050, "name":"tmpv1"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:364:369"]={"bin":1047, "name":"temp6"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:375:391"]={"bin":1051, "name":"res.json(tmpv1);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:375:378"]={"bin":1030, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:384:389"]={"bin":1050, "name":"tmpv1"};
hashVar["3tempHash"]={"bin":1055, "name":"3tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:423:600"]={"bin":1056, "name":"function findById(req, res, next) {\n     var tmpv13 = req.params;\n     var id = tmpv13.id;\n     var tmpv10 = id - 1;\n     var tmpv2 = PROPERTIES[tmpv10];\n     res.json(tmpv2);\n}"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:441:444"]={"bin":1057, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:446:449"]={"bin":1058, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:451:455"]={"bin":1059, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:464:488"]={"bin":1060, "name":"var tmpv13 = req.params;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:468:474"]={"bin":1061, "name":"tmpv13"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:477:480"]={"bin":1057, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:477:487"]={"bin":1062, "name":"req.params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:481:487"]={"bin":1063, "name":"params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:494:513"]={"bin":1064, "name":"var id = tmpv13.id;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:498:500"]={"bin":1065, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:503:509"]={"bin":1061, "name":"tmpv13"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:503:512"]={"bin":1066, "name":"tmpv13.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:510:512"]={"bin":1067, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:519:539"]={"bin":1068, "name":"var tmpv10 = id - 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:523:529"]={"bin":1069, "name":"tmpv10"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:532:534"]={"bin":1065, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:545:576"]={"bin":1074, "name":"var tmpv2 = PROPERTIES[tmpv10];"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:549:554"]={"bin":1075, "name":"tmpv2"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:557:567"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:557:575"]={"bin":1076, "name":"PROPERTIES[tmpv10]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:568:574"]={"bin":1069, "name":"tmpv10"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:582:598"]={"bin":1077, "name":"res.json(tmpv2);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:582:585"]={"bin":1058, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:591:596"]={"bin":1075, "name":"tmpv2"};
hashVar["5tempHash"]={"bin":1081, "name":"5tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:604:693"]={"bin":1082, "name":"function getFavorites(req, res, next) {\n    var tmpv3 = favorites;\n    res.json(tmpv3);\n}"};
hashVar["O_getFavorites"]={"bin":1083, "name":"O_getFavorites"};
hashVar["getFavorites"]={"bin":1084, "name":"getFavorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:626:629"]={"bin":1085, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:631:634"]={"bin":1086, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:636:640"]={"bin":1087, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:648:670"]={"bin":1088, "name":"var tmpv3 = favorites;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:652:657"]={"bin":1089, "name":"tmpv3"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:660:669"]={"bin":1090, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:675:691"]={"bin":1091, "name":"res.json(tmpv3);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:675:678"]={"bin":1086, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:684:689"]={"bin":1089, "name":"tmpv3"};
hashVar["6tempHash"]={"bin":1095, "name":"6tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:695:1056"]={"bin":1096, "name":"function favorite(req, res, next) {\n    var property = req.body;\n    var exists = false;\n    for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }\n    }\n    if (!exists) var tmpv4 = property;\n    favorites.push(tmpv4);\n    var tmpv5 = \"success\";\n    res.send(tmpv5)\n}"};
hashVar["O_favorite"]={"bin":1097, "name":"O_favorite"};
hashVar["favorite"]={"bin":1098, "name":"favorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:713:716"]={"bin":1099, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:718:721"]={"bin":1100, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:723:727"]={"bin":1101, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:735:759"]={"bin":1102, "name":"var property = req.body;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:739:747"]={"bin":1103, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:750:753"]={"bin":1099, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:750:758"]={"bin":1104, "name":"req.body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:754:758"]={"bin":1105, "name":"body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:764:783"]={"bin":1106, "name":"var exists = false;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:768:774"]={"bin":1107, "name":"exists"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:788:941"]={"bin":1112, "name":"for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }\n    }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:793:802"]={"bin":1113, "name":"var i = 0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:804:824"]={"bin":1114, "name":"i < favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:826:829"]={"bin":1115, "name":"i++"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:797:798"]={"bin":1116, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:804:805"]={"bin":1116, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:808:817"]={"bin":1121, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:808:824"]={"bin":1122, "name":"favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:818:824"]={"bin":1123, "name":"length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:826:827"]={"bin":1116, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:841:935"]={"bin":1124, "name":"if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:845:876"]={"bin":1125, "name":"favorites[i].id === property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:845:854"]={"bin":1126, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:845:857"]={"bin":1127, "name":"favorites[i]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:855:856"]={"bin":1116, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:865:873"]={"bin":1103, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:865:876"]={"bin":1128, "name":"property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:874:876"]={"bin":1129, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:892:906"]={"bin":1130, "name":"exists = true;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:892:898"]={"bin":1107, "name":"exists"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:919:925"]={"bin":1135, "name":"break;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:946:980"]={"bin":1136, "name":"if (!exists) var tmpv4 = property;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:950:957"]={"bin":1137, "name":"!exists"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:959:980"]={"bin":1138, "name":"var tmpv4 = property;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:963:968"]={"bin":1139, "name":"tmpv4"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:971:979"]={"bin":1103, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:985:1007"]={"bin":1140, "name":"favorites.push(tmpv4);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:985:994"]={"bin":1141, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1000:1005"]={"bin":1139, "name":"tmpv4"};
hashVar["10tempHash"]={"bin":1145, "name":"10tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1012:1034"]={"bin":1146, "name":"var tmpv5 = \"success\";"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1016:1021"]={"bin":1147, "name":"tmpv5"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1039:1054"]={"bin":1152, "name":"res.send(tmpv5)"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1039:1042"]={"bin":1100, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1048:1053"]={"bin":1147, "name":"tmpv5"};
hashVar["12tempHash"]={"bin":1156, "name":"12tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1058:1385"]={"bin":1157, "name":"function unfavorite(req, res, next) {\n    var tmpv14 = req.params;\nvar id = tmpv14.id;\n    for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }\n    }\n    var tmpv8 = favorites;\nres.json(tmpv8)\n}"};
hashVar["O_unfavorite"]={"bin":1158, "name":"O_unfavorite"};
hashVar["unfavorite"]={"bin":1159, "name":"unfavorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1078:1081"]={"bin":1160, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1083:1086"]={"bin":1161, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1088:1092"]={"bin":1162, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1100:1124"]={"bin":1163, "name":"var tmpv14 = req.params;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1104:1110"]={"bin":1164, "name":"tmpv14"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1113:1116"]={"bin":1160, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1113:1123"]={"bin":1165, "name":"req.params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1117:1123"]={"bin":1166, "name":"params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1125:1144"]={"bin":1167, "name":"var id = tmpv14.id;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1129:1131"]={"bin":1168, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1134:1140"]={"bin":1164, "name":"tmpv14"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1134:1143"]={"bin":1169, "name":"tmpv14.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1141:1143"]={"bin":1170, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1149:1340"]={"bin":1171, "name":"for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }\n    }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1154:1163"]={"bin":1172, "name":"var i = 0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1165:1185"]={"bin":1173, "name":"i < favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1187:1190"]={"bin":1174, "name":"i++"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1158:1159"]={"bin":1175, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1165:1166"]={"bin":1175, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1169:1178"]={"bin":1180, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1169:1185"]={"bin":1181, "name":"favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1179:1185"]={"bin":1182, "name":"length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1187:1188"]={"bin":1175, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1202:1334"]={"bin":1183, "name":"if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1206:1227"]={"bin":1184, "name":"favorites[i].id == id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1206:1215"]={"bin":1185, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1206:1218"]={"bin":1186, "name":"favorites[i]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1216:1217"]={"bin":1175, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1225:1227"]={"bin":1168, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1243:1257"]={"bin":1187, "name":"var tmpv6 = i;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1247:1252"]={"bin":1188, "name":"tmpv6"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1255:1256"]={"bin":1175, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1259:1273"]={"bin":1189, "name":"var tmpv7 = 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1263:1268"]={"bin":1190, "name":"tmpv7"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1274:1305"]={"bin":1195, "name":"favorites.splice(tmpv6, tmpv7);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1274:1283"]={"bin":1196, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1291:1296"]={"bin":1188, "name":"tmpv6"};
hashVar["15tempHash"]={"bin":1200, "name":"15tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1298:1303"]={"bin":1190, "name":"tmpv7"};
hashVar["16tempHash"]={"bin":1204, "name":"16tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1318:1324"]={"bin":1205, "name":"break;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1345:1367"]={"bin":1206, "name":"var tmpv8 = favorites;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1349:1354"]={"bin":1207, "name":"tmpv8"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1357:1366"]={"bin":1208, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1368:1383"]={"bin":1209, "name":"res.json(tmpv8)"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1368:1371"]={"bin":1161, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1377:1382"]={"bin":1207, "name":"tmpv8"};
hashVar["17tempHash"]={"bin":1213, "name":"17tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1387:1600"]={"bin":1214, "name":"function like(req, res, next) {\n    var property = req.body;\n    var tmpv11 = property.id - 1;\nPROPERTIES[tmpv11].likes++;\n    var tmpv12 = property.id - 1;\nvar tmpv9 = PROPERTIES[tmpv12].likes;\nres.json(tmpv9);\n}"};
hashVar["O_like"]={"bin":1215, "name":"O_like"};
hashVar["like"]={"bin":1216, "name":"like"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1401:1404"]={"bin":1217, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1406:1409"]={"bin":1218, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1411:1415"]={"bin":1219, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1423:1447"]={"bin":1220, "name":"var property = req.body;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1427:1435"]={"bin":1221, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1438:1441"]={"bin":1217, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1438:1446"]={"bin":1222, "name":"req.body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1442:1446"]={"bin":1223, "name":"body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1452:1481"]={"bin":1224, "name":"var tmpv11 = property.id - 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1456:1462"]={"bin":1225, "name":"tmpv11"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1465:1473"]={"bin":1221, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1465:1476"]={"bin":1226, "name":"property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1474:1476"]={"bin":1227, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1482:1509"]={"bin":1232, "name":"PROPERTIES[tmpv11].likes++;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1482:1492"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1493:1499"]={"bin":1225, "name":"tmpv11"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1482:1500"]={"bin":1233, "name":"PROPERTIES[tmpv11]"};
hashVar["ttemp0"]={"bin":1234, "name":"ttemp0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1514:1543"]={"bin":1235, "name":"var tmpv12 = property.id - 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1518:1524"]={"bin":1236, "name":"tmpv12"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1527:1535"]={"bin":1221, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1527:1538"]={"bin":1237, "name":"property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1536:1538"]={"bin":1238, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1544:1581"]={"bin":1243, "name":"var tmpv9 = PROPERTIES[tmpv12].likes;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1548:1553"]={"bin":1244, "name":"tmpv9"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1556:1566"]={"bin":1001, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1556:1574"]={"bin":1245, "name":"PROPERTIES[tmpv12]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1567:1573"]={"bin":1236, "name":"tmpv12"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1582:1598"]={"bin":1246, "name":"res.json(tmpv9);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1582:1585"]={"bin":1218, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1591:1596"]={"bin":1244, "name":"tmpv9"};
hashVar["20tempHash"]={"bin":1250, "name":"20tempHash"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1602:1628"]={"bin":1251, "name":"exports.findAll = findAll;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1602:1609"]={"bin":1252, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1610:1617"]={"bin":1253, "name":"findAll"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1620:1627"]={"bin":1254, "name":"findAll"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1629:1657"]={"bin":1255, "name":"exports.findById = findById;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1629:1636"]={"bin":1256, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1637:1645"]={"bin":1257, "name":"findById"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1648:1656"]={"bin":1258, "name":"findById"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1658:1694"]={"bin":1259, "name":"exports.getFavorites = getFavorites;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1658:1665"]={"bin":1260, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1666:1678"]={"bin":1261, "name":"getFavorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1681:1693"]={"bin":1262, "name":"getFavorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1695:1723"]={"bin":1263, "name":"exports.favorite = favorite;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1695:1702"]={"bin":1264, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1703:1711"]={"bin":1265, "name":"favorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1714:1722"]={"bin":1266, "name":"favorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1724:1756"]={"bin":1267, "name":"exports.unfavorite = unfavorite;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1724:1731"]={"bin":1268, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1732:1742"]={"bin":1269, "name":"unfavorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1745:1755"]={"bin":1270, "name":"unfavorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1757:1777"]={"bin":1271, "name":"exports.like = like;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1757:1764"]={"bin":1272, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1765:1769"]={"bin":1273, "name":"like"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1772:1776"]={"bin":1274, "name":"like"};
hashVar["dVXRLg.js:21:11646"]={"bin":1275, "name":"exports.data = [\n        {\n            id: 1,\n            city: 'Boston',\n            state: 'MA',\n            price: '$475,000',\n            title: 'Condominium Redefined',\n            beds: 2,\n            baths: 2,\n            likes: 5,\n            broker: {\n                id: 1,\n                name: \"Caroline Kingsley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/caroline_kingsley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house08wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house08sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 2,\n            city: 'Cambridge',\n            state: 'MA',\n            price: '$1,200,000',\n            title: 'Ultimate Sophistication',\n            beds: 5,\n            baths: 4,\n            likes: 2,\n            broker: {\n                id: 2,\n                name: \"Michael Jones\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/michael_jones.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house02wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house02sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 3,\n            city: 'Boston',\n            state: 'MA',\n            price: '$650,000',\n            title: 'Seaport District Retreat',\n            beds: 3,\n            baths: 2,\n            likes: 6,\n            broker: {\n                id: 3,\n                name: \"Jonathan Bradley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jonathan_bradley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house09wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house09sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 4,\n            city: 'Boston',\n            state: 'MA',\n            price: '$875,000',\n            title: 'Modern City Living',\n            beds: 3,\n            baths: 2,\n            likes: 12,\n            broker: {\n                id: 4,\n                name: \"Jennifer Wu\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jennifer_wu.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house14.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house14sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 5,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$425,000',\n            title: 'Urban Efficiency',\n            beds: 4,\n            baths: 2,\n            likes: 5,\n            broker: {\n                id: 5,\n                name: \"Olivia Green\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/olivia_green.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house03wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house03sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 6,\n            city: 'Boston',\n            state: 'MA',\n            price: '$550,000',\n            title: 'Waterfront in the City',\n            beds: 3,\n            baths: 2,\n            likes: 14,\n            broker: {\n                id: 6,\n                name: \"Miriam Aupont\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/miriam_aupont.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house05wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house05sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 7,\n            city: 'Brookline',\n            state: 'MA',\n            zip: '02420',\n            price: '$850,000',\n            title: 'Suburban Extravaganza',\n            beds: 5,\n            baths: 4,\n            likes: 5,\n            broker: {\n                id: 7,\n                name: \"Michelle Lambert\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/michelle_lambert.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house07wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house07sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 8,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$925,000',\n            title: 'Contemporary Luxury',\n            beds: 6,\n            baths: 6,\n            sqft: 950,\n            likes: 8,\n            broker: {\n                id: 8,\n                name: \"Victor Oachoa\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/victor_ochoa.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house12wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house12sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 9,\n            city: 'Cambridge',\n            state: 'MA',\n            zip: '02420',\n            price: '$550,000',\n            title: 'Heart of Harvard Square',\n            beds: 5,\n            baths: 4,\n            likes: 9,\n            broker: {\n                id: 1,\n                name: \"Caroline Kingsley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/caroline_kingsley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house10.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house10sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 10,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$375,000',\n            title: 'Architectural Details',\n            beds: 2,\n            baths: 2,\n            likes: 10,\n            broker: {\n                id: 2,\n                name: \"Michael Jones\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/michael_jones.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house11wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house11sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 11,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$495,000',\n            title: 'Modern Elegance',\n            beds: 2,\n            baths: 2,\n            likes: 16,\n            broker: {\n                id: 3,\n                name: \"Jonathan Bradley\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jonathan_bradley.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house13wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house13sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 12,\n            city: 'Boston',\n            state: 'MA',\n            zip: '02420',\n            price: '$625,000',\n            title: 'Stunning Colonial',\n            beds: 4,\n            baths: 2,\n            likes: 9,\n            broker: {\n                id: 4,\n                name: \"Jennifer Wu\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/jennifer_wu.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house06wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house06sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 13,\n            city: 'Cambridge',\n            state: 'MA',\n            zip: '02420',\n            price: '$430,000',\n            title: 'Quiet Retreat',\n            beds: 5,\n            baths:4,\n            likes: 18,\n            broker: {\n                id: 5,\n                name: \"Olivia Green\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/olivia_green.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house04.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house04sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        },\n        {\n            id: 14,\n            city: 'Cambridge',\n            state: 'MA',\n            zip: '01742',\n            price: '$450,000',\n            title: 'Victorian Revival',\n            beds: 4,\n            baths:3,\n            sqft: 3800,\n            likes: 10,\n            broker: {\n                id: 6,\n                name: \"Miriam Aupont\",\n                title: \"Senior Broker\",\n                picture: \"https://s3-us-west-1.amazonaws.com/sfdc-demo/people/miriam_aupont.jpg\"\n            },\n            pic: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house01wide.jpg',\n            thumb: 'https://s3-us-west-1.amazonaws.com/sfdc-demo/realty/house01sq.jpg',\n            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad.'\n        }\n    ];"};
hashVar["dVXRLg.js:21:28"]={"bin":1276, "name":"exports"};
hashVar["dVXRLg.js:29:33"]={"bin":1277, "name":"data"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:16:67"]["name"]="var PROPERTIES = require('dVXRLg').data;";
code[hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:16:67"]["bin"]]="var PROPERTIES = require('dVXRLg').data;";
fp.fact(datadep(BitVecVal(hashVar["dVXRLg.js:21:11646"]["bin"],lineNum),BitVecVal(hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:16:67"]["bin"],lineNum)))
boundToExtractFunction = 1274;
fp.fact(refs(BitVecVal(hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:130:145"]["bin"],lineNum),BitVecVal(9114157,val)))
fp.fact(ref(BitVecVal(hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:154:159"]["bin"],var),BitVecVal(1717943,val)))
#sql statements

exitLine = Const('exit', lineNum)
fp.declare_var(exitLine)

fp.query(unMarshal(line2, v1, 9114157))
v_ex = fp.get_answer()
unmarshal_stmt = v_ex.arg(1).arg(1).as_long()
unmarshal_stmt_start = get_key(unmarshal_stmt).split(":")[1]
print colored("*********** Constraint Solving Started::::",'magenta')
print colored( "unMarshal***********",'blue'), unmarshal_stmt, unmarshal_stmt_start
#
#
fp.query(Marshal(line2, v1, 1717943))
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

fp.query(ExecutedStmts(exitLine, 12313, 9114157, 1717943))
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

for sql in sqlstmts:
    print colored("//sql stmts "+ "\n" + sql , 'cyan')

print colored("Extracting Functions DONE!***********  \n See generated JS files in results folder, abcDe.js is entry",'magenta')

