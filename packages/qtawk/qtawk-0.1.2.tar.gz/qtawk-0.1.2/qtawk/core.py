#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import stat

def getPathPyFile():
	return os.path.dirname(os.path.abspath(__file__))
	
def save(filename, data):
	#  os.remove(filename)
	with open(filename, "w") as fd :
		fd.write(data)

def load(filename):
	with open(filename, "r") as fd :
		r = fd.read()
	return r

def call_awk(command, arg, data):
	cmd = [command] 
	if type(arg) == list:
		for i in arg:
			cmd.append(i)
	else:
		cmd.append(arg)
	return call_external_command(cmd, data)

def call_external_command_without_pipe(command):
	with subprocess.Popen(command.split(), stdout=subprocess.PIPE, encoding='utf8') as proc:
		return proc.stdout.read()

def call_external_command(command, data):                                                                                             
   try:                                                                                                                           
		   p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False, encoding='utf8')             
		   return p.communicate(data)[0]                                                                                          
   # python3 need encoding='utf8'                                                                                                 
   except:                                                                                                                        
		   print("%s fail" % command)                                                                                             
   return None                                                                                                                    
     
def call_pipe(cmd, data):
	d = call_external_command(["bash", "-c", cmd], data)
	return d

def man(cmd):
	return load(getPathPyFile() + "/man/" + cmd + '.txt')

def escape_rs( t, reverse=False):
	d = { 	"\\n" : "\n", \
			"\\r" : "\r", \
			"\\t" : "\t"  }
	for k in d:
		if reverse:
			t = t.replace(d[k], k)
		else:
			t = t.replace(k, d[k])
	return t
	
def RS_text(RS):
	if escape_rs( RS ) != "\n":
		return 'RS="{}";'.format(RS)
	else:
		return ""
		
def FS_text(FS):
	if FS != " ":
		return 'FS="{}";'.format(FS)
	else:
		return ""

def awk_begin( m="", FS="", RS="" ):
	m += RS_text(RS)
	m += FS_text(FS)
	if m == "":
		return ""
	return "BEGIN{{{}}}".format(m)

def remove_tabs( t ):
	return t.replace("\t", "").replace("\n", "")

def get_script( name ):
	return remove_tabs( open( getPathPyFile() + "/scripts/" + name ).read() )
	
def chmod( fn ):
	st = os.stat(fn)
	os.chmod(fn,  st.st_mode | stat.S_IXUSR)
	
if __name__ == "__main__":
	rs = "\n"
	print(ord(escape_rs(rs)))
