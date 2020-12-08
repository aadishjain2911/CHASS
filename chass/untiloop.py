import subprocess
from chass.locate_ifs import locate_ifs
from chass.locate_loops import locate_loops

def untiloop (thepassedfile, start_index, end_index ,index,variable_info,params):
	f = open(thepassedfile,"r+")
	g = open("untiloop" + str(index) + ".sh", "w+")
	lines = f.readlines()
	mylines = ""
	i=0
	before_end=end_index-1
	after_start = start_index+1
	for j in lines:
		# if(i==after_start):
		# 	mylines = j+"\necho 'iteration' >> forloop"+str(index)+".txt"
		if(i==before_end):
			mylines =j
			for(a,b,c) in variable_info:
				mylines=mylines+"\necho ${"+a+"[*]}>>"+"untiloop"+str(index)+".txt\n"
		else:
			mylines=j

		g.write(mylines)
		i=i+1

	f.close()
	g.close()

	temporary = open("garbage_file.txt","a")
	temporary.flush()
	subprocess.Popen(["bash","untiloop"+str(index)+".sh"]+params,stdout=temporary,stderr=subprocess.STDOUT)