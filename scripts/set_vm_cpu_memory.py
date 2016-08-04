'''''
This script just for reserving vm's cpu or memory, the method of definition is always contains special tag.
Usage:
    python reservation.py  10.21.138.9 147Testbed5 memory max
    python reservation.py  10.21.138.9 WIN7-Performance-14-1 cpu 0
Author: MyCo
Date: 2014-11-2
'''

import time
import threading
import os
import sys
import urllib2
import mmap
from urlparse import urlparse
from pysphere.vi_mor import VIMor, MORTypes
from pysphere import VIServer, VIProperty, VITask
from pysphere.resources import VimService_services as VI

global false, true, null

if len(sys.argv) < 4 or sys.argv[1] == '--help':
    print('Usage: python ' + sys.argv[0] + ' <VC-IP> ' + ' <vm-name> ' + ' <cpu/memory> ' + ' <size> ')
    sys.exit(0)

vc = sys.argv[1]
vmname = sys.argv[2]
types = sys.argv[3]
if sys.argv[4] == 'max':
    size = sys.argv[4]
else:
    size = int(sys.argv[4])

server = VIServer()
server.connect(vc, "root", "vmware")


# http://pubs.vmware.com/vsphere-50/index.jsp?topic=%2Fcom.vmware.wssdk.apiref.doc_50%2Fvim.vm.ConfigSpec.html
def set_vm_reservation(server, types, vm_name, reservation, level):
    vm_mor = server.get_vm_by_name(vm_name)

    request = VI.ReconfigVM_TaskRequestMsg()
    _this = request.new__this(vm_mor._mor)
    _this.set_attribute_type(vm_mor._mor.get_attribute_type())
    request.set_element__this(_this)
    spec = request.new_spec()

    # if you want set memory resource reservation for this virtual machine will always be equal to the virtual machine's memory size.
    if reservation == 'max' and types == 'memory':
        properties = ["config.hardware.memoryMB", "name"]
        results = server._retrieve_properties_traversal(property_names=properties, obj_type=MORTypes.VirtualMachine)
        for item in results:
            if (item.PropSet[1].Name == 'name' and item.PropSet[1].Val == vm_name) or (
                    item.PropSet[0].Name == 'name' and item.PropSet[0].Val == vm_name):
                reservation = item.PropSet[0].Val

    if types == 'cpu':
        allocation = spec.new_memoryAllocation()
    elif types == 'memory':
        allocation = spec.new_cpuAllocation()

        # cpu allocation settings
    allocation.set_element_expandableReservation("true")  # This property is ignored for virtual machines.
    allocation.set_element_limit(
        -1)  # If set to -1, then there is no fixed limit on resource usage (only bounded by available resources and shares). Units are MB for memory, MHz for CPU.
    allocation.set_element_reservation(reservation)
    obj_shares = allocation.new_shares()
    obj_shares.Level = level
    obj_shares.Shares = 0  # If level is not set to custom, this value is ignored. Therefore, only shares with custom values can be compared.
    allocation.Shares = obj_shares

    if types == 'cpu':
        spec.set_element_cpuAllocation(allocation)
    elif types == 'memory':
        spec.set_element_memoryAllocation(allocation)

    request.Spec = spec
    ret = server._proxy.ReconfigVM_Task(request)._returnval

    task = VITask(ret, server)
    status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
    if status == task.STATE_SUCCESS:
        ret = "VM <" + vm_name + "> successfully reconfigured"
    elif status == task.STATE_ERROR:
        print "Error reconfiguring vm <" + vm_name + ">: %s" % task.get_error_message()
        ret = "Error reconfiguring vm <" + vm_name + ">: %s" % task.get_error_message()
    return ret


# multiple set vm memory or cpu reservation
# --------------------------------------------------------------------------------------------
class multipleReservation(threading.Thread):
    def __init__(self, server, types, vm_name, reservation, level):
        threading.Thread.__init__(self)
        self.server = server
        self.types = types
        self.vm_name = vm_name
        self.reservation = reservation
        self.level = level

    def run(self):
        self.rtn = set_vm_reservation(self.server, self.types, self.vm_name, self.reservation, self.level)

    def get_return(self):
        return self.rtn

        # --------------------------------------------------------------------------------------------


def ModifyMultipleVMReservation(server, types, vm_name, reservation, level='normal'):
    rtn_dict = {}
    rtn_dict['success'] = []
    rtn_dict['error'] = []
    rtn_list = []
    thread_list = []
    vm_list = server.get_registered_vms()
    for path in vm_list:
        if vm_name in path:
            vm = server.get_vm_by_path(path)
            vmname = vm.get_property('name')
            runCMD = multipleReservation(server, types, vmname, reservation, level)
            thread_list.append(runCMD)

    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()

    for t in thread_list:
        rtn = t.get_return()
        print rtn
        if 'successfully' in rtn:
            rtn_dict['success'].append(rtn)
        else:
            rtn_dict['error'].append(rtn)

    return rtn_dict


# #--------------------------------------------------------------------------------------------
ModifyMultipleVMReservation(server, types, vmname, size)