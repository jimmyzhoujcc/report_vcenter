#!/bin/bash
#Name:          get_capacity_fc_storage.sh
#Author:        jimmy zhou
#Email:         c_zhouyimin@cpic.oa.com.cn
#Usage:         get_capacity_fc_storage.sh
#Description:   Collect fc storage total capacity(GB)

###Define variable###
OS=`uname`
HOSTNAME=`hostname`
PATH_MP="/etc/multipath.conf"


###Function ollect fc storage total capacity###
function GET_CAPACITY(){
        #if [ -f "$PATH" ];then
        if [ -f "/tmp/capacity.txt" ];then
                #echo "Path is exist";
                capacityGB=`cat /tmp/capacity.txt | grep "G" | cut -d "G" -f 1 | awk '{sum+=$1}END{print sum}'`
                capacityTB=`cat /tmp/capacity.txt | grep "T" | cut -d "T" -f 1 | awk '{sum+=$1}END{print sum*1000}'`
                TotalCapacityGB=$(($capacityTB + $capacityGB))
                echo -e "$HOSTNAME\t$TotalCapacityGB"
        else
                echo "$PATH_MP is not exist,please try another way,script will exit"
                exit 1
        fi
}

###MAIN###
GET_CAPACITY
