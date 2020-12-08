from chass.get_variable import get_variable

# This function takes the preprocessed file as input and returns a list of n-tuples
# The first and last element of each tuple gives the starting and ending line number of the case statement respectively
# The remaining middle elements give the corresponding line numbers of cases in increasing order

def locate_cases(file) :
	file = open(file,"r")
	case_statements = []
	prev_line_number = []
	line_number = -1
	flag = False
	for line in file.readlines() :
		line_number+=1
		if get_variable(line,0,"forward")=="case" :
			prev_line_number.append((line_number,))
			flag = True
		elif get_variable(line,0,"forward")=="esac" :
			prev_line_number[-1] += (line_number,)
			case_statements.append(prev_line_number[-1])
			prev_line_number.pop()
			flag = False
		elif line[-3:-1]==";;" :
			flag = True 
		elif flag :
			temp = get_variable(line,0,"forward")
			if temp :
				if (line[len(temp)]==')') :
					prev_line_number[-1] += (line_number,)
					flag = False 
			if line[0]=="*" :
				prev_line_number[-1] += (line_number,)
				flag = False
	return case_statements