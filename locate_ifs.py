from get_variable import get_variable

def locate_ifs(file) :
	if_statements = []
	prev_line_number = [0]
	line_number = 0
	for line in file.readlines() :
		line_number+=1
		if get_variable(line,0,"forward")=="if" :
			prev_line_number.append(line_number)
		elif get_variable(line,0,"forward")=="fi" :
			if_statements.append((prev_line_number[-1],line_number))
			prev_line_number.pop()
	return if_statements