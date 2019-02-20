import urllib2 
import json 

def get_all_switches(): 
    url = "http://127.0.0.1:8080/v1.0/topology/switches" 
    req = urllib2.Request(url) 
    res_data = urllib2.urlopen(req) 
    res = res_data.read() 
    res = json.loads(res) 
    return res 

def get_all_links(): 
    url = "http://127.0.0.1:8080/v1.0/topology/links" 
    req = urllib2.Request(url) 
    res_data = urllib2.urlopen(req) 
    res = res_data.read() 
    res = json.loads(res) 
    return res 

def get_switch(dpid): 
    url = "http://127.0.0.1:8080/v1.0/topology/switches/" + dpid 
    req = urllib2.Request(url) 
    res_data = urllib2.urlopen(req) 
    res = res_data.read() 
    res = json.loads(res) 

    return res 
    

'''

 h1---s1---h3
      |
      |
      h2

Reglas: h1 talks to h3
- rule0: priority=0,arp,actions=output:flood
- rule1: priority=10,icmp,in_port=1,actions=output:3
- rule2: priority=10,icmp,in_port=3,actions=output:1
'''

def get_flow_entries(dpid): 
    url = "http://127.0.0.1:8080/stats/flow/" + dpid 
    req = urllib2.Request(url) 
    res_data = urllib2.urlopen(req) 
    res = res_data.read() 
    res = json.loads(res) 
    return res 

 

def add_flow_entry(dpid,match,priority,actions): 
    url = "http://127.0.0.1:8080/stats/flowentry/add" 
    post_data = "{'dpid':%s,'match':%s,'priority':%s,'actions':%s}" % (dpid,str(match),priority,str(actions)) 
    req = urllib2.Request(url,post_data) 
    res = urllib2.urlopen(req) 
    return res.getcode() 

 

def delete_flow_entry(dpid, match=None, priority=None, actions=None): 
    url = "http://127.0.0.1:8080/stats/flowentry/delete" 
    post_data = "{'dpid':%s" % dpid 
    if match is not None: 
        post_data += ",'match':%s" % str(match) 
    if priority is not None: 
        post_data += ",'priority':%s" % priority 
    if actions is not None: 
        post_data += ",'actions':%s" % str(actions) 
    post_data += "}" 

    req = urllib2.Request(url,post_data) 
    res = urllib2.urlopen(req) 
    return res.getcode()

 

'''

 h1---s1---h3
      |
      |
      h2

Reglas: h1 talks to h3
- rule0: priority=0,arp,actions=output:flood
- rule1: priority=10,icmp,in_port=1,actions=output:3
- rule2: priority=10,icmp,in_port=3,actions=output:1
- rule3: priority=20,in_port=1,icmp,actions=mod_dl_dst=00:00:00:00:00:02,output:2
- rule4: priority=20,in_port=2,icmp,dl_dst=00:00:00:00:00:03,output:3
- rule5: priority=20,in_port=3,icmp,actions=mod_dl_dst=00:00:00:00:00:02,output:2
- rule6: priority=20,in_port=2,icmp,dl_dst=00:00:00:00:00:01,output:1
''' 

print "add_flow_entry(dpid,match,priority,actions)"
print add_flow_entry('1',{"in_port":1,"dl_dst": "00:00:00:00:00:03","IP_PROTO":1},20,[{"type": "SET_DL_DST", "dl_dst": "00:00:00:00:00:02"},{"type":"OUTPUT","port":2}])
print add_flow_entry('1',{"in_port":2,"dl_dst": "00:00:00:00:00:03","IP_PROTO":1},20,[{"type":"OUTPUT","port":3}])
print add_flow_entry('1',{"in_port":3,"dl_dst": "00:00:00:00:00:01","IP_PROTO":1},20,[{"type": "SET_DL_DST", "dl_dst": "00:00:00:00:00:02"},{"type":"OUTPUT","port":2}])
print add_flow_entry('1',{"in_port":2,"dl_dst": "00:00:00:00:00:01","IP_PROTO":1},20,[{"type":"OUTPUT","port":1}])