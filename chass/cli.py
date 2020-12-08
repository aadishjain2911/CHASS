import click
import subprocess
import os
import time
from chass.preprocessing import preprocessing
from chass.changed_variables import changed_variables
from chass.identify_variables import identify_variables
from chass.variable import funcvar
from chass.get_line_number import get_value_at_line
from chass.locate_loops import locate_loops
from chass.locate_case import locate_cases
from chass.locate_commands import locate_commands
from chass.identify_functions import identify_functions
from chass.calculate_expr import calculate_expr
from chass.function_handle import function_handle
from chass.sedcommand import sedcommand
from chass.forloop import forloop
from chass.whiloop import whiloop
from chass.untiloop import untiloop
from chass.get_file_paths import get_path
from chass.if_else import if_else
from chass.case_foo import edit_case
from chass.locate_ifs import locate_ifs
from chass.locate_function_calls import locate_function_calls
from chass.remove_cp import remove_cp

@click.command()
@click.option('--variable', '-v', multiple=True, help='Execute this specific variable')
@click.option('--line', '-l', type=int, help='Get value at a particular line')
@click.option('--code', '-c', type=int, help='Get code for a particular line')
@click.option('--codeline', nargs=2, type=int, help='Get a section of your code')
@click.option('--breakpoints', nargs=2, type=int, help="set breakpoint")
@click.option('--function','-f', help="Debug only a function by providing its name")
@click.option('--printall','-p', is_flag=True, help="Prints all the changed variables' values at every line in one go")
@click.option('--output','-o', is_flag=True, help="Shows the actual output of the file")
@click.option('--loops','-r', is_flag=True, help="Debug Only loops")
@click.option('--cond','-i', is_flag=True, help="Debug only conditional statements")
@click.option('--sed','-s', is_flag=True, help="Shows the output of all the sed commands")
@click.argument('file', type=click.Path())

