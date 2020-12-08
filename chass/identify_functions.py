from chass.get_variable import get_variable

# This function takes the preprocessed file as input 
# It returns a list of triples in which the first element gives the function name,
# second element gives the starting line number and the third element gives the ending line number

def identify_functions(file) :
	file = open(file,"r")
	functions = []
	line_number = 0
	ftuple = ()
	count = 0
	for line in file.readlines() :
		first_variable = get_variable(line,0,"forward")
		if first_variable == "function" :
			ftuple = (get_variable(line,9,"forward"),line_number,)
		elif first_variable :
			flag = False
			for i in range(len(first_variable),len(line)) :
				if line[i]=='(' :
					flag = True
				elif line[i]==')' and flag :
					ftuple = (first_variable,line_number,)
					flag = False
				else : 
					flag = False
		if '{' in line and len(ftuple)==2 :
			count += 1
		if '}' in line and len(ftuple)==2 :
			count -= 1 
			if count==0 :
				ftuple += (line_number,)
				functions.append(ftuple)
		line_number += 1
	return functions