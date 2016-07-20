#############################################################
# David Mitchell 2014/06/04
# Script to deploy VM(s) from Template(s) and set appropriate
# IP config for Windows VMs. Also sets # of CPUs, MemoryMB,
# port group.
# Moves deployed VM to specific VMs/Template blue folder.
# Assumptions:
# connected to viserver before running
# Customization spec and templates in place and tested
#############################################################
# Syntax and sample for CSV File:
# template,datastore,diskformat,vmhost,custspec,vmname,ipaddress,subnet,gateway,pdns,sdns,pwins,swins,datacenter,folder,stdpg,memsize,cpucount
# template.2008ent64R2sp1,DS1,thick,host1.domain.com,2008r2CustSpec,Guest1,10.50.35.10,255.255.255.0,10.50.35.1,10.10.0.50,10.10.0.51,10.10.0.50,10.10.0.51,DCName,FldrNm,stdpg.10.APP1,2048,1
#
$vmlist = Import-CSV “E:\DeployVMServers.csv”
# Load PowerCLI
$psSnapInName = “VMware.VimAutomation.Core”
if (-not (Get-PSSnapin -Name $psSnapInName -ErrorAction SilentlyContinue))
{
# Exit if the PowerCLI snapin can’t be loaded
Add-PSSnapin -Name $psSnapInName -ErrorAction Stop
}
connect-viserver ESX.yourdomain.local
foreach ($item in $vmlist) {
# Map variables
$template = $item.template
$datastore = $item.datastore
$diskformat = $item.diskformat
$vmhost = $item.vmhost
$custspec = $item.custspec
$vmname = $item.vmname
$ipaddr = $item.ipaddress
$subnet = $item.subnet
$gateway = $item.gateway
$pdns = $item.pdns
$sdns = $item.sdns
$datacenter = $item.datacenter
$destfolder = $item.folder
$stdpg = $item.stdpg
$memsize = $item.memsize
$cpucount = $item.cpucount
#Configure the Customization Spec info
Get-OSCustomizationSpec $custspec | Get-OSCustomizationNicMapping | Set-OSCustomizationNicMapping -IpMode UseStaticIp -IpAddress $ipaddr -SubnetMask $subnet -DefaultGateway $gateway -Dns $pdns,$sdns
#Deploy the VM based on the template with the adjusted Customization Specification
New-VM -Name $vmname -Template $template -Datastore $datastore -DiskStorageFormat $diskformat -VMHost $vmhost | Set-VM -OSCustomizationSpec $custspec -Confirm:$false
#Move VM to Application Group’s folder
Get-vm -Name $vmname | move-vm -Destination $(Get-Folder -Name $DestFolder -Location $(Get-Datacenter $Datacenter))
#Set the Port Group Network Name (Match PortGroup names with the VLAN name)
Get-VM -Name $vmname | Get-NetworkAdapter | Set-NetworkAdapter -NetworkName $stdpg -Confirm:$false
#Set the number of CPUs and MB of RAM
Get-VM -Name $vmname | Set-VM -MemoryMB $memsize -NumCpu $cpucount -Confirm:$false
}
Disconnect-VIServer ESX.yourdomain.local