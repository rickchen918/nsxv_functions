# The goal of this script is to collect all ESG/DLR configuration with one script click 
# the script was creared for configuratio backup duing the customer environment simulation. 
# the file is not able to be reprovisioned, but it is able to be done by script modification 
# There is a known issue if esg name includes ":". the windows cant create file with that word. 

import requests,xml.dom.minidom
import xml.etree.ElementTree as ET

# You may need to modify the var here during the environment difference 
mgr="192.168.0.66"
user="admin"
passwd="Nicira123$"
api_ep="/api/4.0/edges/"
header={"Content-type":"application/xml"}

# Get ESG/DLR  summary list 
url="https://"+str(mgr)+str(api_ep)
conn=requests.get(url,verify=False,headers=header,auth=(user,passwd))
resp=conn.text
root=ET.fromstring(resp)

# Parse XML and create list for ESG objectID and ESG name for later input requirment 
eid_list=[]
for id in root.iter('objectId'):
    eid=id.text
    eid_list.append(eid)

ename_list=[]
for name in root.iter('name'):
    ename=name.text
    ename_list.append(ename)

ni=len(eid_list)
nj=len(ename_list)

print "The number ESG/DLR appliances is " + str(ni)

# Create while loop which refers the list of eid and ename. I will generate configuration file for indiviual
# appliance automatically 
i=0 
while i < ni:
    id=eid_list[i]
    name=ename_list[i]
    def backup(eid,ename):
	url="https://"+str(mgr)+str(api_ep)+eid
	conn=requests.get(url,verify=False,headers=header,auth=(user,passwd))
	resp=conn.text
	par=xml.dom.minidom.parseString(resp)
	data=par.toprettyxml()
	with open(ename+str(".txt"),'w') as conf:
	    conf.write(data)
    backup(id,name)
    i+=1
