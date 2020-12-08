from chass.get_line_number import get_value_at_line
import subprocess
import time

# This function gives the output of the expression given by user at a given line number
# It takes the line number, the expression and the variables array as input
# Gives the value of the expression as output

def calculate_expr(line_number,expression,variables_info) :
	file = open("expression.sh","w")
	string = ""
	for (variable_name, b, c) in variables_info :
		variable_value = get_value_at_line(variable_name,line_number)
		string += variable_name + "=" + variable_value
	string += "echo " + expression
	file.write(string)
	file.close()
	subprocess.call("chmod 777 ./expression.sh", shell=True)
	time.sleep(0.5)
	temp = open("temporary_output_for_expression.txt","w")
	temp.flush()
	subprocess.Popen(["bash","expression.sh"],stdout=temp)
	time.sleep(0.5)
	temp.close()
	file = open("temporary_output_for_expression.txt","r")
	output = file.read()
	file.close()
	return output