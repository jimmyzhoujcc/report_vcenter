#!/usr/bin/env python
from django.db import models
from django.db.models import Sum
from pysphere import VIServer, MORTypes, VIProperty,VITask
from optparse import OptionParser
from pysphere.resources import VimService_services as VI
import ssl
#ssl._create_default_https_context = ssl._create_unverified_context

#import MySQLdb



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
        maintenanceMode = props.summary.maintenanceMode
        ret_val.append({'name': name,
                        'maintenanceMode': maintenanceMode,
                        'capacity': capacity,
                        'freeSpace': freeSpace})
    print ret_val
    return ret_val

def get_lun(server):
    """Return a list a lun dict with keys canonicalname, capabilities, uuid"""
    mor, name = server.get_hosts().items()[0]
    prop = VIProperty(server, mor)
    ret_val = []
    for lun in prop.configManager.storageSystem.storageDeviceInfo.scsiLun:
        canonicalName= lun.canonicalName
        #capabilities = lun.capabilities
        #displayname = lun.displayName
        uuid= lun.uuid
        ret_val.append({'canonicalName': canonicalName,
                        #'displayname':displayname,
                        'uuid': uuid})

    print ret_val
    return ret_val

def unmount_datastore(server):
    """Umount datastore by uuid"""
    ds_mor,name = server.get_hosts().items()[0]
    prop = VIProperty(server, ds_mor)
    request = VI.UnmountVmfsVolumeRequestMsg()
    #_this = request.new__this(ds_mor)
    #_this.set_attribute_type(ds_mor.get_attribute_type())
    request.vmfsUuid = '0000000000766d686261313a313a30'
    #spec = request.new__this

    #request.vmfsUuid = '0000000000766d686261313a313a30'
    print request
    #request = '0000000000766d686261313a313a30'
    for lun in prop.configManager.storageSystem.storageDeviceInfo.scsiLun:
        canonicalName = lun.canonicalName
        uuid = lun.uuid
        print canonicalName,uuid


    ret = server._proxy.UnmountVmfsVolume(request)._returnval
    print ret



    #ret = ds_mor.UnmountVmfsVolume(request)._returnval
    #task = VITask(ret, server)
    #status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
    #if status == task.STATE_SUCCESS:
    #    print "Datastore unmount successfully"
    #    ret = "Datastore unmount successfully"
    #elif status == task.STATE_ERROR:
    #    print "Error unmount datastore: %s" % task.get_error_message()
    #    ret = "Error unmount datastore: %s" % task.get_error_message()
    #return ret
    #print ret

def get_multipath(server):
    """Return a list a lun dict with keys canonicalname, capabilities, uuid"""
    mor, name = server.get_hosts().items()[0]
    prop = VIProperty(server, mor)
    ret_val = []
    for mp_path in prop.configManager.storageSystem.storageDeviceInfo.multipathInfo.lun:
        policy = mp_path.policy.policy
        for mp in mp_path.path:
            adapter = mp.adapter
            pathState= mp.pathState
            state = mp.state
            ret_val.append({'name':name,
                            'adapter': adapter,
                            'pathState': pathState,
                            'state': state})
    print policy
    print ret_val
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
    hostname = "192.168.1.4"
    user = "root"
    password = "vmware"
    datacenter = ""
    note = ""

    try:
        server = vmware_connect(hostname, user, password)
        #hardware = get_hardware(server)
        #print hardware
        #get_networks(server)
        #get_lun(server)
        #get_multipath(server)
        #insert_record_mysql(hardware)
        #get_datastores(server)
        #get_lun(server)
        unmount_datastore(server)
        #get_guests(server)

    except:
        exit(1)
    """
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
    """
    server.disconnect()
