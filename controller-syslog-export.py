

import requests,time,getpass
requests.packages.urllib3.disable_warnings()

print " This script is to configure syslog exporter on nsx controller"

nsxmgr = raw_input("input nsx manager ip address: ")
nsx_username = raw_input("input nsx manager username: ")
nsx_password = getpass.getpass(prompt="input your password: ")
controller_id_1 = raw_input("input the 1st controller id which you need to configure: ")
controller_id_2 = raw_input("input the 2nd controller id which you need to configure: ")
controller_id_3 = raw_input("input the 3rd controller id which you need to configure: ")
syslog_server = raw_input("input syslog ip address: ")

def controller_syslog(controllerid):
    header={"Content-type":"application/xml"}
    url='''https://%s/api/2.0/vdn/controller/%s/syslog''' %(nsxmgr,controllerid)
    # The port 514 and udp type is hard code in this script for easy use. 
    body = """<controllerSyslogServer>
    <syslogServer>%s</syslogServer>
    <port>514</port>
    <protocol>UDP</protocol>
    <level>INFO</level>
    </controllerSyslogServer>
    """ %syslog_server

    conn=requests.post(url,verify=False,headers=header,auth=(nsx_username,nsx_password),data=body)
    print conn.status_code
    if conn.status_code == 200:
        print "\n"
        print "*" * 100	
        print " the api call is successful"
        print "*" * 100
        print "\n"
    elif conn.status_code == 500:
        print "\n"
        print "*" * 100
        print " the configuration is probably done before, check body return"
        print "*" * 100
        print "\n"
    else:
        print "\n"
        print "*" * 100    
        print "api call is failed"
        print "*" * 100
        print "\n"

    conn1=requests.get(url,verify=False,auth=(nsx_username,nsx_password))
    body_return=conn1.text
    if body.find(syslog_server) != -1:
        print "\n"
        print "*" * 100    
        print "the configuration is done, the body return is "
        print body_return
        print "*" * 100
        print "\n"
    else:
        print "\n"
        print "*" * 100
        print "configuration is not successful"
        print "*" * 100
        print "\n"

controller_syslog(controller_id_1)
time.sleep(5)
controller_syslog(controller_id_2)
time.sleep(5)
controller_syslog(controller_id_3)
