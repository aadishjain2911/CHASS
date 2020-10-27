# This function is to get the name of variable whose name starts from a known position of a line
# It is based on the fact that a variable name can only contain either alpha-numeric characters or an underscore character
# Takes three arguments - a line in the form of string, the starting position, and a flag which tells 
# whether the variable name is to be looked in forward direction or backward direction
# Returns the variable name as a string 

def get_variable(line,start,flag) :
	if flag=="forward" :
		for ite in range(start,len(line)) :
			if ( not line[ite].isalpha() ) and ( not line[ite].isnumeric() ) and (line[ite]!='_'):
				if ite==start : return False
				var = line[start:ite]
				return var
				break
			if ite==(len(line)-1) :
				var = line[start:]
				return var
				break
	else :
		for ite in range(start,-1,-1) :
			if ( not line[ite].isalpha() ) and ( not line[ite].isnumeric() ) and (line[ite]!='_'):
				if ite==start : return False
				var = line[ite+1:start+1]
				return var
				break
			if ite==0 :
				var = line[ite:start+1]
				return var
				break