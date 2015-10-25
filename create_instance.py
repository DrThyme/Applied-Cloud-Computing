import os
import sys
import time
from novaclient.client import Client
import paramiko

PRIV_KEY_PATH = '/home/thyme/Downloads/cloud.key'
PUB_KEY_PATH = '/home/thyme/Downloads/cloud.key.pub'

img_name = 'MOLNS_OpenStack_accpro4_1444644885'


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
network = nc.networks.find(label='ext-net')
user_data = open('/home/thyme/School/Applied-Cloud-Computing/user_data.yml','r')
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
print "Battlestation operational!"

"""
Attach floating ip to the instance.
"""
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
	print "thymeworks_main can be found at", floating_ip.ip 
except Exception as e:
    raise ProviderException("Failed to attach a floating IP to the controller.\n{0}".format(e))

