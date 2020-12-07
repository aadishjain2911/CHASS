# CHASS
Code Hide And Seek Surveillance

A user friendly CLI debugging tool exclusively for bash scripts.
## Table of Content
* [Installation](#installation)

* [Usage](#usage)

   * [Default Mode](#default)
   
   * [Variable Mode](#variable)
   
   * [Variable Line Mode](#line)
   
* [Contributing](#contributing)

---

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

## Usage
For all options available

```bash
chass --help
```

File path is the argument that must be provided.

   <a name="default">
  
  #### Default mode(): 
  
   Get the value of changed variables lines by line
    
   ```bash
   chass {path-to-file}
   ``` 
   <a name="variable">
   
   #### Variable mode():
   
   Get the value of specific variable line by line
   
   ```bash
    chass {path-to-file} --variable={variable-name}
   ```
   
   or

   ```bash
   chass {path-to-file} -v {variable-name}
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
   
   #### Code at a given line mode():
   
   Get code at a specified line
   ```bash
   chass {path-to-file} --code {line-number}
   ```
   or
   
   ```bash
   chass {path-to-file} -c {line-number}
   ```
   
   #### Get Particular segment of your code :
   
   Get a particular section of code present between two line numbers
    
   ```bash
   chass {path-to-file} --codeline {start-line-number} {end-line-number}
   ```
   
   #### Debug only a particular section of your code :
   
   Debugs only the section present between two line numbers
   
   ```bash
   chass {path-to-file} --breakpoints {start-line-number} {end-line-number}
   ```
   
   #### function mode() :
   
   Debug a function by providing the name of the function
   
   ```bash
   chass {path-to-file} -f {function_name}
   ```
   or
   
   ```bash
   chass {path-to-file} --function {function_name}
   ```
   
   #### printall mode() :
   
   Prints all the changed variables' values at every line in one go
   
   ```bash
   chass {path-to-file} --printall
   ```
   or
   
   ```bash
   chass {path-to-file} -p
   ```
   
   #### get actual output :
   
   Shows the actual output of the file
   
   ```bash
   chass {path-to-file} --output
   ```
   or
   
   ```bash
   chass {path-to-file} -o
   ```
   
   #### EXPRESSION MODE ():
   
   At any given line you can write valid syntax bash expression involving any of defined variables. We will give value of that expression by using values of variables upto that line
   
   Step 1 :
   write expr in the default mode() at any line
   
   ```bash
   expr
   ```
   
   Step 2 :
   write the expression in bash syntax
   
   ```bash
   {expression_to_be_calculated_in_valid_bash_syntax}
   ```
   
---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
