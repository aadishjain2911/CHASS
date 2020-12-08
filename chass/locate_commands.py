from chass.get_variable import get_variable


# This function takes the preprocessed file as input and returns a list of tuples
# Each tuple's first element gives the line number and the second element gives the name of the command
# Only classifies a limited number of commands namely echo, cd, mkdir, pwd, sed, awk, touch, mv, rm, cp, ln

def locate_commands(file) :
	myfile = open(file,"r")
	line_number = 0 
	commands = []
	string = ""
	for line in myfile.readlines() :
		new_line = line
		command = get_variable(line,0,"forward")
		if command :
			if command == "sed" :
				commands.append((line_number,"sed"))
				if "-n " in line :
					new_line = line.replace("-n "," ")
				if "--quiet" in line :
					new_line = line.replace("--quiet","")
				if "--silent" in line :
					new_line = line.replace("--silent","")
				if " >> " in line:
					new_line = new_line.replace(line[line.index(" >> "): ]," \n")
				if ">>" in line:
					new_line = new_line.replace(line[line.index(">>"): ]," \n")
				flag1 = True
				flag2 = True
				for i in range(len(line)) :
					character = line[i]
					if character == "'" : flag1 = not flag1
					elif character == '"' : flag2 = not flag2
					elif character == '>' and flag1 and flag2 :
						new_line = new_line.replace(line[i:]," \n")
						break
			elif command == "awk" :
				commands.append((line_number,"awk"))
			elif command == "cd" :
				new_line = new_line.replace(new_line,"\n")
				commands.append((line_number,"cd"))
			elif command == "mkdir" :
				commands.append((line_number,"mkdir"))
			elif command == "pwd" :
				commands.append((line_number,"pwd"))
			elif command == "echo" :
				commands.append((line_number,"echo"))
			elif command == "touch" :
				commands.append((line_number,"touch"))
			elif command == "mv" :
				commands.append((line_number,"mv"))
			elif command == "rm" :
				commands.append((line_number,"rm"))
			elif command == "cp" :
				new_line = new_line.replace(new_line,"\n")
				commands.append((line_number,"cp"))
		if " sed " in line :
			commands.append((line_number,"sed"))
			if "-n " in line :
				new_line = line.replace("-n "," ")
			if "--quiet" in line :
				new_line = line.replace("--quiet","")
			if "--silent" in line :
				new_line = line.replace("--silent","")
			if " >> " in line:
				new_line = new_line.replace(line[line.index(" >> "): ]," \n")
			if ">>" in line:
				new_line = new_line.replace(line[line.index(">>"): ]," \n")
			flag1 = True
			flag2 = True
			for i in range(len(line)) :
				character = line[i]
				if character == "'" : flag1 = not flag1
				elif character == '"' : flag2 = not flag2
				elif character == '>' and flag1 and flag2 :
					new_line = new_line.replace(line[i:]," \n")
					break
		if " awk " in line :
			commands.append((line_number,"awk"))
		if " cd " in line :
			new_line = new_line.replace(new_line,"\n")
			commands.append((line_number,"cd"))
		if " mkdir " in line :
			commands.append((line_number,"mkdir"))
		if " pwd " in line :
			commands.append((line_number,"pwd"))
		if " echo " in line :
			commands.append((line_number,"echo"))
		if " touch " in line :
			commands.append((line_number,"touch"))
		if " mv " in line :
			commands.append((line_number,"mv"))
		if " rm " in line :
			commands.append((line_number,"rm"))
		if " cp " in line :
			new_line = new_line.replace(new_line,"\n")
			commands.append((line_number,"cp"))
		if ">>" in line:
			new_line = new_line.replace(line[line.index(">>"): ]," \n")
		string+=new_line
		line_number+=1
	new_file = open(file,"w")
	new_file.write(string)
	return commands
		