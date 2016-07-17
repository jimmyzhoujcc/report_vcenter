'''
@description:   Insert items into json & excel
@author:        Jimmy Zhou
@Email:         13273980@qq.com
@date:          2016-06-24
'''
from __future__ import division
import sys,os.path
from pysphere import VIServer, MORTypes, VIProperty
from pysphere.resources import VimService_services as VI
import pysphere
import re
import pprint
import json
#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context


import xlsxwriter,xlrd

HOST='192.168.1.4'
USER="root"
PASSWORD="vmware"

stats = dict()

server = VIServer()
server.connect(HOST, USER, PASSWORD)
print '\033[32mVC connect successful...\033[0m'

for d, hname in server.get_hosts().items():

	HostMemoryUsage = 0
	HostCpuUsage = 0
	HostTotalMemory = 0
	HostNumCpuCores = 0
	HostMhzPerCore = 0
	HostStatus = ''

	props = server._retrieve_properties_traversal(property_names=[
		'name',
		'summary.overallStatus',
		'summary.quickStats.overallMemoryUsage',
		'summary.quickStats.overallCpuUsage',
		'summary.hardware.memorySize',
		'summary.hardware.numCpuCores',
		'summary.hardware.cpuMhz',
		'hardware.biosInfo',
		'hardware.systemInfo',
		'summary.runtime.healthSystemRuntime.hardwareStatusInfo.cpuStatusInfo',
		'summary.runtime.inMaintenanceMode',
		'summary.runtime.healthSystemRuntime.hardwareStatusInfo.memoryStatusInfo',
		'summary.runtime.healthSystemRuntime.hardwareStatusInfo.storageStatusInfo',
		'config.dateTimeInfo.ntpConfig.server'
		],from_node=d ,obj_type="HostSystem")

	for prop_set in props:
		#mor = prop_set.Obj #in case you need it
		for prop in prop_set.PropSet:
			if prop.Name == "summary.quickStats.overallMemoryUsage":
				HostMemoryUsage  = prop.Val
			elif prop.Name == "summary.runtime.inMaintenanceMode":
				MaintenanceMode = prop.Val
			elif prop.Name == "config.dateTimeInfo.ntpConfig.server":
				NtpServer = prop.Val.__dict__
				for i in  NtpServer['_string']:
					NtpConfigServer = i
			elif prop.Name == "summary.quickStats.overallCpuUsage":
				HostCpuUsage = prop.Val
			elif prop.Name == "summary.hardware.memorySize":
				HostTotalMemory = (prop.Val/1048576)
 			elif prop.Name == "summary.hardware.numCpuCores":
				HostNumCpuCores = prop.Val
			elif prop.Name == "summary.hardware.cpuMhz":
				HostMhzPerCore = prop.Val
			elif prop.Name == "summary.overallStatus":
				HostStatus = prop.Val
				if HostStatus == "green":
					HostStatus = 0
				elif HostStatus == "gray":
					HostStatus = 1
				elif HostStatus == "yellow":
					HostStatus = 2
				elif HostStatus == "red":
					HostStatus = 3
			elif prop.Name == "hardware.biosInfo":
				HostBiosInfo = prop.Val.__dict__['_biosVersion']
				#print HostBiosInfo
			elif prop.Name == "hardware.systemInfo":
				HostSystemInfo = prop.Val.__dict__
				HostType=HostSystemInfo['_model']
			elif prop.Name == "summary.runtime.healthSystemRuntime.hardwareStatusInfo.cpuStatusInfo":
				HostHealthInfo_cpu = prop.Val.__dict__
				for i in  HostHealthInfo_cpu['_HostHardwareElementInfo']:
					cpu= i.__dict__
					cpu1= cpu['_status'].__dict__
					HostCPUHealthInfo = cpu1['_label']
			elif prop.Name == "summary.runtime.healthSystemRuntime.hardwareStatusInfo.memoryStatusInfo":
				HostHealthInfo_memory = prop.Val.__dict__
				for i in HostHealthInfo_memory['_HostHardwareElementInfo']:
					mem=i.__dict__
					mem1= mem['_status'].__dict__
					#print mem1
					HostMemHealthInfo = mem1['_label']
				#print HostMemHealthInfo
			elif prop.Name == "summary.runtime.healthSystemRuntime.hardwareStatusInfo.storageStatusInfo":
				HostHealthInfo_storage = prop.Val.__dict__

	HostRunningVMS = len(server.get_registered_vms(d, status='poweredOn'))
	HostStoppedVMS = len(server.get_registered_vms(d, status='poweredOff'))
	HostTotalVMS = len(server.get_registered_vms(d))
	HostCpuTotal = (HostNumCpuCores * HostMhzPerCore)
	HostMemoryUsagePercent = ((HostMemoryUsage * 100)/HostTotalMemory)
	HostCpuUsagePercent = ((HostCpuUsage * 100)/HostCpuTotal)

	for ds, dsname in server.get_datastores().items():
		DatastoreCapacity = 0
		DatastoreFreespace = 0
		DatastoreUsagePercent = 0

		props = server._retrieve_properties_traversal(property_names=['name', 'summary.capacity', 'summary.freeSpace'],
												 from_node=ds, obj_type="Datastore")
		# print props
		for prop_set in props:
			for prop in prop_set.PropSet:
				if prop.Name == "summary.capacity":
					DatastoreCapacity = (prop.Val / 1073741824)
				elif prop.Name == "summary.freeSpace":
					DatastoreFreespace = (prop.Val / 1073741824)

		UsedSpace = DatastoreCapacity - DatastoreFreespace
		DatastoreUsagePercent = (((DatastoreCapacity - DatastoreFreespace) * 100) / DatastoreCapacity)

		metricnameZoneDatastoreCapacity = dsname.lower() + 'Capacity'
		metricnameZoneDatastoreFreespace = dsname.lower() + 'FreeSpace'
		metricnameZoneDatastoreUsagePercent = dsname.lower() + 'UsagePercent'

	hosts_dict={'hostname':hname.lower(),'NtpConfigServer':NtpConfigServer,'MaintenanceMode':MaintenanceMode,'numCpuCores':HostNumCpuCores, 'hoststatus':HostStatus, 'hostmemoryusage':HostMemoryUsage, 'hostcpuusage':HostCpuUsage, 'hosttotalmemory':HostTotalMemory, 'hostcputotal':HostCpuTotal, 'hostmemoryusagepercent':HostMemoryUsagePercent, 'hostcpuusagepercent':HostCpuUsagePercent, 'hostrunningvms':HostRunningVMS, 'hoststoppedvms':HostStoppedVMS, 'hosttotalvms':HostTotalVMS, 'hostbiosinfo':HostBiosInfo, 'hosttype':HostType,'hostcpuhealthinfo':HostCPUHealthInfo,'capacity':DatastoreCapacity, 'usagePercent':DatastoreUsagePercent}
	fl = open('/Users/jcc/PycharmProjects/untitled2/mysite/tools/hosts_info.js', 'w')
	fl.write(json.dumps(hosts_dict))
	fl.close()
	pprint.pprint(hosts_dict)

