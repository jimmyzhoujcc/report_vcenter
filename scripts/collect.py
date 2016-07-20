#!/usr/bin/env python
from django.db import models
from django.db.models import Sum
from pysphere import VIServer, MORTypes, VIProperty
from optparse import OptionParser
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import MySQLdb

"""
from models import VirtualNic
from models import Hypervisor
from models import Datastore
from models import Interface
from models import Vswitch
from models import Network
from models import Guest
from models import Disk
"""


from os.path import expanduser
from sys import exit
import ConfigParser
import re

def vmware_connect(host, user, password):
    """Return a VIServer conneciont"""
    s = VIServer()
    s.connect(host, user, password)
    return s


def get_disks(vm):
    """Return a list of disk dict with keys name, size, thin, raw, filename"""
    ret_val = []

    disks = [d for d in vm.properties.config.hardware.device
             if d._type == 'VirtualDisk' and d.backing._type in
             ['VirtualDiskFlatVer1BackingInfo',
              'VirtualDiskFlatVer2BackingInfo',
              'VirtualDiskRawDiskMappingVer1BackingInfo',
              'VirtualDiskSparseVer1BackingInfo',
              'VirtualDiskSparseVer2BackingInfo']]

    for disk in disks:
        name = disk.deviceInfo.label
        size = int(disk.deviceInfo.summary.replace(',', '').replace(' KB', ''))
        size /= 1024
        filename = disk.backing.fileName
        raw = thin = False
        if disk.backing._type == 'VirtualDiskRawDiskMappingVer1BackingInfo':
            raw = True
        if hasattr(disk.backing, "thinProvisioned"):
            thin = True
        ret_val.append({'name': name, 'size': size, 'thin': thin,
                        'raw': raw, 'filename': filename})
    print ret_val
    return ret_val


def get_datastores(server):
    """Return a list of datastore dict with keys name, capacity, freeSpace"""
    ret_val = []
    for ds_mor, name in server.get_datastores().items():
        props = VIProperty(server, ds_mor)
        capacity = props.summary.capacity / 1024 / 1024
        freeSpace = props.summary.freeSpace / 1024 / 1024
        ret_val.append({'name': name,
                        'capacity': capacity,
                        'freeSpace': freeSpace})
    #print ret_val
    return ret_val


def get_networks(server):
    """Return a list a network dict with keys name, vlanId, vswitchName"""
    mor, name = server.get_hosts().items()[0]
    prop = VIProperty(server, mor)
    ret_val = []
    for network in prop.configManager.networkSystem.networkInfo.portgroup:
        name = network.spec.name
        vlanId = network.spec.vlanId
        vswitchName = network.spec.vswitchName
        ret_val.append({'name': name,
                        'vlanId': vlanId,
                        'vswitchName': vswitchName})
    print ret_val
    return ret_val


def get_interfaces(prop):
    """Return a list of interface dict with keys driver, linkSpeed, mac,
    name"""
    ret_val = []
    for interface in prop.configManager.networkSystem.networkInfo.pnic:
        name = interface.device
        mac = interface.mac
        driver = interface.driver
        try:
            linkSpeed = interface.linkSpeed.speedMb
        except:
            try:
                linkSpeed = interface.spec.linkSpeed.speedMb
            except:
                linkSpeed = 0
        ret_val.append({'name': name,
                        'mac': mac,
                        'driver': driver,
                        'linkSpeed': linkSpeed})

    return ret_val


def get_vnics(vm):
    """Return a list of vnic dict with keys name, mac, type, network"""
    ret_val = []
    for v in vm.get_property("devices").values():
        if v.get('macAddress'):
            name = v.get('label')
            mac = v.get('macAddress')
            driver = v.get('type')
            network = v.get('summary')
            ret_val.append({'name': name,
                            'mac': mac,
                            'type': driver,
                            'network': network})

    print ret_val
    return ret_val


def get_vswitch(server):
    """Return a list of vswitch dict with keys name, nicDevice"""
    mor, name = server.get_hosts().items()[0]
    prop = VIProperty(server, mor)
    ret_val = []
    for v in prop.configManager.networkSystem.networkConfig.vswitch:
        name = v.name
        nicDevice = v.spec.bridge.nicDevice  # this is a list
        ret_val.append({'name': name, 'nicDevice': nicDevice})

    return ret_val


def get_guests(server):
    """Return a list of dict guest"""

    properties = [
        'name',
        'storage.perDatastoreUsage',
        'config.hardware.memoryMB',
        'config.hardware.numCPU'
    ]
    results = server._retrieve_properties_traversal(
        property_names=properties,
        obj_type=MORTypes.VirtualMachine
    )

    ret_val = []
    if not results:
        return ret_val

    for item in results:
        for p in item.PropSet:
            if p.Name == 'config.hardware.memoryMB':
                memory = int(p.Val)
            if p.Name == 'config.hardware.numCPU':
                vcpu = int(p.Val)
            if p.Name == 'name':
                name = p.Val
        try:
            vm = server.get_vm_by_name(name)
        except:
            poweredOn = False
            disks = {}
            osVersion = ''
            annotation = ''
            vnics = []
            resourcePool = 'Default'
        else:
            annotation = vm.properties.config.annotation
            osVersion = vm.get_property('guest_full_name')
            poweredOn = vm.is_powered_on()
            disks = get_disks(vm)
            vnics = get_vnics(vm)
            resourcePool = vm.get_resource_pool_name()

        ret_val.append({'name': name,
                        'vcpu': vcpu,
                        'memory': memory,
                        'disks': disks,
                        'vnics': vnics,
                        'poweredOn': poweredOn,
                        'resourcePool': resourcePool,
                        'annotation': annotation,
                        'osVersion': osVersion})
    print ret_val
    return ret_val


