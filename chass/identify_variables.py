from chass.get_variable import get_variable

# This function takes the preprocesased file as the only argument
# Returns a list containing information of the variables in the form of triples
# The elements of each triple give name of the variable, type of the variable, and the line number of the
# first line where the variable is used, respectively

def identify_variables(f):
	file = open(f, "r")
	variables_info = []
	line_number = -1
	for line in file.readlines():
		line_number += 1
		for iterator in range(0, len(line)):
			if line[iterator] == "=":
				if iterator != 0:
					var = get_variable(line, iterator-1, "backward")
					if var:
						if line[iterator+1].isnumeric():
							variables_info.append((var, 'i', line_number))
						elif line[iterator+1] == '(':
							variables_info.append((var, 'a', line_number))
						elif line[iterator+1] == '`':
							variables_info.append((var, 'c', line_number))
						elif line[iterator+1] == '$':
							if line[iterator+2].isalpha() or line[iterator+2] == '_':
								temp1 = get_variable(line, iterator+2, "forward")
								for ele in variables_info:
									if ele[0] == temp1:
										variables_info.append((var, ele[1], line_number))
										break
							else:
								variables_info.append((var, 'm', line_number))
						else:
							variables_info.append((var, 'm', line_number))
		if line[0:7] == "declare":
			for iterator in range(11, len(line)):
				temp = iterator
				if line[iterator] == "=":
					break
			variables_info.append((line[11:temp], line[9], line_number))
	delete_indices = []
	for ele1 in range(len(variables_info)):
		for ele2 in range(ele1+1, len(variables_info)):
			if (variables_info[ele1][0] == variables_info[ele2][0]):
				if ele2 not in delete_indices:
					delete_indices.append(ele2)
	for ele in sorted(delete_indices, reverse=True):
		del variables_info[ele]
	return variables_info
