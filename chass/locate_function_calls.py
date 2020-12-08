from chass.get_variable import get_variable

# This function takes the preprocessed file and the name of the function as input
# Returns a list of line numbers which denote where the function was called

def locate_function_calls(file,func_name) :
	file = open(file,"r")
	function_calls = []
	line_number = 0
	for line in file.readlines() :
		for i in range(0,len(line)) :
			character = line[i]
			if character.isalpha() or character.isnumeric() or character=='_' :
				temp = get_variable(line,i,"forward")
				if func_name == temp :
					function_calls.append(line_number)
					break
				else :
					i += len(temp) 
		line_number += 1
	return function_calls