def get_hardware(server):
    """Return a hardware dict"""
    ret_val = []

    mor, name = server.get_hosts().items()[0]
    prop = VIProperty(server, mor)
    overallMemoryUsage = prop.summary.quickStats.overallMemoryUsage
    overallCpuUsage = prop.summary.quickStats.overallCpuUsage
    numCpuThreads = prop.summary.hardware.numCpuThreads
    productName = prop.summary.config.product.name
    productVersion = prop.summary.config.product.version
    numCpuCores = prop.summary.hardware.numCpuCores
    numCpuPkgs = prop.summary.hardware.numCpuPkgs
    cpuModel = prop.summary.hardware.cpuModel
    numHBAs = prop.summary.hardware.numHBAs
    numNics = prop.summary.hardware.numNics
    cpuMhz = prop.summary.hardware.cpuMhz
    memorySize = prop.hardware.memorySize
    vendor = prop.summary.hardware.vendor
    model = prop.summary.hardware.model
    interfaces = get_interfaces(prop)
    datastores = get_datastores(server)

    ret_val.append({
            'name': name,
            'overallCpuUsage': overallCpuUsage,
            'overallMemoryUsage': overallMemoryUsage,
            'memorySize': memorySize / 1024 / 1024,
            'cpuModel': ' '.join(cpuModel.split()),
            'vendor': vendor,
            'numCpuPkgs': numCpuPkgs,
            'numCpuCores': numCpuCores,
            'numCpuThreads': numCpuThreads,
            'productName': productName,
            'productVersion': productVersion,
            'numNics': numNics,
            'numHBAs': numHBAs,
            'model': model,
            'cpuMhz': cpuMhz,
            'interfaces': interfaces,
            'datastores': datastores,
        })
    return ret_val

def insert_record_mysql(ret_val):
    """Insert record hardware dict to database"""
    hardware_val = ret_val
    #print hardware_val
    for i in hardware_val:
        #print i
        for j in i:
            #print j
            if j == 'name':
                name = i[j]
            if j == 'cpuModel':
                cpuModel = i[j]
                #print cpuModel
            if j == 'numCpuPkgs':
                numCpuPkgs = i[j]
                #print numCpuPkgs
            if j == 'vendor':
                vendor = i[j]
                #print vendor
            if j == 'model':
                model = i[j]
                #print model
        print name
        print vendor
        db = MySQLdb.connect("127.0.0.1","root","123.com","vops" )
        cursor = db.cursor()
        sql = "INSERT INTO web_hypervisor (name,cpuModel, vendor, model) VALUES ('%s', '%s',  '%s', '%s')" % (name,cpuModel, vendor, model)
        try:
            cursor.execute(sql)
            db.commit()
            print 'insert database successful'
        except:
            db.rollback()
            print 'insert database fail'
        db.close()



if __name__ == '__main__':
    """
    Config = ConfigParser.ConfigParser()
    Config.read(expanduser('~/.hypervisor.ini'))

    parser = OptionParser()
    parser.add_option('-H', '--hostname',
                      help='Host name, IP Address - mandatory')
    parser.add_option('-u', '--user', default='root',
                      help='User name [default: %default]')
    parser.add_option('-d', '--datacenter', default='',
                      help='Datacenter [default: %default]')
    parser.add_option('-p', '--password', type='string', default='',
                      help='Password to connect [default: %default]')
    parser.add_option('-a', '--anotation', type='string', default='',
                      help='Hypervisor Note [default: %default]')

    (options, args) = parser.parse_args()

    mandatories = ['hostname', 'datacenter']

    for m in mandatories:
        if getattr(options, m) is None:
            print '"%s" option is missing' % m
            parser.print_help()
            exit(-1)

    try:
        password = Config.get(options.user, 'password')
    except:
        password = ''

    if getattr(options, 'password'):
        password = options.password
    if not password:
        print '"password" option is missing'
        exit(-1)

    #user = options.user
    #hostname = options.hostname
    #datacenter = options.datacenter
    #note = options.anotation
    """

    hostname = "192.168.1.4"
    user = "root"
    password = "vmware"
    datacenter = ""
    note = ""

    try:
        server = vmware_connect(hostname, user, password)
        hardware = get_hardware(server)
        #print hardware
        insert_record_mysql(hardware)
        #get_datastores(server)
        #get_guests(server)

    except:
        exit(1)

    server = vmware_connect(hostname, user, password)
    properties = ['name']
    results = server._retrieve_properties_traversal(property_names=properties,obj_type=MORTypes.VirtualMachine)
    for item in results:
        for p in item.PropSet:
            if p.Name == 'name':
                name = p.Val
                vm = server.get_vm_by_name(name)
                #get_disks(vm)
                #get_vnics(vm)

    server.disconnect()
