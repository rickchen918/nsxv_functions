import requests,os,xml.dom.minidom,json,xmltodict

url="https://192.168.0.66/api/4.0/edges/edge-1"
nsx_username="admin"
nsx_password="Nicira123$"
header={"Content-type":"application/xml"}

conn=requests.get(url,auth=(nsx_username,nsx_password),verify=False)
resp=conn.text

par=xml.dom.minidom.parseString(resp)
xml=par.toprettyxml()

with open('esgconf','w') as file:
    file.write(xml)

