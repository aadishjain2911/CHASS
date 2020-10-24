from get_variable import get_variable

def locate_ifs(file) :
	if_statements = []
	prev_line_number = []
	line_number = 0
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