import psutil
import subprocess
from netstat import netstat

"""
print "hola"
for proc in psutil.process_iter(attrs=['pid', 'name']):
    if "mininet" in proc.info['name']:
        print proc.info['name']
"""

"""
sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py


sudo mn --topo=single,3 --mac --switch=ovsk,protocols=OpenFlow13 --controller=remote,ip=127.0.0.1:6653  --link=tc,bw=100 
"""

pl = subprocess.Popen(['ps', '-ax','-o','pid,cmd'], stdout=subprocess.PIPE).communicate()[0]
#print pl
lines = pl.split('\n')
mininet_lines = []
for l in lines:
    if "mininet" in l:
        mininet_lines.append(l)
    

print mininet_lines
dicProcesos = {}
for p in mininet_lines:
    l = p.split()
    if ("h" in l[-1]) or ("s" in l[-1]):        
        # print l
        # Agregando hosts y el swith
        node = l[-1]
        dicProcesos[node[node.find(':')+1:]] = int(l[0])

port = 6653
for conn in netstat():
    # print conn
    if str(6653) in conn[2] and ('0.0.0.0' in conn[2]):
        dicProcesos['c0'] = int(conn[5]) 

# print dicProcesos

# informacion de los procesos  
# https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/
procesos = []

for k in dicProcesos:
    p = psutil.Process(dicProcesos[k])
    dic_attr = p.as_dict(attrs=['pid', 'name', 'cpu_percent'])
    print(k,dic_attr['pid'],dic_attr['cpu_percent'])







   