# contrail-python-demo
A Python demo to manage Contrail with scripts

## About
This repository provides some scripts to demonstrate how to configure Contrail by using Python library. It provides some basic examples for the following tasks:
- Read virtual-network information
- Create virtual-network
- Create IPAM and POLICY for given virtual-networks
- Delete virtual-network / IPAM / Policy from contrail

All scripts are located under their own directory
```
contrail-python-demo
├── contrail-create-virtual-networks
│   └── contrail-vn-create.py
├── contrail-delete-virtual-networks
│   └── contrail-delete-vn.py
├── contrail-read-virtual-networks
│   └── contrail-vn-read.py
├── LICENSE
└── README.md
```

## Setup environment:
### Setup Python for windows
The easiest way to run these scripts is to execute them from your contrail / Openstack server since all required packages are part of the initial setup.

### Install VNC_API module

To use VNC_API module provided by contrail, 2 different options are available:
- Run scripts directly on the Contrail server
- Install VNC_API client in your environment. Python module is available in the [contrail-controller repository](https://github.com/Juniper/contrail-controller/blob/master/src/api-lib/vnc_api.py)

## Script usage
All scripts are using static authentication information. You can change them to match your lab information

```python
api_server = '127.0.0.1'		# IP of your server
api_port = 8082					# Default port to send your API request
api_user = 'demo-python'		# Username configured to execute these scripts
api_password = 'contrail123'	# User Password
```

##Contributing

- Fork it
- Create your feature branch (git checkout -b my-new-feature)
- Commit your changes (git commit -am 'Add some feature')
- Push to the branch (git push origin my-new-feature)
- Create new Pull Request

##Author
* Thomas Grimonet / Juniper Networks / [Twitter](https://www.twitter.com/titom73)
* Khelil Sator / Juniper Networks
