from chass.get_variable import get_variable

# Function takes preprocessed file and returns a list containing information about the if statements
# The list containes n-tuples of different sizes depending upon the number of elif statements associated with the if statement
# The first and last element of each tuple gives the starting and ending line number of the if statement respectively
# The remaining middle elements give the corresponding line numbers of elif statements in increasing order
# The n-tuple does not include the line number of the else statement if present

def locate_ifs(file) :
	file = open(file,"r")
	if_statements = []
	prev_line_number = []
	line_number = -1
	for line in file.readlines() :
		line_number+=1
		if get_variable(line,0,"forward")=="if" :
			prev_line_number.append((line_number,))
		elif get_variable(line,0,"forward")=="fi" :
			prev_line_number[-1] += (line_number,)
			if_statements.append(prev_line_number[-1])
			prev_line_number.pop()
		elif get_variable(line,0,"forward")=="elif" :
			prev_line_number[-1] += (line_number,)
	return if_statements