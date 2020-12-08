from chass.get_variable import get_variable


# This function takes the preprocessed file as input and creates a new file
# Removes cp and cd commands from the file so that the file can be run without any error

def remove_cp(file) :
	myfile = open(file,"r")
	line_number = 0 
	commands = []
	string = ""
	for line in myfile.readlines() :
		new_line = line
		command = get_variable(line,0,"forward")
		if command :
			if command == "cd" :
				new_line = new_line.replace(new_line,"\n")
				commands.append((line_number,"cd"))
			elif command == "cp" :
				new_line = new_line.replace(new_line,"\n")
				commands.append((line_number,"cp"))
		elif " cd " in line :
			new_line = new_line.replace(new_line,"\n")
			commands.append((line_number,"cd"))
		elif " cp " in line :
			new_line = new_line.replace(new_line,"\n")
			commands.append((line_number,"cp"))
		string+=new_line
		line_number+=1
	new_file = open("copy3.sh","w")
	new_file.write(string)	