# the script is to gen number of ipsets for tsmc testin 
import requests,xml.dom.minidom
requests.packages.urllib3.disable_warnings()

igen=4
jgen=254

nsxmgr="192.168.0.30"
nsx_username="admin"
nsx_password="Nicira123$"

ep="/api/2.0/services/ipset/globalroot-0"
url="https://"+nsxmgr+ep
header={"Content-type":"application/xml"}

i=0
j=0

while i < igen:
    while j < jgen:
    	name="ipset%s-%s"%(i,j)
   	body="""
	<ipset>
	<objectId></objectId>
	<type>
	<typeName>IPSet</typeName>
	</type>
	<description></description>
	<name>%s</name>
	<objectTypeName>GlobalRoot</objectTypeName>
	<value>1.1.%s.%s</value>
	<inheritanceAllowed>false</inheritanceAllowed>
	</ipset>
	"""%(name,i,j)
        j=j+1
        print body
        # api call to create ipset 
        conn=requests.post(url,verify=False,headers=header,auth=(nsx_username,nsx_password),data=body)
        print conn.status_code
        print conn.text
    j=0
    i=i+1