print '\033[32mVC disconnect successful...\033[0m'
server.disconnect()

fname = '/Users/jcc/PycharmProjects/untitled2/mysite/tools/report.xlsx'
if not os.path.isfile(fname):
    print 'report xls file is not exist'
    #sys.exit()
# Create an new Excel file and add a worksheet.

workbook = xlsxwriter.Workbook(fname)
worksheet = workbook.add_worksheet()

# Widen the first column to make the text clearer.
worksheet.set_column('A:A', 20)

# Add a bold format to highlight cell text.
bold = workbook.add_format({'bold': 1})

# Write some simple text.
top = workbook.add_format({'border':1,'align':'left','bg_color':'cccccc','font_size':13,'bold':True})
green = workbook.add_format({'border':1,'align':'center','bg_color':'green','font_size':12})
yellow = workbook.add_format({'border':1,'bg_color':'yellow','font_size':12})
red = workbook.add_format({'border':1,'align':'center','bg_color':'red','font_size':12})
worksheet.write('A1', 'Hostname',top)
worksheet.set_column('A:A', 13)
worksheet.write('B1', 'NumCpuCores', top)
worksheet.set_column('B:B', 12)
worksheet.write('C1', 'Memory', top)
worksheet.write('D1', 'DatastoreCapacity', top)
worksheet.set_column('D:D', 20)
worksheet.write('E1', 'CpuUsagePercent', top)
worksheet.set_column('E:E', 18)
worksheet.write('F1', 'MemoryUsagePercent', top)
worksheet.set_column('F:F', 18)
worksheet.write('G1', 'StorageUsagePercent', top)
worksheet.set_column('G:G', 23)
worksheet.write('H1', 'Alarm', top)
worksheet.write('I1', 'MaintenanceMode', top)
worksheet.set_column('I:I', 18)
worksheet.write('J1', 'HardwareModel', top)
worksheet.set_column('J:J', 22)
worksheet.write('K1', 'NTPServer', top)
worksheet.set_column('K:K', 23)
#worksheet.set_column(0,10,22)

# Write some numbers, with row/column notation.
worksheet.write(1, 0, hname.lower())
worksheet.write(1, 1, HostNumCpuCores)
worksheet.write(1, 2, HostTotalMemory)
worksheet.write(1, 3, DatastoreCapacity)
worksheet.write(1, 4, HostCpuUsagePercent)
worksheet.write(1, 5, HostMemoryUsagePercent)
worksheet.write(1, 6, DatastoreUsagePercent)

worksheet.write(1, 8, MaintenanceMode)
worksheet.write(1, 9, HostType)
worksheet.write(1, 10, NtpConfigServer)

workbook.close()