from get_variable import get_variable

def locate_loops(file,for_loops,while_loops,until_loops) :
	prev_for_line_number = [0]
	prev_while_line_number = [0]
	prev_until_line_number = [0]
	line_number = 0
	for line in file.readlines() :
		line_number+=1
		if get_variable(line,0,"forward")=="for" :
			prev_for_line_number.append(line_number)
		elif get_variable(line,0,"forward")=="while" :
			prev_while_line_number.append(line_number)
		elif get_variable(line,0,"forward")=="until" :
			prev_until_line_number.append(line_number)
		elif get_variable(line,0,"forward")=="done" :
			if prev_while_line_number[-1]>prev_for_line_number[-1] and prev_while_line_number[-1]>prev_until_line_number[-1] :
				while_loops.append((prev_while_line_number[-1],line_number))
				prev_while_line_number.pop()
			elif prev_until_line_number[-1]>prev_for_line_number[-1] and prev_while_line_number[-1]<prev_until_line_number[-1] :
				until_loops.append((prev_until_line_number[-1],line_number))
				prev_until_line_number.pop()
			else :
				for_loops.append((prev_for_line_number[-1],line_number))
				prev_for_line_number.pop()