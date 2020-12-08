import subprocess
#func_find_var finds the variables present in a conditional statement
#func_find_var finds takes the_str as parameter which is just the string in which we have to find the variables
def func_find_var(the_str):
	l=[]
	s=""
	i=0
	while i<len(the_str):
		if(the_str[i]=='$'):
			j=i+1
			s=""
			while j<len(the_str):
				if(j==len(the_str)-1 or the_str[j]==' '):
					l.append(s)
					break
				s=s+the_str[j]
				j+=1
			i=j+1
			continue
		else:
			i+=1
	return l
#imports required for position_of_cases , position_of_fors,position_of_funct,whiles,dountils
#edit_case takes params as parameter wchich is a list of parameters to the script
#corresponding to each case statement edit_case creates a text file having the value of the cariable to be checked against the cases
def edit_case(thefile,position_of_case,position_of_fors,position_of_funct,whiles,dountils,params):
	tot_list=[]
	f=open(thefile,"r+")
	lines = f.readlines()
	e=[]
	for i in lines:
		tot_list.append(0)
	rev_=[]
	for i in lines:
		rev_.append(0)
	for i in position_of_fors:
		rev_[i[0]]+=1
		rev_[i[1]]-=1
	for i in whiles:
		rev_[i[0]]+=1
		rev_[i[1]]-=1
	for i in dountils:
		rev_[i[0]]+=1
		rev_[i[1]]-=1
	for i in position_of_funct:
		rev_[i[1]]+=1
		rev_[i[2]]-=1

	for i in range(1,len(lines)):
		tot_list[i]=tot_list[i-1]+rev_[i]
	i=0
	while i<len(position_of_case):
		if(tot_list[position_of_case[i][0]]>0):
			i+=1
			continue
		g=open("randomstringblablabla"+str(i)+"case.sh","w+")
		e.append("randomstringblablabla"+str(i)+"case.sh")
		it=0
		while it<position_of_case[i][0]:
			g.write(lines[it])
			it+=1
		l=func_find_var(lines[it])
		for k in l:
			g.write("\n echo $"+str(k)+" >>"+"case_"+str(it)+"rand__namenotcommon.txt\n")
		while it<len(lines):
			g.write(lines[it])
			it+=1
		i+=1
	for i in e:
		temporary = open("garbage_file.txt","a")
		temporary.flush()
		subprocess.Popen(["bash",i]+params,stdout=temporary,stderr=subprocess.STDOUT)
		temporary.close()