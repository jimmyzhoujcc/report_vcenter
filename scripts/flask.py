#!/usr/bin/python

import json, os
from flask import Flask, request, redirect, url_for, send_from_directory
from pysphere import VIServer
import ssl

app = Flask(__name__)

# reserved for CF deployment
# port = int(os.getenv("VCAP_APP_PORT"))
port = 5000
# reserved for testing
# port = 8090
HOST = '192.168.1.4'
USER = "root"
PASSWORD = "vmware"


class Server:
    def __init__(self):
        self.server = VIServer()
        self.connect()

    def connect(self):
        try:
            # monkey-patch SSL module (uncomment if unneeded)
            # ssl._create_default_https_context = ssl._create_unverified_context
            ssl._create_default_https_context = ssl._create_unverified_context

            # self.server.connect(os.getenv("API_ADDRESS"), os.getenv("USER"), os.getenv("PASSWORD"))
            # self.server.connect(os.getenv("192.168.1.4"), os.getenv("root"), os.getenv("vmware"))
            self.server.connect(HOST, USER, PASSWORD)
        except Exception as e:
            return str(e)
        return False

    def disconnect(self):
        self.server.disconnect()


@app.route('/')
def root():
    html = """<html>
			<p>Welcome to pySpehere-flask, a RESTful API Server for VSphere</p>
			<br>
			<p>The following api calls are possible:</p>
			<ol>
			<li><p>/api/v1/monitor/api_version&nbsp;<a href='/api/v1/monitor/api_version'>Api Version</a> &nbsp; (GET)</p></li>
			<li><p>/api/v1/monitor/server_type&nbsp;<a href='/api/v1/monitor/server_type'>Server Type</a> &nbsp; (GET)</p></li>
			<li><p>/api/v1/monitor/registered_vms&nbsp;<a href='/api/v1/monitor/registered_vms'>Registered VMs</a> &nbsp;(GET)</p></li>
			<li><p>/api/v1/monitor/properties&nbsp;<a href='/api/v1/monitor/properties?vm_name=08server1'>VM Properties (exhaustive list)</a>&nbsp;(GET,&nbsp;POST)</p>
			<p>@param vm_name - The VM name</p></li>
			<li><p>/api/v1/monitor/property&nbsp;<a href='/api/v1/monitor/property?vm_name=08server1&property=ip_address'>VM Property</a>&nbsp;(GET,&nbsp;POST)</p>
			<p>@param vm_name - The VM name, @param property - Property to query</p>
			<p>This is the list of all the properties you can request:<br>
			<ul><li>name</li>
			<li>path</li>
			<li>guest_id</li>
			<li>guest_full_name</li>
			<li>hostname</li>
			<li>ip_address</li>
			<li>mac_address</li>
			<li>net</li></ul></li>
			<li><p>/api/v1/monitor/status&nbsp;<a href='/api/v1/monitor/status?vm_name=08server1'>VM Status</a>&nbsp;(GET,&nbsp;POST)</p>
			<p>@param vm_name - The VM name</p>
			<p>Status will print one of these strings:<br>
			<ul><li>POWERED ON</li>
			<li>POWERED OFF</li>
			<li>SUSPENDED</li>
			<li>POWERING ON</li>
			<li>POWERING OFF</li>
			<li>SUSPENDING</li>
			<li>RESETTING</li>
			<li>BLOCKED ON MSG</li>
			<li>REVERTING TO SNAPSHOT</li>
			</ul></p></li>
			<li><p>/api/v1/monitor/resource_pool_name&nbsp;<a href='/api/v1/monitor/resource_pool_name?vm_name=08server1'>VM Resource Pool Name</a>&nbsp;(GET,&nbsp;POST)</p>
			<p>@param vm_name - The VM name</p></li>
			</ol>
		</html>"""
    return html


@app.route('/api/v1/monitor/api_version', methods=['GET'])
def api_version():
    retval = "Nothing"
    try:
        con = Server()
        problems = con.connect()
        if problems:
            retval = json.dumps({'connect-exception': problems})
            return retval
        val = con.server.get_api_version()
        con.disconnect()
        retval = json.dumps({'api_version': val})
    except Exception as e:
        retval = json.dumps({'server-exception': str(e)})
    return retval


