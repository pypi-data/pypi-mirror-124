import os
import json
import ast
def start(file):
	hlxjfstart = open(file,"w")
	hlxjfstart.write('')
	hlxjfstart.close()
	hlxjf = open(file,"a")
	hlxjf.write("{ \n")
	hlxjf.close()
def end(file):
	hlxjf = open(file,"a")
	hlxjf.write("}")
	hlxjf.close()
def add(file,name,value):
	hlxjf = open(file,"a")
	hlxjf.write('"')
	hlxjf.write(name)
	hlxjf.write('":')
	hlxjf.write('"')
	hlxjf.write(value)
	hlxjf.write('",')
	hlxjf.write("\n")
	hlxjf.close()
def divstart(file,divname):
	hlxjf = open(file,"a")
	hlxjf.write('"')
	hlxjf.write(divname)
	hlxjf.write('":')
	hlxjf.write("{ \n")
	hlxjf.close()
def divend(file,divname):
	hlxjf = open(file,"a")
	hlxjf.write("}, \n")
	hlxjf.close()
def read(file,name):
	hlxjfreadfile = open(file,"r")
	hlxjfread = hlxjfreadfile.read()
	hlxjfreaddata = ast.literal_eval(hlxjfread)
	hlxjfval = hlxjfreaddata[name]
	return hlxjfval
def readdiv(file,divn,name):
	hlxreadfile = open(file,"r")
	hlxread = hlxreadfile.read()
	hlxreaddata = ast.literal_eval(hlxread)
	hlxreadval = hlxreaddata[divn][name]
	return hlxreadval