#!bin/bash

# This script configures the ROS environment variables. The ROS_IP and ROS_HOSTNAME are configured as the local IP
# If the IP of the ROS_MASTER_URI is given as an argument argument to this script, then the ROS_MASTER is set to  
# that address, otherwise the local ip is considered as master. The ROS_MASTER_URI is set, using the port 11311. 

LOC_IP_temp=`hostname -I`
export ROS_IP="192.168.31.220"
export ROS_HOSTNAME="192.168.31.220"
export ROS_MASTER_URI="http://192.168.31.220:11311"

echo "ROS_IP:         $ROS_IP"
echo "ROS_HOSTNAME:   $ROS_HOSTNAME"
echo "ROS_MASTER_URI: $ROS_MASTER_URI"
