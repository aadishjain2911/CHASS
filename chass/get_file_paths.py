import os
from chass.locate_commands import locate_commands
import time

def get_path(file, num_lines, commands):
    temp_file = file
    pwd_file = open("pwd.txt", "w+")
    sh_file = open(file)
    isabs = os.path.isabs(file)
    if(isabs):
        basename = os.path.basename(file)
        file = file[:-len(basename)]
        pwd_file.write(str(file))
    else:
        curr_path = os.popen("pwd").read()
        curr_path_files = curr_path.split('/')
        basename = os.path.basename(file)
        file = file[:-len(basename)]
        file_paths = file.split('/')
        for f in file_paths:
            if f=='.':
                pass
            elif f=='..':
                curr_path_files = curr_path_files[:-1]
            else:
                curr_path_files.append(f)

        pwd_file.write("/".join(curr_path_files))
    
    time.sleep(0.1)
    #write at every line
    cmd_lst = []
    for (i, cmd) in commands:
        if cmd=='cd':
            cmd_lst.append(i)
    
    pwd_file.close()
    # print(cmd_lst)
    for i in range(1, num_lines-1):
        g = open("pwd.txt", "r+")
        lines = g.readlines()
        last_line = []
        last_line = lines[-1].split('/')
        if last_line[-1] == "":
            last_line.pop(len(last_line)-1)
        if len(cmd_lst) > 0:
            if cmd_lst[0] == i:
                cmd_lst.pop(0)
                t = os.popen("head -"+str(i+1)+" "+temp_file+" | tail -1").read()
                t = t[3:]
                temp = os.path.isabs(t)
                fp = t.split('/')
                if temp:
                    nfp = []
                    for sm in fp:
                        nfp.append(sm.replace('\n',''))
                    last_line = nfp
                else:
                    for f in fp:
                        nf = f.replace("\n", "")
                        if nf=='.':
                            pass
                        elif nf=='..':
                            last_line = last_line[:-1]
                        else:
                            last_line.append(nf) 
        g.write("\n")
        g.write("/".join(last_line))
        g.close()