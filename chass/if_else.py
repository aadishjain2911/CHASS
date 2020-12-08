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
#include imports for fors,whiles,dountils
#include imports for psoition of functions
#posns is positions of if_else
#params is the parameter list for the script
#thefile is a copy of the script of the user
#the function if_else creates text files corresponding to the if/elif statements having information on the variables used in the if/elif condition.
def if_else(thefile,position_of_fors,position_of_funct,whiles,dountils,posns,params):
	tot_list=[]
	f=open(thefile,"r+")
	e=[]
	lines = f.readlines()
	for i in lines:
		tot_list.append(0)
	rev_=[]
	for i in lines:
		rev_.append(0)
	for i in position_of_fors:
		rev_[i[0]]+=1
		rev_[i[1]]-=1
	for i in position_of_funct:
		rev_[i[1]]+=1
		rev_[i[2]]-=1
	for i in whiles:
		rev_[i[0]]+=1
		rev_[i[1]]-=1
	for i in dountils:
		rev_[i[0]]+=1
		rev_[i[1]]-=1
	for i in range(1,len(lines)):
		tot_list[i]=tot_list[i-1]+rev_[i]
	it=0
	w1=0
	w2=0
	b=[]
	for i in lines:
		b.append(0)
	i=0
	while i<len(posns):
		#print("uipty")
		if(tot_list[posns[i][0]]>0):
			i+=1
			continue
		g=open(str(posns[i][0])+"rand.sh","w+")
		e.append(str(posns[i][0])+"rand.sh")
		it=0
		while it<posns[i][0]:
			g.write(lines[it])
			it+=1
		
		for t in range(0,len(posns[i])-1):
			l=func_find_var(lines[posns[i][t]])
			b[posns[i][t]]=1
			for k in l:
				g.write("\necho "+str(k)+" $"+str(k)+">>ifrand"+str(posns[i][t])+".txt\n")
		while it<len(lines):
			if(b[it]==0):
				g.write(lines[it])
			else:
				l=func_find_var(lines[it])
				g.write("\necho >"+"ifrand"+str(it)+".txt\n")
				for k in l:
					g.write("\necho "+str(k)+" $"+str(k)+" >>ifrand"+str(it)+".txt\n")
				#print(type(lines))
				g.write(lines[it])
			it+=1
		i+=1
		g.close()
	for i in range(0,len(e)):
		temporary = open("garbage_file.txt","a")
		temporary.flush()
		subprocess.Popen(["bash",e[i]]+params,stdout=temporary,stderr=subprocess.STDOUT)
		temporary.close()