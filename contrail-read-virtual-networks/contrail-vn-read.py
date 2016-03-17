# VNC_API from Juniper
from vnc_api import vnc_api
import pprint

### PPRINT preparation
pp = pprint.PrettyPrinter(indent=4)

### API Information to login
api_server = '127.0.0.1'
api_port = 8082
api_user = 'admin'
api_password = 'contrail123'
api_tenant = 'admin'

### Start connection to server
vnc_lib = vnc_api.VncApi(username = api_user, password = api_password, tenant_name = api_tenant, api_server_host = api_server)

### Get all VNs and display them
all_vns = vnc_lib.virtual_networks_list()['virtual-networks']
#pp.pprint (all_vns)
print "-----------------------------------------"
print "|         List VNs in contrail          |"
print "-----------------------------------------"
print "\n** List all virtual-networks in Contrail:\n"
for vn in all_vns:
	print '* VM Net: ' + vn['fq_name'][2] 
	print '\t* Tenant: ' + vn['fq_name'][1] 
	print '\t* UUID Key: ' + vn['uuid']
	print '---'
