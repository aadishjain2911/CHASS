def get_line_number(variable,line_number) :
	file = open(variable+"_line_some_rand_txt_itshouldnotbecommonwithavarname.txt","r")
	for i,line in enumerate(file) :
		if (line!='\n') :
			value = int(line)
			if line_number<=value :
				return i
def get_value_at_line(variable,line_number) :
	j = get_line_number(variable,line_number)
	file = open(variable+".txt","r")
	for i,line in enumerate(file) :
		if i==j :
			return line 