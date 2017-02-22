# This script is using for rule generation 
import requests,xml.dom.minidom
requests.packages.urllib3.disable_warnings()

nsxmgr="192.168.0.66"
nsx_username="admin"
nsx_password="Nicira123$"

dfw_section="/api/4.0/firewall/globalroot-0/config/layer3sections"
dfw_conf="/api/4.0/firewall/globalroot-0/config"

def c_body(b,c):
    template=''
    template+="<section name = 'lab_rules'>"
    i=1
    j=1
    while i < b:
	while j < c:
	    template+="""<rule disabled='false' logged='true'>
<name>test_%s</name>
<action>ALLOW</action>
<sources excluded='false'>
<source>
<value>1.1.%s.%s</value>
<type>Ipv4Address</type>
<isValid>true</isValid>
</source>
</sources>
<destinations excluded="false">
<destination>
<value>2.2.%s.%s</value>
<type>Ipv4Address</type>
<isValid>true</isValid>
</destination>
</destinations>
</rule>""" %(i,i,j,i,j)  
            j=j+1
        i=i+1
    template+="\n</section>"
    return template

def create_section():
    url="https://"+nsxmgr+dfw_section
#   print url
    header={"Content-type":"application/xml"}
#    print body
    conn=requests.post(url,verify=False,headers=header,auth=(nsx_username,nsx_password),data=body)
    print conn.status_code
    resp=conn.text
    par=xml.dom.minidom.parseString(resp)
    result=par.toprettyxml()
    print result

def q_rules():
    url="https://"+nsxmgr+dfw_conf
    conn=requests.get(url,verify=False,auth=(nsx_username,nsx_password))
    print conn.status_code
    resp=conn.text
    par=xml.dom.minidom.parseString(resp)
    result=par.toprettyxml()
    print result


body=c_body(2,255)
print body
create_section()
#q_rules()