def cli(file, variable, line, code, codeline, breakpoints, function, printall, output, loops, cond, sed):
    """A user friendly CLI Debugging application exclusively for Bash Scripts"""

    # delete all pre-existing .txt files
    try :
        os.system("rm *.txt >/dev/null 2>&1")
    except : 
        pass
    
    #delete all pre-existing .sh files
    try :
        os.system("rm *.sh >/dev/null 2>&1")
    except : 
        pass

    #create a copy of original file for furthur processing

    preprocessing(file)
    
    subprocess.call("chmod 777 ./copy.sh", shell=True)
    
    # take parameter from user if required
    input_parameters = []
    click.echo("Provide input parameters and press ENTER : ")

    for argument in input().split(" ") :
        input_parameters.append(argument)

    new_file = "copy.sh"
    f = "copy.sh"
    
    variables_info = identify_variables(new_file)

    if_statements = locate_ifs("copy.sh")

    for_loops = []
    while_loops = []
    until_loops = []
    locate_loops(new_file,for_loops,while_loops,until_loops)
    variables_info = identify_variables(new_file)

    remove_cp("copy.sh")

    temp = open("original_output.txt","w")
    temp.flush()
    subprocess.Popen(["bash","copy3.sh"]+input_parameters,stdout=temp,stderr=subprocess.STDOUT)
    time.sleep(0.5)

    if output :
        click.echo("The output of the file is : ")
        click.echo(open("original_output.txt",'r').read())

    commands = locate_commands("copy.sh")

    new_file = open("copy.sh")

    sedcommand(f,commands,input_parameters)

    case_statements = locate_cases("copy.sh")

    functions = identify_functions(f)

    for (a, b, c) in variables_info :
        funcvar(f, a, b, input_parameters, case_statements, functions)

    for (a,b,c) in functions:
        function_handle(f,a,b,c,variables_info,case_statements,input_parameters)

    time.sleep(0.5)

    cnt_for_loops = 0
    cnt_while_loops = 0
    cnt_until_loops = 0

    for (a,b) in for_loops:
        forloop(f,a,b,cnt_for_loops,variables_info,input_parameters)
        cnt_for_loops=cnt_for_loops+1

    for (a,b) in while_loops:
        whiloop(f,a,b,cnt_while_loops,variables_info,input_parameters)
        cnt_while_loops += 1

    for (a,b) in until_loops:
        untiloop(f,a,b,cnt_until_loops,variables_info,input_parameters)
        cnt_until_loops += 1
    time.sleep(0.2)

    if_else("copy.sh",for_loops,functions,while_loops,until_loops,if_statements,input_parameters)

    edit_case("copy.sh",case_statements,for_loops,functions,while_loops,until_loops,input_parameters)

    time.sleep(1)

    #count total lines
    num_lines=0
    new_file = open("copy.sh","r")
    for li in new_file:
        num_lines+=1
    new_file.close()

    get_path(file,num_lines,commands)

    #only loops
    if loops:
        new_file = open("copy.sh")
        i = -1
        changed_variables_info = {}
        for (a,b,c) in variables_info:
            changed_variables_info[a] = ''
        
        while i<(num_lines-1):
            i+=1
            b = False
            loop_number = -1
            #for
            for iterator in for_loops:
                loop_number += 1
                if iterator[0] == i:
                    b = True
                    click.echo("For loop starting from line " +str(iterator[0]+1))
                    for_loop_file = "forloop"+str(loop_number)+".txt"
                    line_number = -1
                    for line in open(for_loop_file, "r"):
                        line_number += 1
                        if (line_number % len(variables_info) == 0):
                            click.echo("press ENTER to continue")
                            var = input()
                            click.echo(
                                "Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                        if var == '':
                            mod = line_number % len(variables_info)
                            if line != changed_variables_info[variables_info[mod][0]] and line != '\n':
                                changed_variables_info[variables_info[mod][0]] = line
                                click.echo(variables_info[mod][0]+" : "+line)
                        elif var == "quit":
                            break
                        else:
                            click.echo("Command not found.")
                            i -= 1
                    break
                if iterator[0] < i and i < iterator[1]:
                    b = True
                if b:
                    break
            if b:
                continue
            loop_number=-1
            #while
            for iterator in while_loops:
                loop_number += 1
                if iterator[0] == i:
                    b = True
                    click.echo("While loop starting from line " +str(iterator[0]+1))
                    while_loop_file = "whiloop"+str(loop_number)+".txt"
                    line_number = -1
                    for line in open(while_loop_file, "r"):
                        line_number += 1
                        if (line_number % len(variables_info) == 0):
                            click.echo("press ENTER to continue")
                            var = input()
                            click.echo(
                                "Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                        if var == '':
                            mod = line_number % len(variables_info)
                            if line != changed_variables_info[variables_info[mod][0]] and line != '\n':
                                changed_variables_info[variables_info[mod][0]] = line
                                click.echo(variables_info[mod][0]+" : "+line)
                        elif var == "quit":
                            break
                        else:
                            click.echo("Command not found.")
                            i -= 1
                    continue
                if iterator[0] < i and i < iterator[1]:
                    b = True
                if b:
                    break
            if b:
                continue
            loop_number = -1
            #until
            for iterator in until_loops:
                loop_number += 1
                if iterator[0] == i:
                    b = True
                    click.echo("Until loop starting from line " +str(iterator[0]+1))
                    until_loop_file = "untiloop"+str(loop_number)+".txt"
                    line_number = -1
                    for line in open(until_loop_file, "r"):
                        line_number += 1
                        if (line_number % len(variables_info) == 0):
                            click.echo("press ENTER to continue")
                            var = input()
                            click.echo("Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                        if var == '':
                            mod = line_number % len(variables_info)
                            if line != changed_variables_info[variables_info[mod][0]] and line != '\n':
                                changed_variables_info[variables_info[mod][0]] = line
                                click.echo(variables_info[mod][0]+" : "+line)
                        elif var == "quit":
                            break
                        else:
                            click.echo("Command not found.")
                            i -= 1
                    continue
                if iterator[0] < i and i < iterator[1]:
                    b = True
                if b:
                    break
            if b:
                continue

    # conditional statements
    elif cond :
        changed_variables_info = {}
        for (a,b,c) in variables_info :
            changed_variables_info[a] = ''
        for ntuple in if_statements :
            i = ntuple[0]
            check = False
            for iterator in for_loops :
                if iterator[0]<i and i<iterator[1] :
                    check = True
                    break
            for iterator in while_loops :
                if iterator[0]<i and i<iterator[1] :
                    check = True
                    break
            for iterator in until_loops :
                if iterator[0]<i and i<iterator[1] :
                    check = True
                    break
            for iterator in functions :
                if iterator[1]<i and i<iterator[2] :
                    check = True
                    break
            if check :
                continue
            else :
                while i<=ntuple[-1] :
                    if_file = "ifrand"+str(i)+".txt"
                    click.echo("press ENTER to continue")
                    var = input()
                    if i in ntuple and i!=ntuple[-1] :
                        if var=='' :
                            click.echo("line : "+str(i+1))
                            click.echo("The condition for the if/elif statement is : ")
                            subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                            click.echo("The values of the variables used in the condition are : ")
                            click.echo(open(if_file,"r").read())
                        elif var=="c" :
                            subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                            i -= 1
                        else :
                            click.echo("Command not found.")
                            i -= 1
                    else :
                        if var=='' :
                            changed_variables_list = changed_variables(f, i)
                            click.echo("line : "+str(i+1))

                            #check if variable is changed or not
                            if changed_variables_list :
                                for j in range(len(changed_variables_list)) :
                                    changed_variables_info[changed_variables_list[j][0]] = changed_variables_list[j][1]
                                    click.echo(changed_variables_list[j][0] + " : " + changed_variables_list[j][1])
                            else:
                                click.echo("No variable change!")
                        elif var=="c" :
                            subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                            i -= 1
                        else :
                            click.echo("Command not found.")
                            i -= 1
                    i += 1

    elif sed :
        changed_variables_info = {}
        for (a,b,c) in variables_info :
            changed_variables_info[a] = ''
        if not line :
            sed_count = 0
            for iterator in commands :
                if iterator[1]=="sed" :
                    i = iterator[0]
                    sedfile = open("sedfile"+str(sed_count)+".txt","r+")
                    sed_count += 1
                    click.echo("press ENTER to continue")
                    var = input()
                    if var=='' :
                        click.echo("line : "+str(i+1))
                        out = sedfile.read()
                        if out!='' :
                            click.echo("The output of the sed file is : ")
                            click.echo(out)
                        else :
                            changed_variables_list = changed_variables(f, i)
                            #check if variable is changed or not
                            if changed_variables_list :
                                for j in range(len(changed_variables_list)) :
                                    changed_variables_info[changed_variables_list[j][0]] = changed_variables_list[j][1]
                                    click.echo(changed_variables_list[j][0] + " : " + changed_variables_list[j][1])
                            else:
                                click.echo("No variable change!")
                    else :
                        click.echo("Command not found.")
        else :
            sed_count = -1
            b = False
            for iterator in commands :
                if iterator[1]=="sed" :
                    sed_count += 1
                    if iterator[0]==(line-1) :
                        b = True
                        sedfile = open("sedfile"+str(sed_count)+".txt","r+")
                        out = sedfile.read()
                        if out!='' :
                            click.echo("The output of the sed file is : ")
                            click.echo(out)
                        else :
                            changed_variables_list = changed_variables(f, line-1)
                            #check if variable is changed or not
                            if changed_variables_list :
                                for j in range(len(changed_variables_list)) :
                                    changed_variables_info[changed_variables_list[j][0]] = changed_variables_list[j][1]
                                    click.echo(changed_variables_list[j][0] + " : " + changed_variables_list[j][1])
                            else:
                                click.echo("No variable change!")
            if not b :
                click.echo("No sed command found on given line number.")
    elif function :
        check = False
        starting_index = 0
        ending_index = 0
        for (a,b,c) in functions :
            if function == a :
                starting_index = b
                ending_index = c
                check = True
                break

        if not check :
            click.echo("No such function is defined.")
        else :
            function_arguments = []
            click.echo("Provide input arguments for the function and press ENTER : ")
            for argument in input().split(" ") :
                function_arguments.append(argument)
            function_calls_list = locate_function_calls("copy.sh",function)
            click.echo("The line numbers where the function was called are : ")
            for d in function_calls_list :
                if d!=starting_index :
                    print(d+1,end=" ")
            click.echo()
            i = starting_index
            sed_count = 0
            line_number = -1
            changed_variables_info = {}
            for (a,b,c) in variables_info :
                changed_variables_info[a] = ''
            while i<(ending_index-1) :
                i += 1
                b = False
                loop_number = -1  
                for iterator in for_loops :
                    loop_number += 1
                    if iterator[0]<=i and i<iterator[1] :
                        b = True
                    if b: 
                        break
                if b: 
                    continue
                loop_number = -1
                for iterator in while_loops :
                    loop_number += 1
                    if iterator[0]<=i and i<iterator[1] :
                        b = True
                    if b:
                        break
                if b: 
                    continue
                loop_number = -1
                for iterator in until_loops :
                    loop_number += 1
                    if iterator[0]<=i and i<iterator[1] :
                        b = True
                    if b: 
                        break
                if b: 
                    continue
                for iterator in if_statements :
                    if iterator[0]<=i and i<iterator[-1] :
                        b = True
                        break
                if b : 
                    continue
                for iterator in case_statements :
                    if iterator[0]<=i and i<iterator[-1]:
                        b = True
                        break
                if b : 
                    continue
                for iterator in commands :
                    if iterator[0]==i and iterator[1]=="sed" :
                        sedfile = open("sedfile"+str(sed_count)+".txt","r+")
                        sed_count += 1
                        b = True
                        click.echo("press ENTER to continue")
                        var = input()
                        click.echo("line : "+str(i+1))
                        if var=='' :
                            out = sedfile.read()
                            if out!='' :
                                click.echo("The output of the sed file is : ")
                                click.echo(out)
                            else :
                                changed_variables_list = changed_variables(f, i)
                                #check if variable is changed or not
                                if changed_variables_list :
                                    for j in range(len(changed_variables_list)) :
                                        changed_variables_info[changed_variables_list[j][0]] = changed_variables_list[j][1]
                                        click.echo(changed_variables_list[j][0] + " : " + changed_variables_list[j][1])
                                else:
                                    click.echo("No variable change!")
                        elif var=='c' :
                            subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                            i -= 1
                        else :
                            click.echo("Command not found.")
                            i -= 1
                        break
                if b :
                    continue

                function_file = str(function)+"_handle.txt"
                click.echo("press ENTER to continue")
                var = input()
                if var=='' :
                    click.echo("line "+str(i+1)+" : ")
                    count = 0
                    temp = 0
                    for line in open(function_file,"r") :
                        if temp==len(variables_info) :
                            break
                        line_number += 1 
                        mod = line_number%len(variables_info)
                        if line!=changed_variables_info[variables_info[mod][0]] and line!='\n': 
                            changed_variables_info[variables_info[mod][0]] = line
                            click.echo(variables_info[mod][0]+" : "+line) 
                            count += 1
                        temp += 1
                    if count==0 :
                        click.echo("No variable change.")

                elif var=="c" :
                    subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                    i -= 1

                elif var=="quit" :
                    break

                elif var=="pwd" :
                    subprocess.call("head -"+str(i+1)+" pwd.txt | tail -1", shell=True)
                    i -= 1

                else :
                    click.echo("Command not found.")
                    i -= 1

    elif code :
        subprocess.call("head -"+str(code)+" "+str(file)+" | tail -1", shell=True)
    
    elif codeline :
        for i in range(codeline[0], codeline[1]+1):
            subprocess.call("head -"+str(i)+" "+str(file)+" | tail -1", shell=True)
    
    #particular variable b/w given breakpoints
    elif breakpoints and variable: 
        for i in range(breakpoints[0], breakpoints[1]+1):
            for variable_name in variable :
                value = get_value_at_line(variable_name, i-1)
                #check variable scope
                if i > num_lines or i <= 0:
                    click.echo("Line number out of file!")
                elif value == "\n":
                    click.echo("Variable out of scope!")
                else:
                    click.echo(variable_name + " at line number " + str(i) + ":" + str(value))

    elif breakpoints:

        new_file = open("copy.sh")
        sed_count = 0
        changed_variables_info = {}
        for (a,b,c) in variables_info :
            changed_variables_info[a] = ''
        if len(breakpoints)==0 :
            click.echo("Insufficient number of arguments for option.")
        else :
            i = breakpoints[0]-1 
            if len(breakpoints)==1 :
                temp = num_lines-1
            else :
                temp = breakpoints[1]-1
            while i<temp :
                i += 1
                b = False
                loop_number = -1
                for iterator in functions :
                    if iterator[1]==i :
                        i = iterator[2]
                        break  
                for iterator in for_loops :
                    loop_number += 1
                    if iterator[0]==i :
                        b = True
                        click.echo("For loop starting from line "+str(iterator[0]+1))
                        for_loop_file = "forloop"+str(loop_number)+".txt"
                        line_number = -1
                        for line in open(for_loop_file,"r") :
                            line_number += 1 
                            if (line_number%len(variables_info)==0) :
                                click.echo("press ENTER to continue")
                                var = input()
                                click.echo("Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                            if var=='' :
                                mod = line_number%len(variables_info)
                                if line!=changed_variables_info[variables_info[mod][0]] and line!='\n': 
                                    changed_variables_info[variables_info[mod][0]] = line
                                    click.echo(variables_info[mod][0]+" : "+line) 
                            elif var=="quit" :
                                break
                            else :
                                click.echo("Command not found.")
                                i -= 1
                        break
                    if iterator[0]<i and i<iterator[1] :
                        b = True
                    if b: 
                        break
                if b: 
                    continue
                loop_number = -1
                for iterator in while_loops :
                    loop_number += 1
                    if iterator[0]==i :
                        b = True
                        click.echo("While loop starting from line "+str(iterator[0]+1))
                        while_loop_file = "whiloop"+str(loop_number)+".txt"
                        line_number = -1
                        for line in open(while_loop_file,"r") :
                            line_number += 1 
                            if (line_number%len(variables_info)==0) :
                                click.echo("press ENTER to continue")
                                var = input()
                                click.echo("Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                            if var=='' :
                                mod = line_number%len(variables_info)
                                if line!=changed_variables_info[variables_info[mod][0]] and line!='\n' : 
                                    changed_variables_info[variables_info[mod][0]] = line
                                    click.echo(variables_info[mod][0]+" : "+line) 
                            elif var=="quit" :
                                break
                            else :
                                click.echo("Command not found.")
                                i -= 1
                        continue
                    if iterator[0]<i and i<iterator[1] :
                        b = True
                    if b:
                        break
                if b: 
                    continue
                loop_number = -1
                for iterator in until_loops :
                    loop_number += 1
                    if iterator[0]==i :
                        b = True
                        click.echo("Until loop starting from line "+str(iterator[0]+1))
                        until_loop_file = "untiloop"+str(loop_number)+".txt"
                        line_number = -1
                        for line in open(until_loop_file,"r") :
                            line_number += 1 
                            if (line_number%len(variables_info)==0) :
                                click.echo("press ENTER to continue")
                                var = input()
                                click.echo("Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                            if var=='' :
                                mod = line_number%len(variables_info)
                                if line!=changed_variables_info[variables_info[mod][0]] and line!='\n' : 
                                    changed_variables_info[variables_info[mod][0]] = line
                                    click.echo(variables_info[mod][0]+" : "+line)
                            elif var=="quit" :
                                break 
                            else :
                                click.echo("Command not found.")
                                i -= 1
                        continue
                    if iterator[0]<i and i<iterator[1] :
                        b = True
                    if b: 
                        break
                if b: 
                    continue
                for iterator in if_statements :
                    for a in range(len(iterator)-1) :
                        if iterator[a]==i :
                            if_file = "ifrand"+str(i)+".txt"
                            click.echo("press ENTER to continue")
                            var = input()
                            b = True
                            if var=='' :
                                click.echo("line : "+str(i+1))
                                click.echo("The condition for the if/elif statement is : ")
                                subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                                click.echo("The values of the variables used in the condition are : ")
                                click.echo(open(if_file,"r").read())
                            elif var=="c" :
                                subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                                i -= 1
                            else :
                                click.echo("Command not found.")
                                i -= 1
                            break
                if b : 
                    continue
                for iterator in case_statements :
                    if iterator[0]==i :
                        case_file = "case_"+str(i)+"rand__namenotcommon.txt"
                        click.echo("press ENTER to continue")
                        var = input()
                        b = True
                        if var=='' :
                            click.echo("line : "+str(i+1))
                            click.echo("The value of the variable used in the condition is : ")
                            click.echo(open(case_file,"r").read())
                        elif var=="c" :
                            subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                            i -= 1
                        else :
                            click.echo("Command not found.")
                            i -= 1
                        break
                if b : 
                    continue
                for iterator in commands :
                    if iterator[0]==i and iterator[1]=="sed" :
                        sedfile = open("sedfile"+str(sed_count)+".txt","r+")
                        sed_count += 1
                        b = True
                        click.echo("press ENTER to continue")
                        var = input()
                        if var=='' :
                            click.echo("line : "+str(i+1))
                            out = sedfile.read()
                            if out!='' :
                                click.echo("The output of the sed file is : ")
                                click.echo(out)
                            else :
                                changed_variables_list = changed_variables(f, i)
                                #check if variable is changed or not
                                if changed_variables_list :
                                    for j in range(len(changed_variables_list)) :
                                        changed_variables_info[changed_variables_list[j][0]] = changed_variables_list[j][1]
                                        click.echo(changed_variables_list[j][0] + " : " + changed_variables_list[j][1])
                                else:
                                    click.echo("No variable change!")
                        elif var=='c' :
                            subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                            i -= 1
                        else :
                            click.echo("Command not found.")
                            i -= 1
                        break
                if b :
                    continue
                click.echo("press ENTER to continue")
                var = input()
                if var=='' :
                    changed_variables_list = changed_variables(f, i)
                    click.echo("line : "+str(i+1))

                    #check if variable is changed or not
                    if changed_variables_list :
                        for j in range(len(changed_variables_list)) :
                            changed_variables_info[changed_variables_list[j][0]] = changed_variables_list[j][1]
                            click.echo(changed_variables_list[j][0] + " : " + changed_variables_list[j][1])
                    else:
                        click.echo("No variable change!")

                elif var=="expr" :
                    click.echo("Provide the expression to be calculated : ")
                    expression = input()
                    output = calculate_expr(i,expression,variables_info)

                    # if the output is empty that means either the syntax is invalid or the variable is out of scope
                    if len(output)==0 :
                        click.echo("The expression could not be evaluated.")
                    else :
                        click.echo("The output of the above expression is : "+ output)
                    i -= 1

                elif var=="c" :
                    subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                    i -= 1

                elif var=="quit" :
                    break

                elif var=="pwd" :
                    subprocess.call("head -"+str(i+1)+" pwd.txt | tail -1", shell=True)
                    i -= 1

                else :
                    click.echo("Command not found.")
                    i -= 1

    #if variable is provided
    elif variable:
        sed_count = 0
        #check if variable(s) is/are present
        for variable_name in variable :
            check = False
            for (a, b, c) in variables_info:
                if variable_name==a:
                    check=True
                    break
                else:
                    pass
            if not check:
                #varibale is not present
                click.echo("Given variable not found!")
                break
        if not check :
            pass

        elif line :
            for variable_name in variable :
                value = get_value_at_line(variable_name, line-1)
                #check variable scope
                if line > num_lines or line <= 0 :
                    click.echo("Line number out of file!")
                elif value == "\n":
                    click.echo("Variable "+variable_name+" out of scope!")
                else:
                    click.echo(variable_name+" : "+value)

        elif not printall :
            changed_variables_info = {}
            for (a,b,c) in variables_info :
                changed_variables_info[a] = ''
            i = -1
            while i<(num_lines-1):
                i += 1
                b = False
                loop_number = -1
                #for
                for iterator in for_loops:
                    loop_number += 1
                    if iterator[0] == i:
                        b = True
                        click.echo("For loop starting from line " +str(iterator[0]+1))
                        for_loop_file = "forloop"+str(loop_number)+".txt"
                        line_number = -1
                        for line in open(for_loop_file, "r"):
                            line_number += 1
                            if (line_number % len(variables_info) == 0):
                                click.echo("press ENTER to continue")
                                var = input()
                                click.echo(
                                    "Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                            if var == '':
                                mod = line_number % len(variables_info)
                                if line != '\n' and ( variables_info[mod][0] in variable) :
                                    changed_variables_info[variables_info[mod][0]] = line
                                    click.echo(variables_info[mod][0]+" : "+line)
                            elif var == "quit":
                                break
                            else:
                                click.echo("Command not found.")
                                i -= 1
                        break
                    if iterator[0] < i and i < iterator[1]:
                        b = True
                    if b:
                        break
                if b:
                    continue
                loop_number = -1
                #while
                for iterator in while_loops:
                    loop_number += 1
                    if iterator[0] == i:
                        b = True
                        click.echo("While loop starting from line " +
                                str(iterator[0]+1))
                        while_loop_file = "whiloop"+str(loop_number)+".txt"
                        line_number = -1
                        for line in open(while_loop_file, "r"):
                            line_number += 1
                            if (line_number % len(variables_info) == 0):
                                click.echo("press ENTER to continue")
                                var = input()
                                click.echo(
                                    "Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                            if var == '':
                                mod = line_number % len(variables_info)
                                if line != '\n' and ( variables_info[mod][0] in variable) :
                                    changed_variables_info[variables_info[mod][0]] = line
                                    click.echo(variables_info[mod][0]+" : "+line)
                            elif var == "quit":
                                break
                            else:
                                click.echo("Command not found.")
                                i -= 1
                        continue
                    if iterator[0] < i and i < iterator[1]:
                        b = True
                    if b:
                        break
                if b:
                    continue
                loop_number = -1
                #until
                for iterator in until_loops:
                    loop_number += 1
                    if iterator[0] == i:
                        b = True
                        click.echo("Until loop starting from line " +
                                str(iterator[0]+1))
                        until_loop_file = "untiloop"+str(loop_number)+".txt"
                        line_number = -1
                        for line in open(until_loop_file, "r"):
                            line_number += 1
                            if (line_number % len(variables_info) == 0):
                                click.echo("press ENTER to continue")
                                var = input()
                                click.echo(
                                    "Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                            if var == '':
                                mod = line_number % len(variables_info)
                                if line != '\n' and ( variables_info[mod][0] in variable) :
                                    changed_variables_info[variables_info[mod][0]] = line
                                    click.echo(variables_info[mod][0]+" : "+line)
                            elif var == "quit":
                                break
                            else:
                                click.echo("Command not found.")
                                i -= 1
                        continue
                    if iterator[0] < i and i < iterator[1]:
                        b = True
                    if b:
                        break
                if b :
                    continue
                click.echo("press ENTER to continue")
                var = input()
                if var=='' :
                    click.echo("line : "+str(i+1))
                    for var_name in variable:
                        click.echo(var_name+" = "+get_value_at_line(var_name,i))
                elif var=="c" :
                    subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                    i -= 1

                elif var=="quit" :
                    break

                elif var=="pwd" :
                    subprocess.call("head -"+str(i+1)+" pwd.txt | tail -1", shell=True)
                    i -= 1

        else :
            changed_variables_info = {}
            for (a,b,c) in variables_info :
                changed_variables_info[a] = ''
            i = -1
            while i<(num_lines-1):
                i += 1
                b = False
                loop_number = -1
                #for
                for iterator in for_loops:
                    loop_number += 1
                    if iterator[0] == i:
                        b = True
                        click.echo("For loop starting from line " +str(iterator[0]+1))
                        for_loop_file = "forloop"+str(loop_number)+".txt"
                        line_number = -1
                        for line in open(for_loop_file, "r"):
                            line_number += 1
                            if (line_number % len(variables_info) == 0):
                                click.echo(
                                    "Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                            mod = line_number % len(variables_info)
                            if line != '\n' and ( variables_info[mod][0] in variable) :
                                changed_variables_info[variables_info[mod][0]] = line
                                click.echo(variables_info[mod][0]+" : "+line)
                        break
                    if iterator[0] < i and i < iterator[1]:
                        b = True
                    if b:
                        break
                if b:
                    continue
                loop_number = -1
                #while
                for iterator in while_loops:
                    loop_number += 1
                    if iterator[0] == i:
                        b = True
                        click.echo("While loop starting from line " +
                                str(iterator[0]+1))
                        while_loop_file = "whiloop"+str(loop_number)+".txt"
                        line_number = -1
                        for line in open(while_loop_file, "r"):
                            line_number += 1
                            if (line_number % len(variables_info) == 0):
                                click.echo(
                                    "Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                            mod = line_number % len(variables_info)
                            if line != '\n' and ( variables_info[mod][0] in variable) :
                                changed_variables_info[variables_info[mod][0]] = line
                                click.echo(variables_info[mod][0]+" : "+line)
                        continue
                    if iterator[0] < i and i < iterator[1]:
                        b = True
                    if b:
                        break
                if b:
                    continue
                loop_number = -1
                #until
                for iterator in until_loops:
                    loop_number += 1
                    if iterator[0] == i:
                        b = True
                        click.echo("Until loop starting from line " +
                                str(iterator[0]+1))
                        until_loop_file = "untiloop"+str(loop_number)+".txt"
                        line_number = -1
                        for line in open(until_loop_file, "r"):
                            line_number += 1
                            if (line_number % len(variables_info) == 0):
                                click.echo(
                                    "Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                            mod = line_number % len(variables_info)
                            if line != '\n' and ( variables_info[mod][0] in variable) :
                                changed_variables_info[variables_info[mod][0]] = line
                                click.echo(variables_info[mod][0]+" : "+line)
                        continue
                    if iterator[0] < i and i < iterator[1]:
                        b = True
                    if b:
                        break
                if b :
                    continue
                click.echo("line : "+str(i+1))
                for var_name in variable:
                    click.echo(var_name+" = "+get_value_at_line(var_name,i))

    elif line :
        for (a,b,c) in variables_info :
            value = get_value_at_line(a,line-1)
            if value!="\n" :
                click.echo(a+" : "+value)

    elif printall :
        new_file = open("copy.sh")
        i = -1
        sed_count = 0
        changed_variables_info = {}
        for (a,b,c) in variables_info :
            changed_variables_info[a] = ''
        while i<(num_lines-1) :
            i += 1
            b = False
            loop_number = -1
            for iterator in functions :
                if iterator[1]==i :
                    i = iterator[2]
                    break 
            for iterator in for_loops :
                loop_number += 1
                if iterator[0]==i :
                    b = True
                    click.echo("For loop starting from line "+str(iterator[0]+1))
                    for_loop_file = "forloop"+str(loop_number)+".txt"
                    line_number = -1
                    for line in open(for_loop_file,"r") :
                        line_number += 1 
                        if (line_number%len(variables_info)==0) :
                            click.echo("Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                        mod = line_number%len(variables_info)
                        if line!=changed_variables_info[variables_info[mod][0]] and line!='\n': 
                            changed_variables_info[variables_info[mod][0]] = line
                            click.echo(variables_info[mod][0]+" : "+line) 
                    break
                if iterator[0]<i and i<iterator[1] :
                    b = True
                if b: 
                    break
            if b: 
                continue
            loop_number = -1
            for iterator in while_loops :
                loop_number += 1
                if iterator[0]==i :
                    b = True
                    click.echo("While loop starting from line "+str(iterator[0]+1))
                    while_loop_file = "whiloop"+str(loop_number)+".txt"
                    line_number = -1
                    for line in open(while_loop_file,"r") :
                        line_number += 1 
                        if (line_number%len(variables_info)==0) :
                            click.echo("Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                        mod = line_number%len(variables_info)
                        if line!=changed_variables_info[variables_info[mod][0]] and line!='\n' : 
                            changed_variables_info[variables_info[mod][0]] = line
                            click.echo(variables_info[mod][0]+" : "+line) 
                    continue
                if iterator[0]<i and i<iterator[1] :
                    b = True
                if b:
                    break
            if b: 
                continue
            loop_number = -1
            for iterator in until_loops :
                loop_number += 1
                if iterator[0]==i :
                    b = True
                    click.echo("Until loop starting from line "+str(iterator[0]+1))
                    until_loop_file = "untiloop"+str(loop_number)+".txt"
                    line_number = -1
                    for line in open(until_loop_file,"r") :
                        line_number += 1 
                        if (line_number%len(variables_info)==0) :
                            click.echo("Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                        mod = line_number%len(variables_info)
                        if line!=changed_variables_info[variables_info[mod][0]] and line!='\n' : 
                            changed_variables_info[variables_info[mod][0]] = line
                            click.echo(variables_info[mod][0]+" : "+line)
                    continue
                if iterator[0]<i and i<iterator[1] :
                    b = True
                if b: 
                    break
            if b: 
                continue
            for iterator in if_statements :
                for a in range(len(iterator)-1) :
                    if iterator[a]==i :
                        click.echo("line : "+str(i+1))
                        if_file = "ifrand"+str(i)+".txt"
                        b = True
                        click.echo("The condition for the if/elif statement is : ")
                        subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                        click.echo("The values of the variables used in the condition are : ")
                        click.echo(open(if_file,"r").read())
                        break
            if b : 
                continue
            for iterator in case_statements :
                if iterator[0]==i :
                    click.echo("line : "+str(i+1))
                    case_file = "case_"+str(i)+"rand__namenotcommon.txt"
                    b = True
                    click.echo("The value of the variable used in the condition is : ")
                    click.echo(open(case_file,"r").read())
                    break
            if b : 
                continue
            for iterator in commands :
                if iterator[0]==i and iterator[1]=="sed" :
                    sedfile = open("sedfile"+str(sed_count)+".txt","r+")
                    sed_count += 1
                    b = True
                    click.echo("line : "+str(i+1))
                    out = sedfile.read()
                    if out!='' :
                        click.echo("The output of the sed file is : ")
                        click.echo(out)
                    else :
                        changed_variables_list = changed_variables(f, i)
                        #check if variable is changed or not
                        if changed_variables_list :
                            for j in range(len(changed_variables_list)) :
                                changed_variables_info[changed_variables_list[j][0]] = changed_variables_list[j][1]
                                click.echo(changed_variables_list[j][0] + " : " + changed_variables_list[j][1])
                        else:
                            click.echo("No variable change!")
                    break
            if b :
                continue
            changed_variables_list = changed_variables(f, i)
            click.echo("line : "+str(i+1))
            
            #check if variable is changed or not
            if changed_variables_list :
                for j in range(len(changed_variables_list)) :
                    changed_variables_info[changed_variables_list[j][0]] = changed_variables_list[j][1]
                    click.echo(changed_variables_list[j][0] + " : " + changed_variables_list[j][1])
            else:
                click.echo("No variable change!")

    #Default version
    else :
        new_file = open("copy.sh")
        i = -1
        sed_count = 0
        changed_variables_info = {}
        for (a,b,c) in variables_info :
            changed_variables_info[a] = ''
        while i<(num_lines-1) :
            i += 1
            b = False
            loop_number = -1
            for iterator in functions :
                if iterator[1]==i :
                    i = iterator[2]
                    break  
            for iterator in for_loops :
                loop_number += 1
                if iterator[0]==i :
                    b = True
                    click.echo("For loop starting from line "+str(iterator[0]+1))
                    for_loop_file = "forloop"+str(loop_number)+".txt"
                    line_number = -1
                    for line in open(for_loop_file,"r") :
                        line_number += 1 
                        if (line_number%len(variables_info)==0) :
                            click.echo("press ENTER to continue")
                            var = input()
                            click.echo("Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                        if var=='' :
                            mod = line_number%len(variables_info)
                            if line!=changed_variables_info[variables_info[mod][0]] and line!='\n': 
                                changed_variables_info[variables_info[mod][0]] = line
                                click.echo(variables_info[mod][0]+" : "+line) 
                        elif var=="quit" :
                            break
                        else :
                            click.echo("Command not found.")
                            i -= 1
                    break
                if iterator[0]<i and i<iterator[1] :
                    b = True
                if b: 
                    break
            if b: 
                continue
            loop_number = -1
            for iterator in while_loops :
                loop_number += 1
                if iterator[0]==i :
                    b = True
                    click.echo("While loop starting from line "+str(iterator[0]+1))
                    while_loop_file = "whiloop"+str(loop_number)+".txt"
                    line_number = -1
                    for line in open(while_loop_file,"r") :
                        line_number += 1 
                        if (line_number%len(variables_info)==0) :
                            click.echo("press ENTER to continue")
                            var = input()
                            click.echo("Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                        if var=='' :
                            mod = line_number%len(variables_info)
                            if line!=changed_variables_info[variables_info[mod][0]] and line!='\n' : 
                                changed_variables_info[variables_info[mod][0]] = line
                                click.echo(variables_info[mod][0]+" : "+line) 
                        elif var=="quit" :
                            break
                        else :
                            click.echo("Command not found.")
                            i -= 1
                    continue
                if iterator[0]<i and i<iterator[1] :
                    b = True
                if b:
                    break
            if b: 
                continue
            loop_number = -1
            for iterator in until_loops :
                loop_number += 1
                if iterator[0]==i :
                    b = True
                    click.echo("Until loop starting from line "+str(iterator[0]+1))
                    until_loop_file = "untiloop"+str(loop_number)+".txt"
                    line_number = -1
                    for line in open(until_loop_file,"r") :
                        line_number += 1 
                        if (line_number%len(variables_info)==0) :
                            click.echo("press ENTER to continue")
                            var = input()
                            click.echo("Iteration "+str(1+int(line_number/len(variables_info)))+" : ")
                        if var=='' :
                            mod = line_number%len(variables_info)
                            if line!=changed_variables_info[variables_info[mod][0]] and line!='\n' : 
                                changed_variables_info[variables_info[mod][0]] = line
                                click.echo(variables_info[mod][0]+" : "+line)
                        elif var=="quit" :
                            break 
                        else :
                            click.echo("Command not found.")
                            i -= 1
                    continue
                if iterator[0]<i and i<iterator[1] :
                    b = True
                if b: 
                    break
            if b: 
                continue
            for iterator in if_statements :
                for a in range(len(iterator)-1) :
                    if iterator[a]==i :
                        if_file = "ifrand"+str(i)+".txt"
                        click.echo("press ENTER to continue")
                        var = input()
                        b = True
                        if var=='' :
                            click.echo("line : "+str(i+1))
                            click.echo("The condition for the if/elif statement is : ")
                            subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                            click.echo("The values of the variables used in the condition are : ")
                            click.echo(open(if_file,"r").read())
                        elif var=="c" :
                            subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                            i -= 1
                        else :
                            click.echo("Command not found.")
                            i -= 1
                        break
            if b : 
                continue
            for iterator in case_statements :
                if iterator[0]==i :
                    case_file = "case_"+str(i)+"rand__namenotcommon.txt"
                    click.echo("press ENTER to continue")
                    var = input()
                    b = True
                    if var=='' :
                        click.echo("line : "+str(i+1))
                        click.echo("The value of the variable used in the condition is : ")
                        click.echo(open(case_file,"r").read())
                    elif var=="c" :
                        subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                        i -= 1
                    else :
                        click.echo("Command not found.")
                        i -= 1
                    break
            if b : 
                continue
            for iterator in commands :
                if iterator[0]==i and iterator[1]=="sed" :
                    sedfile = open("sedfile"+str(sed_count)+".txt","r+")
                    sed_count += 1
                    b = True
                    click.echo("press ENTER to continue")
                    var = input()
                    if var=='' :
                        click.echo("line : "+str(i+1))
                        out = sedfile.read()
                        if out!='' :
                            click.echo("The output of the sed file is : ")
                            click.echo(out)
                        else :
                            changed_variables_list = changed_variables(f, i)
                            #check if variable is changed or not
                            if changed_variables_list :
                                for j in range(len(changed_variables_list)) :
                                    changed_variables_info[changed_variables_list[j][0]] = changed_variables_list[j][1]
                                    click.echo(changed_variables_list[j][0] + " : " + changed_variables_list[j][1])
                            else:
                                click.echo("No variable change!")
                    elif var=='c' :
                        subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                        i -= 1
                    else :
                        click.echo("Command not found.")
                        i -= 1
                    break
            if b :
                continue
            click.echo("press ENTER to continue")
            var = input()
            if var=='' :
                changed_variables_list = changed_variables(f, i)
                click.echo("line : "+str(i+1))

                #check if variable is changed or not
                if changed_variables_list :
                    for j in range(len(changed_variables_list)) :
                        changed_variables_info[changed_variables_list[j][0]] = changed_variables_list[j][1]
                        click.echo(changed_variables_list[j][0] + " : " + changed_variables_list[j][1])
                else:
                    click.echo("No variable change!")

            elif var=="expr" :
                click.echo("Provide the expression to be calculated : ")
                expression = input()
                output = calculate_expr(i,expression,variables_info)

                # if the output is empty that means either the syntax is invalid or the variable is out of scope
                if len(output)==0 :
                    click.echo("The expression could not be evaluated.")
                else :
                    click.echo("The output of the above expression is : "+ output)
                i -= 1

            elif var=="c" :
                subprocess.call("head -"+str(i+1)+" copy.sh | tail -1", shell=True)
                i -= 1

            elif var=="quit" :
                break

            elif var=="pwd" :
                subprocess.call("head -"+str(i+1)+" pwd.txt | tail -1", shell=True)
                i -= 1

            else :
                click.echo("Command not found.")
                i -= 1

    # delete all temp file created during execution   
    subprocess.call("rm *.txt", shell=True)
    subprocess.call("rm *.sh", shell=True)