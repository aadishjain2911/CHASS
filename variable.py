import subprocess
from locate_ifs import locate_ifs
from locate_loops import locate_loops

def funcvar(theapssedfile,variable,var_type,params) :
	f = open(theapssedfile,"r+")
	somelist_if = locate_ifs(f)
	f = open(theapssedfile,"r+")
	sometuple_list_for = []
	some_tupelist_w = []
	some_tuplist_un = []
	locate_loops(f,sometuple_list_for,some_tupelist_w,some_tuplist_un)
	f = open(theapssedfile,"r+")
	g = open(str(variable)+"some_random_jargon"+".sh","w+")
	lines = f.readlines()
	sanitylist = []
	mylines = ""
	t = 1
	for_close_op = []
	for i in lines:
		sanitylist.append(1)
		for_close_op.append(0)
	for k in somelist_if:
		for e in range(0,len(k)):
			if(e==len(k)-1):
				break
			else:
				sanitylist[k[e]-1]=0

	for k in sometuple_list_for:
		for_close_op[k[0]-1]=1
		for_close_op[k[1]-1]=-1
	for k in some_tuplist_un:
		for_close_op[k[0]-1]=1
		for_close_op[k[1]-1]=-1
	for k in some_tupelist_w:
		for_close_op[k[0]-1]=1
		for_close_op[k[1]-1]=-1
	t=0
	for i in range(0,len(lines)):
		t+=for_close_op[i]
		if(t>0):
			sanitylist[i]=0
	t=0
	if (var_type=="a" or var_type=="A"):
		for i in lines:
			if(sanitylist[t]==1):
				mylines=i+"\necho '"+str(t)+"'>>"+variable+"_line_some_rand_txt_itshouldnotbecommonwithavarname.txt"+"\n"+"\necho ${"+variable+"[*]}>>"+variable+".txt\n"
			else:
				mylines=i
			t+=1
			g.write(mylines)
	else:
		for i in lines:
			if(sanitylist[t]==1):
				mylines=i+"\necho '"+str(t)+"'>>"+variable+"_line_some_rand_txt_itshouldnotbecommonwithavarname.txt"+"\n"+"echo $"+variable+">>"+variable+".txt\n"
			else:
				mylines=i
			t+=1
			g.write(mylines)
	f.close()
	g.close()
	del lines
	temporary = open("garbage_file.txt","a")
	temporary.flush()
	subprocess.Popen(["bash",str(variable)+"some_random_jargon"+".sh"]+params,stdout=temporary)
