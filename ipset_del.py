# the script is remove the all ipsets to recover from test environment
import requests,xml.dom.minidom
requests.packages.urllib3.disable_warnings()
import xml.etree.ElementTree as ET


gen=2

nsxmgr="192.168.0.30"
nsx_username="admin"
nsx_password="Nicira123$"

ep="/api/2.0/services/ipset/scope/globalroot-0"
url="https://"+nsxmgr+ep
header={"Content-type":"application/xml"}

# retrieve the ipset info list 
conn=requests.get(url,verify=False,headers=header,auth=(nsx_username,nsx_password))
resp=conn.text
root=ET.fromstring(resp)

objid=[]
for id in root.iter('objectId'):
    objid.append(id.text)

# delete created ipset 
for x in objid:
    ep="/api/2.0/services/ipset/%s"%x
    url="https://"+nsxmgr+ep
    conn=requests.delete(url,verify=False,auth=(nsx_username,nsx_password))
    print conn.status_code

