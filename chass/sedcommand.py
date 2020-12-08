from chass.locate_commands import locate_commands
import subprocess

def sedcommand (thepassedfile, commands, params):
	f = open(thepassedfile,"r+")
	g = open("copy2.sh","w+")
	sed_count=0
	lines = f.readlines()
	sed_ls = []
	for a,b in commands:
		if(b=="sed"):
			sed_ls.append(a)

	for index in sed_ls:
		lines[index] = lines[index].strip("\n")
		lines[index]+=  ">> sedfile"+str(sed_count)+".txt\n"
		sed_count+=1

	g.write(''.join(lines))
	f.close()
	g.close()

	temporary = open("garbage_file.txt","a")
	temporary.flush()
	subprocess.Popen(["bash","copy2"+".sh"]+params,stdout=temporary,stderr=subprocess.STDOUT)

	# commands = locate_commands(thepassedfile)