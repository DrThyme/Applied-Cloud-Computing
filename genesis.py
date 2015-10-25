import os
import sys
import time
from novaclient.client import Client
import paramiko

PRIV_KEY_PATH = '/home/thyme/Downloads/cloud.key'
PUB_KEY_PATH = '/home/thyme/Downloads/cloud.key.pub'

## CREATED BY Brian Khuu
## MODIFIED BY Tim Josefsson
## update_pddrogress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\r####   Percent: [{0}] {1}% {2}    ####".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


img_name = 'Ubuntu Server 14.04 LTS (Trusty Tahr)'

config = {'username':os.environ['OS_USERNAME'], 
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL']}

nc = Client('2',**config)

if not nc.keypairs.findall(name='master_key'):
    with open(os.path.expanduser(PUB_KEY_PATH)) as fpubkey:
        nc.keypairs.create(name='master_key', public_key=fpubkey.read())
image = nc.images.find(name=img_name)
flavor = nc.flavors.find(name='m1.medium')


"""
Create the instance.
"""
print "##########################################"
print "####   INSTANCE CREATION HAS BEGUN    ####"
network = nc.networks.find(label='ext-net')
user_data = open('/home/thyme/Repository/Applied-Cloud-Computing/user_data.yml','r')
instance = nc.servers.create(name='thymeworks',
                            image = image,
                            flavor = flavor,
                            network = network,
                            key_name = 'master_key',
                            userdata = user_data) 

user_data.close()

status = instance.status
while status == 'BUILD':
	time.sleep(3)
	instance = nc.servers.get(instance.id)
	status = instance.status
print "####   BATTLE STATION OPERATIONAL!    ####"
print "##########################################"


"""
Attach floating ip to the instance.
"""
thymeworks_ip = 0
try:
	fip_set = 0
	fip_list = nc.floating_ips.list()
	for fip in fip_list:
		check_ip = nc.floating_ips.get(fip)
		if check_ip.fixed_ip == None:
			floating_ip = check_ip
			fip_set = 1
			break
	if fip_set == 0:
		floating_ip = nc.floating_ips.create(self.config['floating_ip_pool'])
	instance.add_floating_ip(floating_ip)
	thymeworks_ip = floating_ip.ip
	#print "thymeworks_main can be found at", floating_ip.ip 
except Exception as e:
    raise ProviderException("Failed to attach a floating IP to the controller.\n{0}".format(e))

"""
Show progress of cloud_init
"""
print "#### INSTANCE CONFIGURATION HAS BEGUN ####"
print "####      ESTIMATED TIME = 360s       ####"
print "##########################################"
print "####      PROGRESS OF CLOUD_INIT      ####"
for i in range(100):
	time.sleep(4.1)
	x = i/100.0
	update_progress(x)
print "\n##########################################"
print "###  ALL PROGRAMS OPERATIONAL"
print "###  thymeworks@{}".format(thymeworks_ip)
print "##########################################"
