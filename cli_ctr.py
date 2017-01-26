# The usage description has to be on top of all lines 

'''Usage:
    clictr.py list -vsmip <nsxmgr_ip> -vsmuser <nsx_username> -vsmpass <nsx_password>  
    clictr.py syslogset -vsmip <nsxmgr_ip> -vsmuser <nsx_username> -vsmpass <nsx_password> -id <ctr_id> -logserver <syslog_ip>
    clictr.py syslogdel -vsmip <nsxmgr_ip> -vsmuser <nsx_username> -vsmpass <nsx_password> -id <ctr_id> 
'''

# the imp module can check the module availability, before running processs
import imp
try: 
    imp.find_module('docopt')
except ImportError:
    print '*'*100
    print "docopt module is required to run command. you can get the module by 'pip install docopt ' "
    print '*'*100
    exit()

from docopt import docopt

if __name__ == '__main__':
    var = docopt(__doc__)

#print var

import requests,re,xml.dom.minidom
requests.packages.urllib3.disable_warnings()

nsxmgr=var['<nsxmgr_ip>']
nsx_username=var['<nsx_username>']
nsx_password=var['<nsx_password>']
syslog_server=var['<syslog_ip>']
header={"Content-type":"application/xml"}

def controller_list():
    api_endpoint="/api/2.0/vdn/controller"
    url="https://%s%s" %(nsxmgr,api_endpoint)
    conn=requests.get(url,verify=False,auth=(nsx_username,nsx_password))
    print conn.status_code
    body=conn.text
    par=xml.dom.minidom.parseString(body)
    xmlformat=par.toprettyxml()
    result=re.findall("<id>controller.*</id>",xmlformat)
    for ctrid in result:
        print '*' * 100
	print "The controller id is: %s " %(ctrid).strip('</id>')
        print '*' * 100

def syslog_conf(controller_id):
    api_endpoint="/api/2.0/vdn/controller/%s/syslog" %(controller_id)
    url="https://%s%s" %(nsxmgr,api_endpoint)    
    body = '''<controllerSyslogServer>
    <syslogServer>%s</syslogServer>
    <port>514</port>
    <protocol>UDP</protocol>
    <level>INFO</level>
    </controllerSyslogServer>
    ''' %syslog_server

    conn=requests.post(url,verify=False,headers=header,auth=(nsx_username,nsx_password),data=body)
    print conn.status_code
    if conn.status_code == 200:
        print "\n"
        print "*" * 100
        print " the api call is successful  " + str(controller_id)
        print "*" * 100
        print "\n"
    elif conn.status_code == 500:
        print "\n"
        print "*" * 100
        print str(controller_id)+" configuration is probably done before, check body return"
        print "*" * 100
        print "\n"
    else:
        print "\n"
        print "*" * 100
        print "api call is failed  " +str(controllerid)
        print "*" * 100
        print "\n"

    conn1=requests.get(url,verify=False,auth=(nsx_username,nsx_password))
    body_return=conn1.text
    if body.find(syslog_server) != -1:
#        print "\n"
#        print "*" * 100
        print str(controller_id)+ " configuration is done, the body return is "
        print body_return
        print "*" * 100
        print "\n"
    else:
        print "\n"
        print "*" * 100
        print str(controller_id)+ " configuration is not successful"
        print "*" * 100
        print "\n"

def syslog_del(controller_id):
    api_endpoint="/api/2.0/vdn/controller/%s/syslog" %(controller_id)
    url="https://%s/api/2.0/vdn/controller/%s/syslog" %(nsxmgr,controller_id)
    conn=requests.delete(url,verify=False,headers=header,auth=(nsx_username,nsx_password))
    print conn.status_code
    if conn.status_code == 200:
        print "\n"
        print "*" * 100
        print " the api call is successful  " + str(controller_id)
        print "*" * 100
        print "\n"
    else:
        print "\n"
        print "*" * 100
        print "api call is failed  " +str(controller_id)
        print "*" * 100
        print "\n"



if var['syslogset'] == True:
    idlist = var['<ctr_id>'].split(',')
    for id in idlist:
        idinput = "%s" %(id)
        syslog_conf(idinput)
elif var['syslogdel'] == True:
    idlist = var['<ctr_id>'].split(',')
    for id in idlist:
        idinput = "%s" %(id)
        syslog_del(idinput)
elif var['list'] == True:
    controller_list()
else:
    pass
    
