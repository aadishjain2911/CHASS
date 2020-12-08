import subprocess
from chass.locate_ifs import locate_ifs
from chass.locate_loops import locate_loops
#the function funcvar is used to make two files one containing the value of a variable and the other conataining the corresponding line number
#funcvar takes four parameters the preprocessed file name, the variable to be tracked, the type of the variable and a list of the parameters to the bash file provided by the user
#funcvar additionally calls the function locate_ifs which returns a list of positions of if statements
#funcvar also calls the function locate_loops . This stores the positions of for, while and until loops in sometuple_list_for,some_tupelist_w,some_tuplist_un respectively
#finally funcvar starts a subprocess to make the two files one containing the value of a variable and the other conataining the corresponding line number.
def funcvar(theapssedfile,variable,var_type,params,cases_, func) :
	f = open(theapssedfile,"r+")
	somelist_if = locate_ifs(theapssedfile)
	f = open(theapssedfile,"r+")
	sometuple_list_for = []
	some_tupelist_w = []
	some_tuplist_un = []
	fun_l = []
	locate_loops(theapssedfile, sometuple_list_for,
	             some_tupelist_w, some_tuplist_un)
	f = open(theapssedfile,"r+")
	g = open(str(variable)+"some_random_jargon"+".sh","w+")
	lines = f.readlines()
	sanitylist = []
	mylines = ""
	t = 1
	for_close_op = []
	case_list=[]
	for i in lines:
		sanitylist.append(1)
		for_close_op.append(0)
		case_list.append(0)
		fun_l.append(0)
	for k in somelist_if:
		for e in range(0,len(k)):
			if(e==len(k)-1):
				break
			else:
				sanitylist[k[e]]=0
	for i in cases_:
		case_list[i[0]]=1
		for j in range(1,len(i)):
			case_list[i[j]-1]=1
	for i in func:
		fun_l[i[1]]=1
		fun_l[i[2]]=-1
	for i in range(1,len(lines)):
		fun_l[i]+=fun_l[i-1]
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
	if (var_type=="a" or var_type=="A"):
		for i in lines:
			if(sanitylist[t]==1 and case_list[t]==0 and (fun_l[t]==0)):
				mylines=i+"\necho '"+str(t)+"'>>"+variable+"_line_some_rand_txt_itshouldnotbecommonwithavarname.txt"+"\n"+"\necho ${"+variable+"[*]}>>"+variable+".txt\n"
			else:
				mylines=i
			t+=1
			g.write(mylines)
	else:
		for i in lines:
			if(sanitylist[t]==1 and case_list[t]==0 and (fun_l[t]==0)):
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
	subprocess.Popen(["bash",str(variable)+"some_random_jargon"+".sh"]+params,stdout=temporary,stderr=subprocess.STDOUT)
