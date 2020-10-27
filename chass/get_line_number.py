# This function returns the line number of the variable.txt which contains the value of a variable at a fixed line number 

def get_line_number(variable,line_number) :
	file = open(variable+"_line_some_rand_txt_itshouldnotbecommonwithavarname.txt","r")
	for i,line in enumerate(file) :
		if (line!='\n') :
			value = int(line)
			if line_number<=value :
				return i

# This function takes the name of a variable and a line number as input 
# It returns the value of that variable at the given line number 

def get_value_at_line(variable,line_number) :
	j = get_line_number(variable,line_number)
	file = open(variable+".txt","r")
	for i,line in enumerate(file) :
		if i==j :
			return line 