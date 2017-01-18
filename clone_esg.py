# The script is to backup the deployed esg and convert the file to be  redployable 
# The backup filename output will be "esgbackup.xml"
import requests, xml.dom.minidom 
import xml.etree.ElementTree as ET
requests.packages.urllib3.disable_warnings()

# vsm login information 
nsxmgr_ip = "https://192.168.0.66"
nsxmgr_user = "admin"
nsxmgr_pass = "Nicira123$"

# edge endpoint infomation 
api_endpoint = "/api/4.0/edges/"
edge_id = "edge-26"
edge_new_pass = "!QAZ2wsx3edc"

# api call header
header={"Content-type":"application/xml"}
url = nsxmgr_ip+api_endpoint+edge_id

conn = requests.get(url,verify=False,headers=header,auth=(nsxmgr_user,nsxmgr_pass))
print conn.status_code
re_body = conn.text

# load the xml return into 
root = ET.fromstring(re_body)
id=root.find('id')
cli_element = root.find('cliSettings')

# remove id element, this should be striped during the reprovision 
root.remove(id)

new_element = ET.SubElement(cli_element, 'password')
new_element.text = edge_new_pass
#print ET.tostring(root)
se_body =  ET.tostring(root)

# use for testing format verification 
###################################################################################################
#url1 = nsxmgr_ip+api_endpoint
#conn1 = requests.post(url1,verify=False,headers=header,auth=(nsxmgr_user,nsxmgr_pass),data=se_body)
#print conn1.status_code
#print conn1.text 
###################################################################################################

parse = xml.dom.minidom.parseString(se_body)
format = parse.toprettyxml()

with open('esgbackup.xml','w') as file:
    file.write(format)

