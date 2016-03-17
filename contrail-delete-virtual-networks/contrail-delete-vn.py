# VNC_API from Juniper
from vnc_api import vnc_api
import pprint

### PPRINT preparation
pp = pprint.PrettyPrinter(indent=4)

### API Information to login
api_server = '127.0.0.1'
api_port = 8082
api_user = 'demo-python'
api_password = 'contrail123'
api_tenant = 'demo-python'

print "-----------------------------------------"
print "|      Delete VNs From contrail         |"
print "-----------------------------------------"

### Start connection to server
try:
	vnc_lib = vnc_api.VncApi(username = api_user, password = api_password, tenant_name = api_tenant, api_server_host = api_server)
except:
	print "Can't connect to API server, please check your credentials"


### collect tenant ID for demo-python tenant
tenant = vnc_lib.project_read( fq_name = 'default-domain:demo-python'.split(':') )


### Remove all networks created in ../contrail-create-virtual-networks/
for vn_name in ["vn-python-red","vn-python-blue"]:
	print "* Remove VN "+vn_name+" from contrail"
	try:
		vnc_lib.virtual_network_delete(fq_name = ['default-domain', 'demo-python', vn_name])
	except:
		print "  ! Can't delete "+vn_name+" - Please check if network exists in contrail"


### Remove all IPAMs created in ../contrail-create-virtual-networks/
print "* Delete IPAM for python-demo tenant"
try:
	vnc_lib.network_ipam_delete( fq_name = 'default-domain:demo-python:ipam-default'.split(':') )
except:
	print "  ! Can't delete default-domain:demo-python:ipam-default - Please check if network exists in contrail"


### Remove Policy created in ../contrail-create-virtual-networks/ from contrail
print "* Delete Netowrk Policy for python-demo tenant"
try:
	vnc_lib.network_policy_delete( fq_name = 'default-domain:demo-python:python-policy'.split(':') )
except:
	print "  ! Can't delete default-domain:demo-python:ipam-default - Please check if network exists in contrail"