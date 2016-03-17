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
print "|         Add VNs to contrail           |"
print "-----------------------------------------"

### Start connection to server
try:
	vnc_lib = vnc_api.VncApi(username = api_user, password = api_password, tenant_name = api_tenant, api_server_host = api_server)
except:
	print "Can't connect to API server, please check your credentials"

### collect tenant ID for demo-python tenant
tenant = vnc_lib.project_read( fq_name = 'default-domain:demo-python'.split(':') )

### Create IPAM for this tenant
ipam = vnc_api.NetworkIpam(
        name = 'ipam-default',
        parent_obj = tenant)
try:
	vnc_lib.network_ipam_create(ipam)
	print "* IPAM has been created without error"
except :
	print "!!! IPAM is already configured ... skipped"
print ""

print "* Manage first VN: vn-python-red"
### Create VN-RED
print "  * Create VN: vn-python-red"
red = vnc_api.VirtualNetwork( name = 'vn-python-red', parent_obj = tenant )

### Get IPAM information
ipam = vnc_lib.network_ipam_read(
        fq_name = 'default-domain:demo-python:ipam-default'.split(':'))

print "  * Create subnet for vn-python-red: 10.5.1.0/24"
subnet = vnc_api.SubnetType(
        ip_prefix = '10.5.1.0',
        ip_prefix_len = 24)

print "  * Create gateway for vn-python-red"
ipam_subnet = vnc_api.IpamSubnetType(
        subnet = subnet,
        default_gateway = '10.5.1.1')

print "  * Attach subnet to IPAM"
red.set_network_ipam(
        ref_obj = ipam,
        ref_data = vnc_api.VnSubnetsType([ipam_subnet]))

print "  * Install vn-python-red in contrail"
try:
	vnc_lib.virtual_network_create(red)
except:
	print "!!! Network already exist, please remove it before running this script"

print ""

# -----------------------------------------------------------------------------------# 

print "* Manage second VN: vn-python-blue"
### Create VN-RED
print "  * Create VN: vn-python-blue"
blue = vnc_api.VirtualNetwork( name = 'vn-python-blue', parent_obj = tenant )

### Get IPAM information
ipam = vnc_lib.network_ipam_read(
        fq_name = 'default-domain:demo-python:ipam-default'.split(':'))

print "  * Create subnet for vn-python-blue: 10.5.2.0/24"
subnet = vnc_api.SubnetType(
        ip_prefix = '10.5.2.0',
        ip_prefix_len = 24)

print "  * Create gateway for vn-python-blue"
ipam_subnet = vnc_api.IpamSubnetType(
        subnet = subnet,
        default_gateway = '10.5.2.1')

print "  * Attach subnet to IPAM"
blue.set_network_ipam(
        ref_obj = ipam,
        ref_data = vnc_api.VnSubnetsType([ipam_subnet]))

print "  * Install vn-python-red in contrail"
try:
	vnc_lib.virtual_network_create(blue)
except:
	print "!!! Network already exist, please remove it before running this script"
print ""

# -----------------------------------------------------------------------------------# 

print "* Setup policy between vn-python-red and vn-python-blue"
print "  * create a rule: ANY ANY ANY ANY Permit"
rule = vnc_api.PolicyRuleType(
        direction = '<>',
        protocol = 'any',
        action_list = vnc_api.ActionListType(simple_action = 'pass'),
        src_addresses = [vnc_api.AddressType(virtual_network = 'any')],
        src_ports = [vnc_api.PortType(start_port = -1, end_port = -1)],
        dst_addresses = [vnc_api.AddressType(virtual_network = 'any')],
        dst_ports = [vnc_api.PortType(start_port = -1, end_port = -1)])
print "  * Configure policy with previous rule"
policy = vnc_api.NetworkPolicy(
        name = 'python-policy',
        parent_obj = tenant,
        network_policy_entries = vnc_api.PolicyEntriesType([rule]))
try :
	print "  * Create policy in Contrail"
	vnc_lib.network_policy_create(policy)
except:
	print 

# -----------------------------------------------------------------------------------# 

print "* Attach policy (python-policy) to vn-python-red and vn-python-blue"
print "  * Look for python-policy"
policy = vnc_lib.network_policy_read(
        fq_name = 'default-domain:demo-python:python-policy'.split(':'))
policy_type = vnc_api.VirtualNetworkPolicyType(
        sequence = vnc_api.SequenceType(major = 0, minor = 0))

for vn_name in ["vn-python-red","vn-python-blue"]:
	print "  * Look for "+vn_name
	vn = vnc_lib.virtual_network_read(
	        fq_name = ['default-domain', 'demo-python', vn_name])
	vn.add_network_policy(
	        ref_obj = policy,
	        ref_data = policy_type)
	try:
		vnc_lib.virtual_network_update(vn)
		print "    * VN "+vn_name+" has been updated with policy python-policy"
	except:
		print "    * Can't update following VN: "+vn_name