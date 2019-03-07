import psutil
import subprocess

"""
print "hola"
for proc in psutil.process_iter(attrs=['pid', 'name']):
    if "mininet" in proc.info['name']:
        print proc.info['name']
"""


pl = subprocess.Popen(['ps', '-ax','-o','pid,cmd'], stdout=subprocess.PIPE).communicate()[0]
#print pl
lines = pl.split('\n')
mininet_lines = []
for l in lines:
    if "mininet" in l:
        mininet_lines.append(l)
    elif "controller" in l:
        mininet_lines.append(l)

print mininet_lines
dicProcesos = {}
for p in mininet_lines:
    l = p.split()
    if "mininet" in p:        
        dicProcesos[l[-1]] = int(l[0])
    else:
        dicProcesos[l[1]] = int(l[0])

print dicProcesos

# informacion de los procesos  
# https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/
procesos = []
for k in dicProcesos:
    p = psutil.Process(dicProcesos[k])
    print(p.as_dict(attrs=['pid', 'name', 'cpu_percent']))








   