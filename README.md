# CHASS
Code Hide And Seek Surveillance

A user friendly CLI debugging tool exclusively for bash scripts.
## Table of Content
* [Installation](#installation)

* [Usage](#usage)

   * [Default Mode](#default)
   
   * [Variable Mode](#variable)
   
   * [Variable Line Mode](#line)
   
   * [Code Line Mode](#code)
   
   * [Code Segment Mode](#codeline)
   
   * [Debug Particualar section Mode](#breakpoints)
   
   * [Function Mode](#function)
   
   * [Printall Mode](#printall)
   
   * [Printall Variable Mode](#printall_variable)
   
   * [Loops Mode](#loops)
   
   * [Conditions Mode](#conditions)
   
   * [Sed Mode](#sed)
   
   * [Actual Output Mode](#output)
   
   * [Expression Mode](#expr)
   
   * [PWD Mode](#pwd)
   
   * [Code at any point in Default Mode](#c)
   
   * [Quit](#quit)
   
* [Limitations](#limitations)

* [Contributing](#contributing)

---
<a name="installation">

## Installation

If you don't have virtualenv installed
```bash
sudo pip3 install virtualenv
```
Now make a virtual env inside the repo
```bash
python3 -m venv chassenv
```
Activate the virtual env
```bash
source chassenv/bin/activate
```
Now install the chass package
```bash
python3 -m pip install .
```
---
<a name="usage">
  
## Usage
For all options available

```bash
chass --help
```

File path is the argument that must be provided.

   <a name="default">
  
  #### Default mode(): 
  
   Get the value of changed variables lines by line (functions are to be dealt with separately using function mode given below)
    
   ```bash
   chass {path-to-file}
   ``` 
   <a name="variable">
   
   #### Variable mode():
   
   Get the value of specific multiple variables line by line
   
   ```bash
    chass {path-to-file} --variable={variable-name_1} --variable={variable-name_3_(optional)}
   ```
   
   or

   ```bash
   chass {path-to-file} -v {variable-name_1} -v {variable-name_2_(optional)}
   ```

   <a name="line">

   #### Variable at given line mode():
   
   Get the value of a specific variable at a specific line
   
   ```bash
   chass {path-to-file} --variable={variable-name} --line={line-number}
   ```
    
   or
   
   ```bash
   chass {path-to-file} -v {variable-name} -l {line-number}
   ```
   <a name="code">
  
   #### Code at a given line mode():
   
   Get code at a specified line
   ```bash
   chass {path-to-file} --code {line-number}
   ```
   or
   
   ```bash
   chass {path-to-file} -c {line-number}
   ```
   <a name="codeline">
  
   #### Get Particular segment of your code :
   
   Get a particular section of code present between two line numbers
    
   ```bash
   chass {path-to-file} --codeline {start-line-number} {end-line-number}
   ```
   <a name="breakpoints">
   
   #### Debug only a particular section of your code :
   
   Debugs only the section present between two line numbers
   
   ```bash
   chass {path-to-file} --breakpoints {start-line-number} {end-line-number}
   ```
   <a name="function">
   
   #### function mode() :
   
   Debug a function by providing the name of the function
   
   ```bash
   chass {path-to-file} -f {function_name}
   ```
   or
   
   ```bash
   chass {path-to-file} --function {function_name}
   ```
   <a name="printall">
   
   #### printall mode() :
   
   Prints all the changed variables' values at every line in one go
   
   ```bash
   chass {path-to-file} --printall
   ```
   or
   
   ```bash
   chass {path-to-file} -p
   ```
   <a name="printall_variable">
   
   #### printall values of given multiple variables mode() :
   
   Prints values of the given multiple variables at each line in one go 
   
   ```bash
   chass {path-to-file} --printall --variable={variable_name_1} --variable={variable_name_2(optional)}
   ```
   
   or
   
   ```bash
   chass {path-to-file} -p -v {variable_name_1} -v {variable_name_2(optional)}
   ```
   <a name="loops">
   
   #### loops mode():
   
   Debug only loops iteration wise
   
   ```bash
   chass {path-to-file} --loops
   ```
   
   or
   
   ```bash
   chass {path-to-file} -r
   ```
   <a name="conditions">
   
   #### conditions mode():
   
   Debug only conditions line by line
   
    
   ```bash
   chass {path-to-file} --cond
   ```
   or
   
    
   ```bash
   chass {path-to-file} -i
   ```
   <a name="sed">
   
   #### Debugging only sed commands mode():
   
   Debug only sed commands. You can specify line_number also to debug a specific sed command
   
   ```bash
   chass {path-to-file} --sed -l {line_number}(optional)
   ```
   
   or
   
   ```bash
   chass {path-to-file} -s -l {line_number}(optional)
   ```
   <a name="output">
   
   #### get actual output :
   
   Shows the actual output of the file
   
   ```bash
   chass {path-to-file} --output
   ```
   or
   
   ```bash
   chass {path-to-file} -o
   ```
   <a name="expr">
   
   #### EXPRESSION MODE ():
   
   At any given line you can write valid syntax bash expression involving any of defined variables. We will give value of that expression by using values of variables upto that line
   
   Step 1 :
   write expr in the default mode() at any line (Note: line should not be in any loop,if and case)
   
   ```bash
   expr
   ```
   
   Step 2 :
   write the expression in bash syntax
   
   ```bash
   {expression_to_be_calculated_in_valid_bash_syntax}
   ```
   <a name="pwd">
   
   #### PWD mode():
   
   At any line inside default mode() you can print working directory (Note: line should not be in any loop,if and case)
   
   ```bash
   pwd
   ```
   <a name="c">
  
   #### Get code of any particular line in Default mode():
   
   At any line inside default mode you can get the line written by you in the original code by just typing "c"
   
   ```bash
   c
   ```
   <a name="quit">
  
  #### Quit():
  
  You can exit the process at any stage by typing quit. If you are inside any loop, a single quit will get you out of the loop and typing quit again will terminate chass
  
  
  ```bash
   quit
   ```
  
---
<a name="limitations">
  
## Limitations

1. Absolute File paths should be given everywhere inside the code
2. Avoid using recursive functions for best usage
3. Any String should not contain " sed ", " cd " and other keywords as a part of it
4. Syntax of the file is assumed to be correct
5. rm command should not be present inside file

---
<a name="contributing">

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
