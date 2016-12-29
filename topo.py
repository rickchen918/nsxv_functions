import requests,json,xmltodict,os
nsxmgr="192.168.0.66"
nsx_username="admin"
nsx_password="Nicira123$"
header={"Content-type":"application/xml"}

# create the logical switch creation function call 
def lsw_create(lsw_name):
    url="https://%s/api/2.0/vdn/scopes/vdnscope-1/virtualwires" %nsxmgr
    body="""<virtualWireCreateSpec><name>%s</name><description></description>
            <tenantId></tenantId><controlPlaneMode>UNICAST_MODE</controlPlaneMode>
            <guestVlanAllowed>true</guestVlanAllowed></virtualWireCreateSpec>""" %(lsw_name)
    
    print body
    conn=requests.post(url,auth=(nsx_username,nsx_password),verify=False,data=body,headers=header)
    resp_code=conn.status_code
    if resp_code != 201:
	print "the connection is not success"
	exit() 
    else:
        pass
    resp_raw=conn.text
    with open('dict','a') as file:
	file.write(resp_raw+str(','))
    conn.close()

# The number of logical switch to create by while loop	
i=1
while i < 3:
	lsw_create("switch"+str(i))
	i+=1

# append the api retun into list for edge attachment
with open('dict') as list:
    text=list.read().split(",")
    lsw0=text[0]
    lsw1=text[1]

def esg_create(esg_name):
    with open('vnic.json') as vnic:
	text=vnic.read()
	js=json.loads(text)
   
    vnic0=js['vnic']['vnic0']
    vnic1=js['vnic']['vnic1']

    url="https://192.168.0.66/api/4.0/edges"
    input=open("esg_template.xml").read()
    body=input %(esg_name,vnic0['name'],vnic0['type'],lsw0,vnic0['ip'],vnic0['mask'],vnic0['status'],\
		vnic1['name'],vnic1['type'],lsw1,vnic1['ip'],vnic1['mask'],vnic1['status'])
    conn=requests.post(url,verify=False,headers=header,auth=(nsx_username,nsx_password),data=body)
    print conn.status_code
    print conn.text
    resp_code=conn.status_code
    if resp_code != 201:
        print "the connection is not success"
        exit()
    else:
        pass    

    conn.close()

esg_create('python_test')
os.system("rm dict")
