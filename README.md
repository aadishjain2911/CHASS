# CHASS
Code Hide And Seek Surveillance

A user friendly CLI debugging tool exclusively for bash scripts.
## Table of Content
[Installation](#installation)

[Usage](#usage)

[Contributing](#contributing)

---

## Installation

If you don't have virtualenv installed
```bash
sudo pip3 install virtualenv
```
Now set up make a virtual env inside the repo
```bash
python3 -m venv chassenv
```
Actiavte the vitual env
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

### Default mode(): 

```bash
chass {path-to-file}
``` 
Get the value of changed variables lines by line

### Variable mode():
```bash
chass {path-to-file} {--variable/-v}={variable-name}
```
Get the value of specific variable line by line

### Variable at given line mode():
```bash
chass {path-to-file} {--variable/-v}={variable-name} {--line/-l}={line-number}
```  
Get the value of a specific variable at a specific line

---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
