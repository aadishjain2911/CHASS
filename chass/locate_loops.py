from chass.get_variable import get_variable

# Function takes preprocessed file and three empty lists as arguments
# This function fills tuples in the three lists with for, while, and until loops
# The tuple represents (starting index, ending index) of the corresponding loop

def locate_loops(file,for_loops,while_loops,until_loops) :
	file = open(file,"r")
	prev_for_line_number = [0] # these arrays are used to take care of nested loops
	prev_while_line_number = [0]
	prev_until_line_number = [0]
	line_number = -1
	for line in file.readlines() :
		line_number+=1
		if get_variable(line,0,"forward")=="for" : # if the line starts with the "for" keyword then
			prev_for_line_number.append(line_number) # appends the line to the list of for loops
		elif get_variable(line,0,"forward")=="while" : # similarly for while loops
			prev_while_line_number.append(line_number)
		elif get_variable(line,0,"forward")=="until" : # similarly for until loops
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