from novaclient.client import Client

config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

nc = Client('2',**config)

"""
Create the instance.
"""
image = nc.images.find(name='Ubuntu Server 14.04 LTS (Trusty Tahr)')
flavor = nc.flavors.find(name='m1.medium')
network = nc.networks.find(label='ext-net')
user_data = '/home/thyme/School/Applied-Cloud-Computing/user_data.yml'
isntance = nc.servers.create(name='thymeworks_main',
                            image = image.id,
                            flavor = flavor.id,
                            network = network.id,
                            key_name = keypair.name,
                            userdata = user_data) 

"""
Attach floating ip to the instance.
"""
try:
	fip_set = 0
	fip_list = self.nova.floating_ips.list()
	for fip in fip_list:
		check_ip = self.nova.floating_ips.get(fip)
		if check_ip.fixed_ip == None:
			floating_ip = check_ip
			fip_set = 1
			break
	if fip_set == 0:
		floating_ip = self.nova.floating_ips.create(self.config['floating_ip_pool'])
	instance.add_floating_ip(floating_ip)
except Exception as e:
    raise ProviderException("Failed to attach a floating IP to the controller.\n{0}".format(e))

