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

Executed    = Function('Executed',lineNum, uid, mval, val, BoolSort()) #; call-dep (variable variable) #(declare-rel call-dep (var var))
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
fp.register_relation(Executed)
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
fp.rule(Read1(v2,line1),[Calls(o1,line1),Formal(v1,i1, o1),Actual(line1,i1, v2)])


fp.register_relation(Write1,Calls,Formal,Actual)
fp.declare_var(v1,v2,line1,o1,i1,v2)
fp.rule(Write1(v1,line1),[Calls(o1,line1),Formal(v1,i1, o1),Actual(line1,i1, v2)])

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

fp.register_relation(Executed,datadep,unMarshal, Marshal)
fp.declare_var(line1,line2,line3, v1,val1,uid1, val2, v2)
# fp.query(datadep(BitVecVal(1, lineNum),exitLine), Not(datadep(BitVecVal(3, lineNum),exitLine)))

fp.rule(Executed(line1, uid1, val1, val2),
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

# fp.rule(Executed(line1, uid1, val1, val2),
#         [
#              datadep(line2,line1), unMarshal(line2, v1, val1),
#              Not(datadep(line3,line1)), Marshal(line3, v2, val2)
#         ])

#fp.rule(Assign(v2,v1,line1),[Calls(o1,line1),MethodRet(o1,v1),CallRet(line1,v2)])


#fp.rule(Executed(line1, uid1),[datadep(line2,line1), unMarshal(line2, v1, val1)])

# fp.register_relation(Marshal,Read1,ref)
# fp.declare_var(line1,v1,val1)
#fp.rule(Marshal(line1, v1, val1),[Read1(v1,line1),ref(v1, val1)])

#code[11742563]="var id = TempV1.id;"
#fp.fact(Write1(BitVecVal(20,obj),BitVecVal(11742563,lineNum)))
#fp.fact(Read2(BitVecVal(18,obj),BitVecVal(20,var),BitVecVal(11742563,lineNum)))
#fp.fact(Load(BitVecVal(20,var),BitVecVal(18,prop), BitVecVal(20,var),BitVecVal(11742563,lineNum)))
#fp.fact(Stmt(BitVecVal(11742563,lineNum),BitVecVal(16,obj)))
#VariableDecl: var TempV0 = speakers[id];
#code[3498392]="var TempV0 = speakers[id];"
#fp.fact(Read2(BitVecVal(2,obj),BitVecVal(20,var),BitVecVal(3498392,lineNum)))
#fp.fact(Load(BitVecVal(21,var),BitVecVal(2,prop), BitVecVal(20,var),BitVecVal(3498392,lineNum)))
#fp.fact(Stmt(BitVecVal(3498392,lineNum),BitVecVal(16,obj)))

fp.register_relation(datadep,Load,Read2)
fp.declare_var(line1,line2,v1,v2,o1,f1)
fp.rule(datadep(line1,line2),[Load(v1,f1,v2,line1),Read2(o1,v1,line2)])

fp.register_relation(datadep,Write1,Read2)
fp.declare_var(line1,line2,v1,f1)
fp.rule(datadep(line1,line2),[Write1(v1,line1),Read2(v1,f1,line2)])


'''
    code[11390510]="var TempV1 = id - 1;"
    fp.fact(Read1(BitVecVal(16,var),BitVecVal(11390510,lineNum)))
    fp.fact(Assign(BitVecVal(17,var),BitVecVal(16,obj),BitVecVal(11390510,lineNum)))
    fp.fact(Heap(BitVecVal(25,var),BitVecVal(26,obj)))
    fp.fact(Assign(BitVecVal(17,var),BitVecVal(25,obj),BitVecVal(11390510,lineNum)))
    fp.fact(Stmt(BitVecVal(11390510,lineNum),BitVecVal(12,obj)))
    #1111VariableDecl: var TempV0 = BROKERS[TempV1]; 17: TempV1
    code[10199495]="var TempV0 = BROKERS[TempV1];"
    fp.fact(Read2(BitVecVal(2,obj),BitVecVal(17,var),BitVecVal(10199495,lineNum)))
    fp.fact(Load(BitVecVal(27,var),BitVecVal(2,prop), BitVecVal(17,var),BitVecVal(10199495,lineNum)))
    fp.fact(Stmt(BitVecVal(10199495,lineNum),BitVecVal(12,obj)))
    '''

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


# fp.register_relation(controldep,controldep)
# fp.declare_var(line1,line2)
# fp.rule(controldep(line1,line2),controldep(line2,line1))
# fp.fact(Actual(BitVecVal(14817998,lineNum), BitVecVal(0,num), BitVecVal(9,var)))
# fp.fact(FuncDecl(BitVecVal(9,var),BitVecVal(8,obj),BitVecVal(10908367,lineNum)))




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

#VariableDecl: var dummyvar;
code[1000]="var dummyvar;"
#VariableDecl: var PROPERTIES = require('./mock-properties').data;
code[1001]="var PROPERTIES = require('./mock-properties').data;"
fp.fact(Write1(BitVecVal(1002,var),BitVecVal(1001,lineNum)))
fp.fact(Read2(BitVecVal(1003,var), BitVecVal(1005,prop), BitVecVal(1001,lineNum)))
fp.fact(Load(BitVecVal(1002,var),BitVecVal(1003,var), BitVecVal(1004,prop),BitVecVal(1001,lineNum)))
#functionDeclaration: findAll
code[1006]="function findAll(req, res, next) {\n    var tmpv0 = PROPERTIES;\n    res.json(tmpv0);\n}"
fp.fact(FuncDecl(BitVecVal(1007,var),BitVecVal(1008,obj),BitVecVal(1006,lineNum)))
fp.fact(Formal(BitVecVal(1008,obj),BitVecVal(1009,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1008,obj),BitVecVal(1010,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1008,obj),BitVecVal(1011,obj),BitVecVal(3,obj)))
#VariableDecl: var tmpv0 = PROPERTIES;
code[1012]="var tmpv0 = PROPERTIES;"
fp.fact(Write1(BitVecVal(1013,var),BitVecVal(1012,lineNum)))
fp.fact(Read1(BitVecVal(1014,var),BitVecVal(1012,lineNum)))
fp.fact(Assign(BitVecVal(1013,var),BitVecVal(1002,obj),BitVecVal(1012,lineNum)))
#CallExpression: res.json(tmpv0);
code[1014]="res.json(tmpv0);"
#functionDeclaration: findById
code[1016]="function findById(req, res, next) {\n    var temp4 = req.params;\n    var idd2 = temp4.id;\n    var temp5 = idd2-1;\n    var temp6 = PROPERTIES[temp5];\n    var tmpv1 = temp6;\n    res.json(tmpv1);\n}"
fp.fact(FuncDecl(BitVecVal(1017,var),BitVecVal(1018,obj),BitVecVal(1016,lineNum)))
fp.fact(Formal(BitVecVal(1018,obj),BitVecVal(1019,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1018,obj),BitVecVal(1020,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1018,obj),BitVecVal(1021,obj),BitVecVal(3,obj)))
#VariableDecl: var temp4 = req.params;
code[1022]="var temp4 = req.params;"
fp.fact(Write1(BitVecVal(1023,var),BitVecVal(1022,lineNum)))
fp.fact(Read2(BitVecVal(1019,var), BitVecVal(1025,prop), BitVecVal(1022,lineNum)))
fp.fact(Load(BitVecVal(1023,var),BitVecVal(1019,var), BitVecVal(1024,prop),BitVecVal(1022,lineNum)))
#VariableDecl: var idd2 = temp4.id;
code[1026]="var idd2 = temp4.id;"
fp.fact(Write1(BitVecVal(1027,var),BitVecVal(1026,lineNum)))
fp.fact(Read2(BitVecVal(1023,var), BitVecVal(1029,prop), BitVecVal(1026,lineNum)))
fp.fact(Load(BitVecVal(1027,var),BitVecVal(1023,var), BitVecVal(1028,prop),BitVecVal(1026,lineNum)))
#VariableDecl: var temp5 = idd2-1;
code[1030]="var temp5 = idd2-1;"
fp.fact(Write1(BitVecVal(1031,var),BitVecVal(1030,lineNum)))
fp.fact(Write1(BitVecVal(1031,var),BitVecVal(1030,lineNum)))
fp.fact(Read1(BitVecVal(1032,var),BitVecVal(1030,lineNum)))
fp.fact(Assign(BitVecVal(1031,var),BitVecVal(1027,obj),BitVecVal(1030,lineNum)))
fp.fact(Write1(BitVecVal(1031,var),BitVecVal(1030,lineNum)))
fp.fact(Heap(BitVecVal(1032,var),BitVecVal(1034,obj)))
fp.fact(Assign(BitVecVal(1031,var),BitVecVal(1035,obj),BitVecVal(1030,lineNum)))
#VariableDecl: var temp6 = PROPERTIES[temp5];
code[1036]="var temp6 = PROPERTIES[temp5];"
fp.fact(Write1(BitVecVal(1037,var),BitVecVal(1036,lineNum)))
fp.fact(Read2(BitVecVal(1002,var), BitVecVal(1031,prop), BitVecVal(1036,lineNum)))
fp.fact(Load(BitVecVal(1037,var),BitVecVal(1002,var), BitVecVal(1038,prop),BitVecVal(1036,lineNum)))
#VariableDecl: var tmpv1 = temp6;
code[1039]="var tmpv1 = temp6;"
fp.fact(Write1(BitVecVal(1040,var),BitVecVal(1039,lineNum)))
fp.fact(Read1(BitVecVal(1041,var),BitVecVal(1039,lineNum)))
fp.fact(Assign(BitVecVal(1040,var),BitVecVal(1037,obj),BitVecVal(1039,lineNum)))
#CallExpression: res.json(tmpv1);
code[1041]="res.json(tmpv1);"
#functionDeclaration: findById
code[1042]="function findById(req, res, next) {\n     var tmpv13 = req.params;\n     var id = tmpv13.id;\n     var tmpv10 = id - 1;\n     var tmpv2 = PROPERTIES[tmpv10];\n     res.json(tmpv2);\n}"
fp.fact(FuncDecl(BitVecVal(1017,var),BitVecVal(1018,obj),BitVecVal(1042,lineNum)))
fp.fact(Formal(BitVecVal(1018,obj),BitVecVal(1043,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1018,obj),BitVecVal(1044,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1018,obj),BitVecVal(1045,obj),BitVecVal(3,obj)))
#VariableDecl: var tmpv13 = req.params;
code[1046]="var tmpv13 = req.params;"
fp.fact(Write1(BitVecVal(1047,var),BitVecVal(1046,lineNum)))
fp.fact(Read2(BitVecVal(1043,var), BitVecVal(1049,prop), BitVecVal(1046,lineNum)))
fp.fact(Load(BitVecVal(1047,var),BitVecVal(1043,var), BitVecVal(1048,prop),BitVecVal(1046,lineNum)))
#VariableDecl: var id = tmpv13.id;
code[1050]="var id = tmpv13.id;"
fp.fact(Write1(BitVecVal(1051,var),BitVecVal(1050,lineNum)))
fp.fact(Read2(BitVecVal(1047,var), BitVecVal(1053,prop), BitVecVal(1050,lineNum)))
fp.fact(Load(BitVecVal(1051,var),BitVecVal(1047,var), BitVecVal(1052,prop),BitVecVal(1050,lineNum)))
#VariableDecl: var tmpv10 = id - 1;
code[1054]="var tmpv10 = id - 1;"
fp.fact(Write1(BitVecVal(1055,var),BitVecVal(1054,lineNum)))
fp.fact(Write1(BitVecVal(1055,var),BitVecVal(1054,lineNum)))
fp.fact(Read1(BitVecVal(1056,var),BitVecVal(1054,lineNum)))
fp.fact(Assign(BitVecVal(1055,var),BitVecVal(1051,obj),BitVecVal(1054,lineNum)))
fp.fact(Write1(BitVecVal(1055,var),BitVecVal(1054,lineNum)))
fp.fact(Heap(BitVecVal(1056,var),BitVecVal(1058,obj)))
fp.fact(Assign(BitVecVal(1055,var),BitVecVal(1059,obj),BitVecVal(1054,lineNum)))
#VariableDecl: var tmpv2 = PROPERTIES[tmpv10];
code[1060]="var tmpv2 = PROPERTIES[tmpv10];"
fp.fact(Write1(BitVecVal(1061,var),BitVecVal(1060,lineNum)))
fp.fact(Read2(BitVecVal(1002,var), BitVecVal(1055,prop), BitVecVal(1060,lineNum)))
fp.fact(Load(BitVecVal(1061,var),BitVecVal(1002,var), BitVecVal(1062,prop),BitVecVal(1060,lineNum)))
#CallExpression: res.json(tmpv2);
code[1063]="res.json(tmpv2);"
#functionDeclaration: getFavorites
code[1064]="function getFavorites(req, res, next) {\n    var tmpv3 = favorites;\n    res.json(tmpv3);\n}"
fp.fact(FuncDecl(BitVecVal(1065,var),BitVecVal(1066,obj),BitVecVal(1064,lineNum)))
fp.fact(Formal(BitVecVal(1066,obj),BitVecVal(1067,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1066,obj),BitVecVal(1068,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1066,obj),BitVecVal(1069,obj),BitVecVal(3,obj)))
#VariableDecl: var tmpv3 = favorites;
code[1070]="var tmpv3 = favorites;"
fp.fact(Write1(BitVecVal(1071,var),BitVecVal(1070,lineNum)))
fp.fact(Read1(BitVecVal(1072,var),BitVecVal(1070,lineNum)))
fp.fact(Assign(BitVecVal(1071,var),BitVecVal(1072,obj),BitVecVal(1070,lineNum)))
#CallExpression: res.json(tmpv3);
code[1073]="res.json(tmpv3);"
#functionDeclaration: favorite
code[1074]="function favorite(req, res, next) {\n    var property = req.body;\n    var exists = false;\n    for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }\n    }\n    if (!exists) var tmpv4 = property;\n    favorites.push(tmpv4);\n    var tmpv5 = \"success\";\n    res.send(tmpv5)\n}"
fp.fact(FuncDecl(BitVecVal(1075,var),BitVecVal(1076,obj),BitVecVal(1074,lineNum)))
fp.fact(Formal(BitVecVal(1076,obj),BitVecVal(1077,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1076,obj),BitVecVal(1078,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1076,obj),BitVecVal(1079,obj),BitVecVal(3,obj)))
#VariableDecl: var property = req.body;
code[1080]="var property = req.body;"
fp.fact(Write1(BitVecVal(1081,var),BitVecVal(1080,lineNum)))
fp.fact(Read2(BitVecVal(1077,var), BitVecVal(1083,prop), BitVecVal(1080,lineNum)))
fp.fact(Load(BitVecVal(1081,var),BitVecVal(1077,var), BitVecVal(1082,prop),BitVecVal(1080,lineNum)))
#VariableDecl: var exists = false;
code[1084]="var exists = false;"
fp.fact(Write1(BitVecVal(1085,var),BitVecVal(1084,lineNum)))
fp.fact(Heap(BitVecVal(1086,var),BitVecVal(1088,obj)))
fp.fact(Assign(BitVecVal(1085,var),BitVecVal(1089,obj),BitVecVal(1084,lineNum)))
code[1090]="for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }\n    }"
fp.fact(controldep(BitVecVal(1091,lineNum),BitVecVal(1090,lineNum)))
fp.fact(controldep(BitVecVal(1092,lineNum),BitVecVal(1090,lineNum)))
fp.fact(controldep(BitVecVal(1093,lineNum),BitVecVal(1090,lineNum)))
#VariableDecl: var i = 0
code[1091]="var i = 0"
fp.fact(Write1(BitVecVal(1094,var),BitVecVal(1091,lineNum)))
fp.fact(Heap(BitVecVal(1095,var),BitVecVal(1097,obj)))
fp.fact(Assign(BitVecVal(1094,var),BitVecVal(1098,obj),BitVecVal(1091,lineNum)))
#BinaryExpression: i < favorites.length
code[1092]="i < favorites.length"
fp.fact(Read1(BitVecVal(1099,var),BitVecVal(1092,lineNum)))
fp.fact(Assign(BitVecVal(0,var),BitVecVal(1094,obj),BitVecVal(1092,lineNum)))
fp.fact(Read2(BitVecVal(1099,var), BitVecVal(1101,prop), BitVecVal(1092,lineNum)))
fp.fact(Load(BitVecVal(0,var),BitVecVal(1099,var), BitVecVal(1100,prop),BitVecVal(1092,lineNum)))
#UpdateExpression: i++
code[1093]="i++"
fp.fact(Write1(BitVecVal(1094,var),BitVecVal(1093,lineNum)))
fp.fact(Read1(BitVecVal(1102,var),BitVecVal(1093,lineNum)))
fp.fact(Assign(BitVecVal(1094,var),BitVecVal(1094,obj),BitVecVal(1093,lineNum)))
code[1102]="if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }"
fp.fact(controldep(BitVecVal(1103,lineNum),BitVecVal(1102,lineNum)))
#BinaryExpression: favorites[i].id === property.id
code[1103]="favorites[i].id === property.id"
fp.fact(Read2(BitVecVal(1104,var), BitVecVal(1094,prop), BitVecVal(1103,lineNum)))
fp.fact(Load(BitVecVal(0,var),BitVecVal(1104,var), BitVecVal(1105,prop),BitVecVal(1103,lineNum)))
fp.fact(Read2(BitVecVal(1081,var), BitVecVal(1107,prop), BitVecVal(1103,lineNum)))
fp.fact(Load(BitVecVal(0,var),BitVecVal(1081,var), BitVecVal(1106,prop),BitVecVal(1103,lineNum)))
#Assignment: exists = true;"
code[1108]="exists = true;"
fp.fact(Write1(BitVecVal(1085,var),BitVecVal(1108,lineNum)))
fp.fact(Heap(BitVecVal(1109,var),BitVecVal(1111,obj)))
fp.fact(Assign(BitVecVal(1085,var),BitVecVal(1112,obj),BitVecVal(1108,lineNum)))
code[1114]="if (!exists) var tmpv4 = property;"
fp.fact(controldep(BitVecVal(1115,lineNum),BitVecVal(1114,lineNum)))
#VariableDecl: var tmpv4 = property;
code[1116]="var tmpv4 = property;"
fp.fact(Write1(BitVecVal(1117,var),BitVecVal(1116,lineNum)))
fp.fact(Read1(BitVecVal(1118,var),BitVecVal(1116,lineNum)))
fp.fact(Assign(BitVecVal(1117,var),BitVecVal(1081,obj),BitVecVal(1116,lineNum)))
#CallExpression: favorites.push(tmpv4);
code[1118]="favorites.push(tmpv4);"
#VariableDecl: var tmpv5 = \"success\";
code[1119]="var tmpv5 = \"success\";"
fp.fact(Write1(BitVecVal(1120,var),BitVecVal(1119,lineNum)))
fp.fact(Heap(BitVecVal(1121,var),BitVecVal(1123,obj)))
fp.fact(Assign(BitVecVal(1120,var),BitVecVal(1124,obj),BitVecVal(1119,lineNum)))
#CallExpression: res.send(tmpv5)
code[1125]="res.send(tmpv5)"
#functionDeclaration: unfavorite
code[1126]="function unfavorite(req, res, next) {\n    var tmpv14 = req.params;\nvar id = tmpv14.id;\n    for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }\n    }\n    var tmpv8 = favorites;\nres.json(tmpv8)\n}"
fp.fact(FuncDecl(BitVecVal(1127,var),BitVecVal(1128,obj),BitVecVal(1126,lineNum)))
fp.fact(Formal(BitVecVal(1128,obj),BitVecVal(1129,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1128,obj),BitVecVal(1130,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1128,obj),BitVecVal(1131,obj),BitVecVal(3,obj)))
#VariableDecl: var tmpv14 = req.params;
code[1132]="var tmpv14 = req.params;"
fp.fact(Write1(BitVecVal(1133,var),BitVecVal(1132,lineNum)))
fp.fact(Read2(BitVecVal(1129,var), BitVecVal(1135,prop), BitVecVal(1132,lineNum)))
fp.fact(Load(BitVecVal(1133,var),BitVecVal(1129,var), BitVecVal(1134,prop),BitVecVal(1132,lineNum)))
#VariableDecl: var id = tmpv14.id;
code[1136]="var id = tmpv14.id;"
fp.fact(Write1(BitVecVal(1137,var),BitVecVal(1136,lineNum)))
fp.fact(Read2(BitVecVal(1133,var), BitVecVal(1139,prop), BitVecVal(1136,lineNum)))
fp.fact(Load(BitVecVal(1137,var),BitVecVal(1133,var), BitVecVal(1138,prop),BitVecVal(1136,lineNum)))
code[1140]="for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }\n    }"
fp.fact(controldep(BitVecVal(1141,lineNum),BitVecVal(1140,lineNum)))
fp.fact(controldep(BitVecVal(1142,lineNum),BitVecVal(1140,lineNum)))
fp.fact(controldep(BitVecVal(1143,lineNum),BitVecVal(1140,lineNum)))
#VariableDecl: var i = 0
code[1141]="var i = 0"
fp.fact(Write1(BitVecVal(1144,var),BitVecVal(1141,lineNum)))
fp.fact(Heap(BitVecVal(1145,var),BitVecVal(1147,obj)))
fp.fact(Assign(BitVecVal(1144,var),BitVecVal(1148,obj),BitVecVal(1141,lineNum)))
#BinaryExpression: i < favorites.length
code[1142]="i < favorites.length"
fp.fact(Read1(BitVecVal(1149,var),BitVecVal(1142,lineNum)))
fp.fact(Assign(BitVecVal(0,var),BitVecVal(1144,obj),BitVecVal(1142,lineNum)))
fp.fact(Read2(BitVecVal(1149,var), BitVecVal(1151,prop), BitVecVal(1142,lineNum)))
fp.fact(Load(BitVecVal(0,var),BitVecVal(1149,var), BitVecVal(1150,prop),BitVecVal(1142,lineNum)))
#UpdateExpression: i++
code[1143]="i++"
fp.fact(Write1(BitVecVal(1144,var),BitVecVal(1143,lineNum)))
fp.fact(Read1(BitVecVal(1152,var),BitVecVal(1143,lineNum)))
fp.fact(Assign(BitVecVal(1144,var),BitVecVal(1144,obj),BitVecVal(1143,lineNum)))
code[1152]="if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }"
fp.fact(controldep(BitVecVal(1153,lineNum),BitVecVal(1152,lineNum)))
#BinaryExpression: favorites[i].id == id
code[1153]="favorites[i].id == id"
fp.fact(Read2(BitVecVal(1154,var), BitVecVal(1144,prop), BitVecVal(1153,lineNum)))
fp.fact(Load(BitVecVal(0,var),BitVecVal(1154,var), BitVecVal(1155,prop),BitVecVal(1153,lineNum)))
fp.fact(Read1(BitVecVal(1156,var),BitVecVal(1153,lineNum)))
fp.fact(Assign(BitVecVal(0,var),BitVecVal(1137,obj),BitVecVal(1153,lineNum)))
#VariableDecl: var tmpv6 = i;
code[1156]="var tmpv6 = i;"
fp.fact(Write1(BitVecVal(1157,var),BitVecVal(1156,lineNum)))
fp.fact(Read1(BitVecVal(1158,var),BitVecVal(1156,lineNum)))
fp.fact(Assign(BitVecVal(1157,var),BitVecVal(1144,obj),BitVecVal(1156,lineNum)))
#VariableDecl: var tmpv7 = 1;
code[1158]="var tmpv7 = 1;"
fp.fact(Write1(BitVecVal(1159,var),BitVecVal(1158,lineNum)))
fp.fact(Heap(BitVecVal(1160,var),BitVecVal(1162,obj)))
fp.fact(Assign(BitVecVal(1159,var),BitVecVal(1163,obj),BitVecVal(1158,lineNum)))
#CallExpression: favorites.splice(tmpv6, tmpv7);
code[1164]="favorites.splice(tmpv6, tmpv7);"
#VariableDecl: var tmpv8 = favorites;
code[1166]="var tmpv8 = favorites;"
fp.fact(Write1(BitVecVal(1167,var),BitVecVal(1166,lineNum)))
fp.fact(Read1(BitVecVal(1168,var),BitVecVal(1166,lineNum)))
fp.fact(Assign(BitVecVal(1167,var),BitVecVal(1168,obj),BitVecVal(1166,lineNum)))
#CallExpression: res.json(tmpv8)
code[1169]="res.json(tmpv8)"
#functionDeclaration: like
code[1170]="function like(req, res, next) {\n    var property = req.body;\n    var tmpv11 = property.id - 1;\nPROPERTIES[tmpv11].likes++;\n    var tmpv12 = property.id - 1;\nvar tmpv9 = PROPERTIES[tmpv12].likes;\nres.json(tmpv9);\n}"
fp.fact(FuncDecl(BitVecVal(1171,var),BitVecVal(1172,obj),BitVecVal(1170,lineNum)))
fp.fact(Formal(BitVecVal(1172,obj),BitVecVal(1173,obj),BitVecVal(1,obj)))
fp.fact(Formal(BitVecVal(1172,obj),BitVecVal(1174,obj),BitVecVal(2,obj)))
fp.fact(Formal(BitVecVal(1172,obj),BitVecVal(1175,obj),BitVecVal(3,obj)))
#VariableDecl: var property = req.body;
code[1176]="var property = req.body;"
fp.fact(Write1(BitVecVal(1177,var),BitVecVal(1176,lineNum)))
fp.fact(Read2(BitVecVal(1173,var), BitVecVal(1179,prop), BitVecVal(1176,lineNum)))
fp.fact(Load(BitVecVal(1177,var),BitVecVal(1173,var), BitVecVal(1178,prop),BitVecVal(1176,lineNum)))
#VariableDecl: var tmpv11 = property.id - 1;
code[1180]="var tmpv11 = property.id - 1;"
fp.fact(Write1(BitVecVal(1181,var),BitVecVal(1180,lineNum)))
fp.fact(Write1(BitVecVal(1181,var),BitVecVal(1180,lineNum)))
fp.fact(Read2(BitVecVal(1177,var), BitVecVal(1183,prop), BitVecVal(1180,lineNum)))
fp.fact(Load(BitVecVal(1181,var),BitVecVal(1177,var), BitVecVal(1182,prop),BitVecVal(1180,lineNum)))
fp.fact(Write1(BitVecVal(1181,var),BitVecVal(1180,lineNum)))
fp.fact(Heap(BitVecVal(1184,var),BitVecVal(1186,obj)))
fp.fact(Assign(BitVecVal(1181,var),BitVecVal(1187,obj),BitVecVal(1180,lineNum)))
#UpdateExpression: PROPERTIES[tmpv11].likes++;
code[1188]="PROPERTIES[tmpv11].likes++;"
fp.fact(Write2(BitVecVal(1002,obj),BitVecVal(1181,var), BitVecVal(1188,lineNum)))
fp.fact(Read2(BitVecVal(1002,var), BitVecVal(1181,prop), BitVecVal(1188,lineNum)))
fp.fact(Load(BitVecVal(1190,var),BitVecVal(1189,prop), BitVecVal(1189,var),BitVecVal(1188,lineNum)))
fp.fact(Store(BitVecVal(1062,var),BitVecVal(1002,prop), BitVecVal(1189,var), BitVecVal(1188,lineNum)))
#VariableDecl: var tmpv12 = property.id - 1;
code[1191]="var tmpv12 = property.id - 1;"
fp.fact(Write1(BitVecVal(1192,var),BitVecVal(1191,lineNum)))
fp.fact(Write1(BitVecVal(1192,var),BitVecVal(1191,lineNum)))
fp.fact(Read2(BitVecVal(1177,var), BitVecVal(1194,prop), BitVecVal(1191,lineNum)))
fp.fact(Load(BitVecVal(1192,var),BitVecVal(1177,var), BitVecVal(1193,prop),BitVecVal(1191,lineNum)))
fp.fact(Write1(BitVecVal(1192,var),BitVecVal(1191,lineNum)))
fp.fact(Heap(BitVecVal(1195,var),BitVecVal(1197,obj)))
fp.fact(Assign(BitVecVal(1192,var),BitVecVal(1198,obj),BitVecVal(1191,lineNum)))
#VariableDecl: var tmpv9 = PROPERTIES[tmpv12].likes;
code[1199]="var tmpv9 = PROPERTIES[tmpv12].likes;"
fp.fact(Write1(BitVecVal(1200,var),BitVecVal(1199,lineNum)))
fp.fact(Read2(BitVecVal(1002,var), BitVecVal(1192,prop), BitVecVal(1199,lineNum)))
fp.fact(Load(BitVecVal(1200,var),BitVecVal(1002,var), BitVecVal(1201,prop),BitVecVal(1199,lineNum)))
#CallExpression: res.json(tmpv9);
code[1202]="res.json(tmpv9);"
#Assignment: exports.findAll = findAll;"
code[1203]="exports.findAll = findAll;"
fp.fact(Write2(BitVecVal(1204,obj),BitVecVal(1205,var), BitVecVal(1203,lineNum)))
fp.fact(Read1(BitVecVal(1206,var),BitVecVal(1203,lineNum)))
fp.fact(Store(BitVecVal(3567,var),BitVecVal(1008,var), BitVecVal(1206,prop), BitVecVal(1203,lineNum)))
#Assignment: exports.findById = findById;"
code[1207]="exports.findById = findById;"
fp.fact(Write2(BitVecVal(1208,obj),BitVecVal(1209,var), BitVecVal(1207,lineNum)))
fp.fact(Read1(BitVecVal(1210,var),BitVecVal(1207,lineNum)))
fp.fact(Store(BitVecVal(1204,var),BitVecVal(1018,var), BitVecVal(1210,prop), BitVecVal(1207,lineNum)))
#Assignment: exports.getFavorites = getFavorites;"
code[1211]="exports.getFavorites = getFavorites;"
fp.fact(Write2(BitVecVal(1212,obj),BitVecVal(1213,var), BitVecVal(1211,lineNum)))
fp.fact(Read1(BitVecVal(1214,var),BitVecVal(1211,lineNum)))
fp.fact(Store(BitVecVal(1208,var),BitVecVal(1066,var), BitVecVal(1214,prop), BitVecVal(1211,lineNum)))
#Assignment: exports.favorite = favorite;"
code[1215]="exports.favorite = favorite;"
fp.fact(Write2(BitVecVal(1216,obj),BitVecVal(1217,var), BitVecVal(1215,lineNum)))
fp.fact(Read1(BitVecVal(1218,var),BitVecVal(1215,lineNum)))
fp.fact(Store(BitVecVal(1212,var),BitVecVal(1076,var), BitVecVal(1218,prop), BitVecVal(1215,lineNum)))
#Assignment: exports.unfavorite = unfavorite;"
code[1219]="exports.unfavorite = unfavorite;"
fp.fact(Write2(BitVecVal(1220,obj),BitVecVal(1221,var), BitVecVal(1219,lineNum)))
fp.fact(Read1(BitVecVal(1222,var),BitVecVal(1219,lineNum)))
fp.fact(Store(BitVecVal(1216,var),BitVecVal(1128,var), BitVecVal(1222,prop), BitVecVal(1219,lineNum)))
#Assignment: exports.like = like;"
code[1223]="exports.like = like;"
fp.fact(Write2(BitVecVal(1224,obj),BitVecVal(1225,var), BitVecVal(1223,lineNum)))
fp.fact(Read1(BitVecVal(1226,var),BitVecVal(1223,lineNum)))
fp.fact(Store(BitVecVal(1220,var),BitVecVal(1172,var), BitVecVal(1226,prop), BitVecVal(1223,lineNum)))







fp.fact(controldep(BitVecVal(1012,lineNum),BitVecVal(1014,lineNum)))



fp.fact(controldep(BitVecVal(1022,lineNum),BitVecVal(1026,lineNum)))

fp.fact(controldep(BitVecVal(1026,lineNum),BitVecVal(1030,lineNum)))

fp.fact(controldep(BitVecVal(1030,lineNum),BitVecVal(1036,lineNum)))

fp.fact(controldep(BitVecVal(1036,lineNum),BitVecVal(1039,lineNum)))

fp.fact(controldep(BitVecVal(1039,lineNum),BitVecVal(1041,lineNum)))



fp.fact(controldep(BitVecVal(1046,lineNum),BitVecVal(1050,lineNum)))

fp.fact(controldep(BitVecVal(1050,lineNum),BitVecVal(1054,lineNum)))

fp.fact(controldep(BitVecVal(1054,lineNum),BitVecVal(1060,lineNum)))

fp.fact(controldep(BitVecVal(1060,lineNum),BitVecVal(1063,lineNum)))



fp.fact(controldep(BitVecVal(1070,lineNum),BitVecVal(1073,lineNum)))



fp.fact(controldep(BitVecVal(1080,lineNum),BitVecVal(1084,lineNum)))



fp.fact(controldep(BitVecVal(1090,lineNum),BitVecVal(1102,lineNum)))

fp.fact(controldep(BitVecVal(1102,lineNum),BitVecVal(1108,lineNum)))

fp.fact(controldep(BitVecVal(1090,lineNum),BitVecVal(1114,lineNum)))

fp.fact(controldep(BitVecVal(1114,lineNum),BitVecVal(1116,lineNum)))

fp.fact(controldep(BitVecVal(1114,lineNum),BitVecVal(1118,lineNum)))

fp.fact(controldep(BitVecVal(1118,lineNum),BitVecVal(1119,lineNum)))

fp.fact(controldep(BitVecVal(1119,lineNum),BitVecVal(1125,lineNum)))



fp.fact(controldep(BitVecVal(1132,lineNum),BitVecVal(1136,lineNum)))



fp.fact(controldep(BitVecVal(1140,lineNum),BitVecVal(1152,lineNum)))

fp.fact(controldep(BitVecVal(1152,lineNum),BitVecVal(1156,lineNum)))

fp.fact(controldep(BitVecVal(1156,lineNum),BitVecVal(1158,lineNum)))

fp.fact(controldep(BitVecVal(1158,lineNum),BitVecVal(1164,lineNum)))

fp.fact(controldep(BitVecVal(1140,lineNum),BitVecVal(1166,lineNum)))

fp.fact(controldep(BitVecVal(1166,lineNum),BitVecVal(1169,lineNum)))



fp.fact(controldep(BitVecVal(1176,lineNum),BitVecVal(1180,lineNum)))

fp.fact(controldep(BitVecVal(1180,lineNum),BitVecVal(1188,lineNum)))

fp.fact(controldep(BitVecVal(1188,lineNum),BitVecVal(1191,lineNum)))

fp.fact(controldep(BitVecVal(1191,lineNum),BitVecVal(1199,lineNum)))

fp.fact(controldep(BitVecVal(1199,lineNum),BitVecVal(1202,lineNum)))







hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:-1:-1"]={"bin":1000, "name":"var dummyvar;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:14:65"]={"bin":1001, "name":"var PROPERTIES = require('./mock-properties').data;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:18:28"]={"bin":1002, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:31:59"]={"bin":1003, "name":"require('./mock-properties')"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:31:64"]={"bin":1004, "name":"require('./mock-properties').data"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:60:64"]={"bin":1005, "name":"data"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:89:174"]={"bin":1006, "name":"function findAll(req, res, next) {\n    var tmpv0 = PROPERTIES;\n    res.json(tmpv0);\n}"};
hashVar["O_findAll"]={"bin":1007, "name":"O_findAll"};
hashVar["findAll"]={"bin":1008, "name":"findAll"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:106:109"]={"bin":1009, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:111:114"]={"bin":1010, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:116:120"]={"bin":1011, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:128:151"]={"bin":1012, "name":"var tmpv0 = PROPERTIES;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:132:137"]={"bin":1013, "name":"tmpv0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:140:150"]={"bin":1002, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:156:172"]={"bin":1014, "name":"res.json(tmpv0);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:174:175"]={"bin":1015, "name":";"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:178:371"]={"bin":1016, "name":"function findById(req, res, next) {\n    var temp4 = req.params;\n    var idd2 = temp4.id;\n    var temp5 = idd2-1;\n    var temp6 = PROPERTIES[temp5];\n    var tmpv1 = temp6;\n    res.json(tmpv1);\n}"};
hashVar["O_findById"]={"bin":1017, "name":"O_findById"};
hashVar["findById"]={"bin":1018, "name":"findById"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:196:199"]={"bin":1019, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:201:204"]={"bin":1020, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:206:210"]={"bin":1021, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:218:241"]={"bin":1022, "name":"var temp4 = req.params;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:222:227"]={"bin":1023, "name":"temp4"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:230:233"]={"bin":1019, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:230:240"]={"bin":1024, "name":"req.params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:234:240"]={"bin":1025, "name":"params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:246:266"]={"bin":1026, "name":"var idd2 = temp4.id;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:250:254"]={"bin":1027, "name":"idd2"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:257:262"]={"bin":1023, "name":"temp4"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:257:265"]={"bin":1028, "name":"temp4.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:263:265"]={"bin":1029, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:271:290"]={"bin":1030, "name":"var temp5 = idd2-1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:275:280"]={"bin":1031, "name":"temp5"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:283:287"]={"bin":1027, "name":"idd2"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:295:325"]={"bin":1036, "name":"var temp6 = PROPERTIES[temp5];"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:299:304"]={"bin":1037, "name":"temp6"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:307:317"]={"bin":1002, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:307:324"]={"bin":1038, "name":"PROPERTIES[temp5]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:318:323"]={"bin":1031, "name":"temp5"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:330:348"]={"bin":1039, "name":"var tmpv1 = temp6;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:334:339"]={"bin":1040, "name":"tmpv1"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:342:347"]={"bin":1037, "name":"temp6"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:353:369"]={"bin":1041, "name":"res.json(tmpv1);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:401:578"]={"bin":1042, "name":"function findById(req, res, next) {\n     var tmpv13 = req.params;\n     var id = tmpv13.id;\n     var tmpv10 = id - 1;\n     var tmpv2 = PROPERTIES[tmpv10];\n     res.json(tmpv2);\n}"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:419:422"]={"bin":1043, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:424:427"]={"bin":1044, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:429:433"]={"bin":1045, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:442:466"]={"bin":1046, "name":"var tmpv13 = req.params;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:446:452"]={"bin":1047, "name":"tmpv13"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:455:458"]={"bin":1043, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:455:465"]={"bin":1048, "name":"req.params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:459:465"]={"bin":1049, "name":"params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:472:491"]={"bin":1050, "name":"var id = tmpv13.id;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:476:478"]={"bin":1051, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:481:487"]={"bin":1047, "name":"tmpv13"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:481:490"]={"bin":1052, "name":"tmpv13.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:488:490"]={"bin":1053, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:497:517"]={"bin":1054, "name":"var tmpv10 = id - 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:501:507"]={"bin":1055, "name":"tmpv10"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:510:512"]={"bin":1051, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:523:554"]={"bin":1060, "name":"var tmpv2 = PROPERTIES[tmpv10];"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:527:532"]={"bin":1061, "name":"tmpv2"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:535:545"]={"bin":1002, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:535:553"]={"bin":1062, "name":"PROPERTIES[tmpv10]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:546:552"]={"bin":1055, "name":"tmpv10"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:560:576"]={"bin":1063, "name":"res.json(tmpv2);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:582:671"]={"bin":1064, "name":"function getFavorites(req, res, next) {\n    var tmpv3 = favorites;\n    res.json(tmpv3);\n}"};
hashVar["O_getFavorites"]={"bin":1065, "name":"O_getFavorites"};
hashVar["getFavorites"]={"bin":1066, "name":"getFavorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:604:607"]={"bin":1067, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:609:612"]={"bin":1068, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:614:618"]={"bin":1069, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:626:648"]={"bin":1070, "name":"var tmpv3 = favorites;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:630:635"]={"bin":1071, "name":"tmpv3"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:638:647"]={"bin":1072, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:653:669"]={"bin":1073, "name":"res.json(tmpv3);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:673:1034"]={"bin":1074, "name":"function favorite(req, res, next) {\n    var property = req.body;\n    var exists = false;\n    for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }\n    }\n    if (!exists) var tmpv4 = property;\n    favorites.push(tmpv4);\n    var tmpv5 = \"success\";\n    res.send(tmpv5)\n}"};
hashVar["O_favorite"]={"bin":1075, "name":"O_favorite"};
hashVar["favorite"]={"bin":1076, "name":"favorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:691:694"]={"bin":1077, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:696:699"]={"bin":1078, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:701:705"]={"bin":1079, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:713:737"]={"bin":1080, "name":"var property = req.body;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:717:725"]={"bin":1081, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:728:731"]={"bin":1077, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:728:736"]={"bin":1082, "name":"req.body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:732:736"]={"bin":1083, "name":"body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:742:761"]={"bin":1084, "name":"var exists = false;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:746:752"]={"bin":1085, "name":"exists"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:766:919"]={"bin":1090, "name":"for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }\n    }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:771:780"]={"bin":1091, "name":"var i = 0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:782:802"]={"bin":1092, "name":"i < favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:804:807"]={"bin":1093, "name":"i++"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:775:776"]={"bin":1094, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:782:783"]={"bin":1094, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:786:795"]={"bin":1099, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:786:802"]={"bin":1100, "name":"favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:796:802"]={"bin":1101, "name":"length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:804:805"]={"bin":1094, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:819:913"]={"bin":1102, "name":"if (favorites[i].id === property.id) {\n            exists = true;\n            break;\n        }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:823:854"]={"bin":1103, "name":"favorites[i].id === property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:823:832"]={"bin":1104, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:823:835"]={"bin":1105, "name":"favorites[i]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:833:834"]={"bin":1094, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:843:851"]={"bin":1081, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:843:854"]={"bin":1106, "name":"property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:852:854"]={"bin":1107, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:870:884"]={"bin":1108, "name":"exists = true;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:870:876"]={"bin":1085, "name":"exists"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:897:903"]={"bin":1113, "name":"break;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:924:958"]={"bin":1114, "name":"if (!exists) var tmpv4 = property;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:928:935"]={"bin":1115, "name":"!exists"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:937:958"]={"bin":1116, "name":"var tmpv4 = property;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:941:946"]={"bin":1117, "name":"tmpv4"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:949:957"]={"bin":1081, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:963:985"]={"bin":1118, "name":"favorites.push(tmpv4);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:990:1012"]={"bin":1119, "name":"var tmpv5 = \"success\";"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:994:999"]={"bin":1120, "name":"tmpv5"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1017:1032"]={"bin":1125, "name":"res.send(tmpv5)"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1036:1363"]={"bin":1126, "name":"function unfavorite(req, res, next) {\n    var tmpv14 = req.params;\nvar id = tmpv14.id;\n    for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }\n    }\n    var tmpv8 = favorites;\nres.json(tmpv8)\n}"};
hashVar["O_unfavorite"]={"bin":1127, "name":"O_unfavorite"};
hashVar["unfavorite"]={"bin":1128, "name":"unfavorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1056:1059"]={"bin":1129, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1061:1064"]={"bin":1130, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1066:1070"]={"bin":1131, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1078:1102"]={"bin":1132, "name":"var tmpv14 = req.params;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1082:1088"]={"bin":1133, "name":"tmpv14"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1091:1094"]={"bin":1129, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1091:1101"]={"bin":1134, "name":"req.params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1095:1101"]={"bin":1135, "name":"params"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1103:1122"]={"bin":1136, "name":"var id = tmpv14.id;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1107:1109"]={"bin":1137, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1112:1118"]={"bin":1133, "name":"tmpv14"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1112:1121"]={"bin":1138, "name":"tmpv14.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1119:1121"]={"bin":1139, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1127:1318"]={"bin":1140, "name":"for (var i = 0; i < favorites.length; i++) {\n        if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }\n    }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1132:1141"]={"bin":1141, "name":"var i = 0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1143:1163"]={"bin":1142, "name":"i < favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1165:1168"]={"bin":1143, "name":"i++"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1136:1137"]={"bin":1144, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1143:1144"]={"bin":1144, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1147:1156"]={"bin":1149, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1147:1163"]={"bin":1150, "name":"favorites.length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1157:1163"]={"bin":1151, "name":"length"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1165:1166"]={"bin":1144, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1180:1312"]={"bin":1152, "name":"if (favorites[i].id == id) {\n            var tmpv6 = i;\n\nvar tmpv7 = 1;\nfavorites.splice(tmpv6, tmpv7);\n            break;\n        }"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1184:1205"]={"bin":1153, "name":"favorites[i].id == id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1184:1193"]={"bin":1154, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1184:1196"]={"bin":1155, "name":"favorites[i]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1194:1195"]={"bin":1144, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1203:1205"]={"bin":1137, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1221:1235"]={"bin":1156, "name":"var tmpv6 = i;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1225:1230"]={"bin":1157, "name":"tmpv6"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1233:1234"]={"bin":1144, "name":"i"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1237:1251"]={"bin":1158, "name":"var tmpv7 = 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1241:1246"]={"bin":1159, "name":"tmpv7"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1252:1283"]={"bin":1164, "name":"favorites.splice(tmpv6, tmpv7);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1296:1302"]={"bin":1165, "name":"break;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1323:1345"]={"bin":1166, "name":"var tmpv8 = favorites;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1327:1332"]={"bin":1167, "name":"tmpv8"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1335:1344"]={"bin":1168, "name":"favorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1346:1361"]={"bin":1169, "name":"res.json(tmpv8)"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1365:1578"]={"bin":1170, "name":"function like(req, res, next) {\n    var property = req.body;\n    var tmpv11 = property.id - 1;\nPROPERTIES[tmpv11].likes++;\n    var tmpv12 = property.id - 1;\nvar tmpv9 = PROPERTIES[tmpv12].likes;\nres.json(tmpv9);\n}"};
hashVar["O_like"]={"bin":1171, "name":"O_like"};
hashVar["like"]={"bin":1172, "name":"like"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1379:1382"]={"bin":1173, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1384:1387"]={"bin":1174, "name":"res"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1389:1393"]={"bin":1175, "name":"next"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1401:1425"]={"bin":1176, "name":"var property = req.body;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1405:1413"]={"bin":1177, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1416:1419"]={"bin":1173, "name":"req"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1416:1424"]={"bin":1178, "name":"req.body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1420:1424"]={"bin":1179, "name":"body"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1430:1459"]={"bin":1180, "name":"var tmpv11 = property.id - 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1434:1440"]={"bin":1181, "name":"tmpv11"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1443:1451"]={"bin":1177, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1443:1454"]={"bin":1182, "name":"property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1452:1454"]={"bin":1183, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1460:1487"]={"bin":1188, "name":"PROPERTIES[tmpv11].likes++;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1460:1470"]={"bin":1002, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1471:1477"]={"bin":1181, "name":"tmpv11"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1460:1478"]={"bin":1189, "name":"PROPERTIES[tmpv11]"};
hashVar["ttemp0"]={"bin":1190, "name":"ttemp0"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1492:1521"]={"bin":1191, "name":"var tmpv12 = property.id - 1;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1496:1502"]={"bin":1192, "name":"tmpv12"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1505:1513"]={"bin":1177, "name":"property"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1505:1516"]={"bin":1193, "name":"property.id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1514:1516"]={"bin":1194, "name":"id"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1522:1559"]={"bin":1199, "name":"var tmpv9 = PROPERTIES[tmpv12].likes;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1526:1531"]={"bin":1200, "name":"tmpv9"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1534:1544"]={"bin":1002, "name":"PROPERTIES"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1534:1552"]={"bin":1201, "name":"PROPERTIES[tmpv12]"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1545:1551"]={"bin":1192, "name":"tmpv12"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1560:1576"]={"bin":1202, "name":"res.json(tmpv9);"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1580:1606"]={"bin":1203, "name":"exports.findAll = findAll;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1580:1587"]={"bin":1204, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1588:1595"]={"bin":1205, "name":"findAll"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1598:1605"]={"bin":1206, "name":"findAll"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1607:1635"]={"bin":1207, "name":"exports.findById = findById;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1607:1614"]={"bin":1208, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1615:1623"]={"bin":1209, "name":"findById"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1626:1634"]={"bin":1210, "name":"findById"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1636:1672"]={"bin":1211, "name":"exports.getFavorites = getFavorites;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1636:1643"]={"bin":1212, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1644:1656"]={"bin":1213, "name":"getFavorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1659:1671"]={"bin":1214, "name":"getFavorites"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1673:1701"]={"bin":1215, "name":"exports.favorite = favorite;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1673:1680"]={"bin":1216, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1681:1689"]={"bin":1217, "name":"favorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1692:1700"]={"bin":1218, "name":"favorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1702:1734"]={"bin":1219, "name":"exports.unfavorite = unfavorite;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1702:1709"]={"bin":1220, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1710:1720"]={"bin":1221, "name":"unfavorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1723:1733"]={"bin":1222, "name":"unfavorite"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1735:1755"]={"bin":1223, "name":"exports.like = like;"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1735:1742"]={"bin":1224, "name":"exports"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1743:1747"]={"bin":1225, "name":"like"};
hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:1750:1754"]={"bin":1226, "name":"like"};


