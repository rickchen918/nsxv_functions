#configure secondary ip address on nsx edge 
import requests,xml.dom.minidom,pdb
import xml.etree.ElementTree as ET

mgr="192.168.0.66"
user="admin"
passwd="Nicira123$"
header={"Content-type":"application/xml"}
sec_ip="192.168.64.14"

def nic(edgeid,vnic,sec_ip):
    api_ep="/api/4.0/edges/%s/vnics/%s"%(edgeid,vnic)
    url="https://"+str(mgr)+str(api_ep)

# get vnic xml return and modify xml as next call body
    conn=requests.get(url,verify=False,headers=header,auth=(user,passwd))
    resp=conn.text
    root=ET.fromstring(resp)
    for position in root.iter('addressGroup'):
# identify secondary ip address section
# if it existed, add ipAddress section under secondaryAddresses
# XML subelement adding by ET.SubElement under secondaryAddresses
	try:
	    secaddr=position.find('secondaryAddresses').tag # check if secondaryAddress element existed
	    for addr in root.iter('secondaryAddresses'): # if it exists 
		ipaddr=ET.SubElement(addr,'ipAddress') # create subelement new ipAddress element
		ipaddr.text='%s'%sec_ip # upate ip address in the element 
		addr.append(ipaddr) # append new created tree under position (iter addressGroup)
		print "secondary section is existed"
		print(ET.tostring(root))
		body=ET.tostring(root)
# if is is existed, add secondaryAddresses and ipAddress section 
	except AttributeError:
	    secaddr=ET.Element('secondaryAddresses') # create element secondaryAddress 
	    ipaddr=ET.SubElement(secaddr,'ipAddress') # create subelement ipAddress
	    ipaddr.text='%s'%sec_ip # update ip address under ipAddress subelement
	    position.append(secaddr) # append new created tree under position (iter addressGroup)
	    print("create new section for secondary")
	    print(ET.tostring(root)) # dump XML to review
            body=ET.tostring(root)

    conn1=requests.put(url,verify=False,headers=header,data=body,auth=(user,passwd))
    resp=conn1.status_code
    print resp


nic("edge-18","0","%s"%sec_ip)

