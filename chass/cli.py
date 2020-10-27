import click
import subprocess
import time
from chass.preprocessing import preprocessing
from chass.changed_variables import changed_variables
from chass.identify_variables import identify_variables
from chass.variable import funcvar
from chass.get_line_number import get_value_at_line
from chass.locate_loops import locate_loops

@click.command()
@click.option('--variable', '-v', help='Execute this specific variable')
@click.option('--line', '-l', type=int, help='Get value for a particular line')
@click.version_option()
@click.argument('file', type=click.Path())

def cli(variable, line, quit, file):
    """A user friendly CLI Debugging application exclusively for Bash Scripts"""

    #create a copy of original file for furthue processing
    preprocessing(file)
    
    subprocess.call("chmod 777 ./copy.sh", shell=True)
    new_file = "copy.sh"
    f = "copy.sh"
    
    variables_info = identify_variables(new_file)

    for_loops = []
    while_loops = []
    until_loops = []
    locate_loops(new_file,for_loops,while_loops,until_loops)
    variables_info = identify_variables(new_file)

    new_file = open("copy.sh")
    
    #take parameter from user if required
    input_parameters = []
    click.echo("Provide input parameters and press ENTER : ")

    for argument in input().split(" ") :
        input_parameters.append(argument)

    for (a, b, c) in variables_info:
        funcvar(f, a, b, input_parameters)
        time.sleep(0.5)
		
    #if variable is provided
    if variable:

        #check if variable is present
        check=False
        for (a, b, c) in variables_info:
            if variable==a:
                check=True
                break
            else:
                pass
        
        #count total lines
        num_lines=0
        new_file = open("copy.sh")
        for li in new_file:
            num_lines+=1

        if not check:
            #varibale is not present
            click.echo("Given variable not found!")

        elif line :
            value = get_value_at_line(variable, line)
            #check variable scope
            if line > num_lines or line < 0 :
                click.echo("Line number out of file!")
            elif value == "\n":
                click.echo("Variable out of scope!")
            else:
                click.echo(value) 

        elif line==0 :
            value = get_value_at_line(variable,0)
            # check variable scope
            if value == "\n":
                click.echo("Variable out of scope!")
            else:
                click.echo(value) 

        else:
            idx=0
            new_file = open("copy.sh")
            for li in new_file:
                click.echo("line : "+str(idx))
                var = input()
                if(var==''):
                    click.echo(get_value_at_line(variable,idx))
                click.echo("press ENTER to continue")
                idx +=1

    #Default version
    else:
        i=-1
        new_file = open("copy.sh")
        for li in new_file :
            i+=1
            b = False
            for iterator in for_loops :
                if (iterator[0]<=i and i<iterator[1]) :
                    b = True
                    break
                if b: 
                    break
            if b: 
                continue
            for iterator in while_loops :
                if (iterator[0]<=i and i<iterator[1]) :
                    b = True
                    continue
                if b:
                    break
            if b: 
                continue
            for iterator in until_loops :
                if (iterator[0]<=i and i<iterator[1]) :
                    b = True
                    continue
                if b: 
                    break
            if b: 
                continue
            click.echo("press ENTER to continue")
            var = input()
            if(var==''):
                variables_info = changed_variables(f, i)
                click.echo("line : "+str(i))
                
                #check if variable is changed or not
                if variables_info:
                    for j in range(len(variables_info)):
                        click.echo(variables_info[j][0] + " " + variables_info[j][1])
                else:
                    click.echo("No variable change!")
                    
    # delete all temp file created during execution   
    subprocess.call("rm *.txt", shell=True)
    subprocess.call("rm *.sh", shell=True)
