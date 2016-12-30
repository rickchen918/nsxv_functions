# the script is to remove syslog server for nsx controller. The function is not provided on UI currently. 
# the script is testing under nsx-vsphere 6.2.4

import requests,time,getpass
requests.packages.urllib3.disable_warnings()

print " This script is to remove  syslog exporter on nsx controller"

nsxmgr = raw_input("input nsx manager ip address: ")
nsx_username = raw_input("input nsx manager username: ")
nsx_password = getpass.getpass(prompt="input your password: ")
controller_id_1 = raw_input("input the 1st controller id which you need to configure: ")
controller_id_2 = raw_input("input the 2nd controller id which you need to configure: ")
controller_id_3 = raw_input("input the 3rd controller id which you need to configure: ")

def controller_syslog(controllerid):
    header={"Content-type":"application/xml"}
    url='''https://%s/api/2.0/vdn/controller/%s/syslog''' %(nsxmgr,controllerid)
    conn=requests.delete(url,verify=False,headers=header,auth=(nsx_username,nsx_password))
    print conn.status_code
    if conn.status_code == 200:
        print "\n"
        print "*" * 100	
        print " the api call is successful  " + str(controllerid)
        print "*" * 100
        print "\n"
    elif conn.status_code == 500:
        print "\n"
        print "*" * 100
        print str(controllerid)+" configuration is probably done before, check body return"
        print "*" * 100
        print "\n"
    else:
        print "\n"
        print "*" * 100    
        print "api call is failed  " +str(controllerid)
        print "*" * 100
        print "\n"

controller_syslog(controller_id_1)
time.sleep(5)
controller_syslog(controller_id_2)
time.sleep(5)
controller_syslog(controller_id_3)