@app.route('/api/v1/monitor/server_type', methods=['GET'])
def server_type():
    try:
        con = Server()
        con.connect()
        retval = con.server.get_server_type()
        con.disconnect()
    except Exception as e:
        retval = e
    finally:
        return json.dumps({'server_type': retval})


@app.route('/api/v1/monitor/registered_vms', methods=['GET'])
def monitor_registered_vms():
    try:
        con = Server()
        con.connect()
        retval = con.server.get_registered_vms()
        con.disconnect()
    except Exception as e:
        retval = e
    finally:
        return json.dumps({'registered_vms': retval})


@app.route('/api/v1/monitor/properties', methods=['GET', 'POST'])
def monitor_properties():
    props = {}
    vm_name = None
    try:
        if request.method == 'GET':
            vm_name = request.args['vm_name']
        if request.method == 'POST':
            vm_name = request.get_json()['vm_name']
        con = Server()
        con.connect()
        vm = con.server.get_vm_by_name(vm_name)
        props = vm.get_properties()
        con.disconnect()
        remove_specific_key(props, "_obj")
    except Exception as e:
        props = e
    return json.dumps(props)


@app.route('/api/v1/monitor/status', methods=['GET', 'POST'])
def monitor_status():
    vm_name = None
    try:
        if request.method == 'GET':
            vm_name = request.args['vm_name']
        if request.method == 'POST':
            vm_name = request.get_json()['vm_name']
        con = Server()
        con.connect()
        vm = con.server.get_vm_by_name(vm_name)
        status = vm.get_status()
        con.disconnect()
    except Exception as e:
        status = e
    return json.dumps({'vm_status': status})


@app.route('/api/v1/monitor/property', methods=['GET', 'POST'])
def monitor_property():
    vm_name = None
    property = None
    try:
        if request.method == 'GET':
            vm_name = request.args['vm_name']
            property = request.args['property']
        if request.method == 'POST':
            vm_name = request.get_json()['vm_name']
            property = request.get_json()['property']
        if property in ['name', 'path', 'guest_id', 'guest_full_name', 'hostname', 'ip_address', 'mac_address', 'net']:
            con = Server()
            con.connect()
            vm = con.server.get_vm_by_name(vm_name)
            prop = vm.get_property(property)
            con.disconnect()
        else:
            prop = 'Unsupported'
    except Exception as e:
        prop = e
    return json.dumps({property: prop})


@app.route('/api/v1/monitor/resource_pool_name', methods=['GET', 'POST'])
def monitor_resource_pool():
    vm_name = None
    try:
        if request.method == 'GET':
            vm_name = request.args['vm_name']
        if request.method == 'POST':
            vm_name = request.get_json()['vm_name']
        con = Server()
        con.connect()
        vm = con.server.get_vm_by_name(vm_name)
        pool = vm.get_resource_pool_name()
        con.disconnect()
    except Exception as e:
        pool = e
    return json.dumps({'resource_pool_name': pool})


@app.route('/api/v1/snapshots/list', methods=['GET', 'POST'])
def snapshots_list():
    vm_name = None
    try:
        if request.method == 'GET':
            vm_name = request.args['vm_name']
        if request.method == 'POST':
            vm_name = request.get_json()['vm_name']
        con = Server()
        con.connect()
        vm = con.server.get_vm_by_name(vm_name)
        snapshot_list = vm.get_snapshots()
        con.disconnect()
    except Exception as e:
        snapshot_list = e
    return json.dumps({'snapshot_list': snapshot_list})


"""
http://stackoverflow.com/questions/10179033/how-to-recursively-remove-certain-keys-from-a-multi-dimensionaldepth-not-known
"""


def remove_specific_key(the_dict, rubbish):
    """Used to remove the _obj references from pySphere requests that are un-jsonifyable"""
    if the_dict.has_key(rubbish):
        the_dict.pop(rubbish)
    else:
        for key in the_dict:
            if isinstance(the_dict[key], dict):
                remove_specific_key(the_dict[key], rubbish)
            elif isinstance(the_dict[key], list):
                if the_dict[key].count(rubbish):
                    the_dict[key].remove(rubbish)
    return the_dict


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port)