fp.fact(ref(BitVecVal(hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:476:478"]["bin"],var),BitVecVal(1888,val)))
fp.fact(ref(BitVecVal(hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:527:532"]["bin"],var),BitVecVal(1999,val)))

# fp.fact(ref2(BitVecVal(hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:535:545"]["bin"],var),BitVecVal(hashVar["subject_apps/ionic2-realty-rest/server/norm_property-service.js:546:552"]["bin"],prop), BitVecVal(1999,val)))

# hashVar["norm_property-service.js:132:137"]={"bin":1013, "name":"tmpv0"};
# hashVar["norm_property-service.js:140:150"]

# function to return key for any value

#fp.fact(ref2(BitVecVal(1001,var),BitVecVal(1019,prop), BitVecVal(1999,val)))

# fp.fact(ref2(BitVecVal(hashVar["TempV1"],var),BitVecVal(hashVar["BROKERS"],prop), BitVecVal(1999,val)))

# fp.fact(ref(BitVecVal(hashVar["norm_property-service.js:436:455"]['bin'],var),BitVecVal(1888,val)))
# fp.fact(ref2(BitVecVal(hashVar["norm_property-service.js:487:518"]['bin'],var),BitVecVal(hashVar["norm_property-service.js:465:471"]['bin'],prop), BitVecVal(1999,val)))

# print hashVar["norm_property-service.js:436:455"]['bin']
exitLine = Const('exit', lineNum)
fp.declare_var(exitLine)

fp.query(unMarshal(line2, v1, 1888))
v_ex = fp.get_answer()
unmarshal_stmt = v_ex.arg(1).arg(1).as_long()
unmarshal_stmt_start = get_key(unmarshal_stmt).split(":")[1]
print "unMarshal***********  ", colored(v_ex,'magenta'), unmarshal_stmt, unmarshal_stmt_start
#
#
fp.query(Marshal(line2, v1, 1999))
v_ex = fp.get_answer()
print "Marshal***********  ", colored(v_ex,'blue'), v_ex


# fp.fact(Load(BitVecVal(27,var),BitVecVal(2,prop), BitVecVal(17,var),BitVecVal(16736239,lineNum)))
# fp.fact(ref2(BitVecVal(17,var),BitVecVal(2,prop), BitVecVal(1999,val)))

marshal_stmt = v_ex.arg(1).arg(1).as_long()
loadedVar = v_ex.arg(0).arg(1).as_long()
marshal_stmt_start = get_key(marshal_stmt).split(":")[1]
print "Marshal***********  ", colored(v_ex,'blue') , marshal_stmt, marshal_stmt_start
print "LoadedVar??  ", loadedVar
# fp.fact(Load(BitVecVal(1028,var),BitVecVal(1001,var), BitVecVal(1020,prop),BitVecVal(1027,lineNum)))


fp.query(datadep(exitLine,unmarshal_stmt))
v_ex = fp.get_answer()
print "@@@@@@@@@@@@***********  ", v_ex


fp.query(datadep(exitLine,marshal_stmt))
v_ex = fp.get_answer()
print "@@@@@@@@@@@@***********  ", v_ex

# fp.query(Load)
# v_ex = fp.get_answer()
# print "######################LoadOrAssignVar", v_ex

fp.query(Executed(exitLine, 12313, 1888, 1999))
v_ex = fp.get_answer()
print "ExecutedExecutedExecuted***********  ", type(v_ex), v_ex
uid = "abcDe"


jscode=""

extract_ftn={};
extract_others={};

for x in range(0, v_ex.num_args()):
    myposition = get_key(v_ex.arg(x).arg(1).as_long()).split(":")[1];
    if myposition<unmarshal_stmt_start or myposition>marshal_stmt_start:
        extract_others[myposition]= v_ex.arg(x).arg(1).as_long();
    else:
        extract_ftn[myposition]=v_ex.arg(x).arg(1).as_long();

print "extract_ftn", extract_ftn
print "extract_others", extract_others


for key in sorted(extract_others.keys()):
    print colored(code[extract_others[key]], 'red')
    jscode +=code[extract_others[key]]+"\n"

print colored("function "+uid+"(input){","yellow")
jscode +="function "+uid+"(input){"+"\n"
print colored(adaptinput(code[unmarshal_stmt],"id"), 'blue')

for key in sorted(extract_ftn.keys()):
    print colored("\t" + code[extract_ftn[key]], 'yellow')
    jscode += code[extract_ftn[key]] + "\n"

print colored(adaptoutput(code[marshal_stmt], loadedVar), 'blue')
jscode +=adaptoutput(code[marshal_stmt], loadedVar) +"\n"
print colored("\treturn output;\n}","yellow")
jscode +="\treturn output;\n}"
f=open(uid+".js", "w")
f.write(jscode)
