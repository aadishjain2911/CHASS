import subprocess

def preprocessing(f):
	rc=subprocess.call("sed -e 's/^[ \t]*#[^!].*$//g' -e 's/[ \t]#.*$//g' "+f+" | awk '{$1=$1};1' > copy.sh", shell=True)
