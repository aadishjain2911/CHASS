from chass.identify_variables import identify_variables
from chass.get_line_number import get_line_number

# This function takes the preprocessed file and the line number as an argument
# It returns a list of tuples of variables whose values have changed with respect to the previous line 
# The elements of each tuple are name of the variable and its value in the form of a string
# In case of list variables, the value is in the form of space separated elements of the list ending with a "\n"  

def changed_variables(orig_file,line_number) :
	# orig_file = "copy.sh"
	myfile = open(orig_file,"r")
	variables = identify_variables(orig_file)
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