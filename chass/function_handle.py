import subprocess
from chass.locate_ifs import locate_ifs
from chass.locate_loops import locate_loops

def function_handle(thepassedfile,function_name,start_index,end_index,variables_info,cases_,params):
	f = open(thepassedfile,"r+")
	somelist_if = locate_ifs(thepassedfile)
	f = open(thepassedfile,"r+")
	sometuple_list_for = []
	some_tupelist_w = []
	some_tuplist_un = []
	locate_loops(thepassedfile, sometuple_list_for,
	             some_tupelist_w, some_tuplist_un)
	f = open(thepassedfile,"r+")
	g = open(function_name+"_handle"+".sh","w+")
	lines = f.readlines()
	sanitylist = []
	case_list=[]
	if_list=[]
	mylines = ""
	t = 1
	for_close_op = []
	for i in lines:
		sanitylist.append(1)
		for_close_op.append(0)
		case_list.append(0)
		if_list.append(0)
	for k in somelist_if:
		start=k[0]
		end=k[-1]
		for i in range(start,end):
			if_list[i]=1

	for k in cases_:
		start=k[0]
		end=k[-1]
		for i in range(start,end):
			case_list[i]=1

	for k in sometuple_list_for:
		for_close_op[k[0]]=1
		for_close_op[k[1]]=-1
	for k in some_tuplist_un:
		for_close_op[k[0]]=1
		for_close_op[k[1]]=-1
	for k in some_tupelist_w:
		for_close_op[k[0]]=1
		for_close_op[k[1]]=-1
	t=0
	for i in range(0,len(lines)):
		t+=for_close_op[i]
		if(t>0):
			sanitylist[i]=0
	t=0
	for i in lines:
		if(sanitylist[t]==1 and start_index<t and end_index>t and case_list[t]==0 and if_list[t]==0):
			mylines=i
			for (a,b,c) in variables_info:
				mylines+="echo ${"+a+"[*]}>>"+function_name+"_handle"+".txt\n"
		else:
			mylines=i
		t+=1
		g.write(mylines)
	f.close()
	g.close()
	del lines
	temporary = open("garbage_file.txt","a")
	temporary.flush()
	subprocess.Popen(["bash",function_name+"_handle"+".sh"]+params,stdout=temporary,stderr=subprocess.STDOUT)
