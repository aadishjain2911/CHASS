from identify_variables import identify_variables
from get_line_number import get_line_number

def changed_variables(orig_file,line_number) :
	myfile = open(orig_file,"r")
	variables = identify_variables(myfile)
	changed_variables = []
	for (var,var_type,line_num) in variables :
		file = var+".txt"
		open_file = open(file,"r")
		new_line_number = get_line_number(var,int(line_number))
		if new_line_number==0 or new_line_number==None:
			for i,line in enumerate(open_file) :
				if line!="\n" and i==0 :
					changed_variables.append((var,line))
				break
		else : 
			prev_line_number = new_line_number-1 
			for i,line in enumerate(open_file):
				if i==prev_line_number :
					prev = line
				if i==new_line_number :
					if line!=prev :
						changed_variables.append((var,line))
						break
	return changed_variables