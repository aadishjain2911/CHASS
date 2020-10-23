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