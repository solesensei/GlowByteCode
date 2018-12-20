#!/bin/sh
#
# dfs_manage.sh (rc)
# 
# The script managing FED Server
# 
# Usage: bash dfs_manage.sh [stop|start|status|restart]
# 
# GlowByte, v1.0, 10.2018
#


# Print help
if  [ $# -eq 0 ] || [ $1 == '-h' ] || [ $1 == "-help" ] || [ $1 == "--help" ]; then
    echo
    echo "-------------------- INFO --------------------"
    echo "Usage: bash dfs_manage.sh [-h] ACTION"
    echo "------                                        "
    echo "-h,--help   - prints this help message        "
    echo "ACTION      - stop | start | status | restart "
    echo "----------------------------------------------"
    echo
    exit 0
fi

# Get argument
if [ "$1" = "start" ]; then
   arg=start
elif [ "$1" = "status" ]; then
   arg=status
elif [ "$1" = "restart" ]; then
   arg=restart
elif [ "$1" = "stop" ]; then
   arg=stop
else
   arg=$1
fi

time_start=$SECONDS
case "$arg" in
start)
    read -p "Press ENTER to start FED Server..."
    echo "-------------------- INFO --------------------"
    echo "               FED Server starts              "
    echo "----------------------------------------------"
    /sas/sashome/SASFederationServer/4.1/fedserver/bin/dfsadmin start
    ;;
stop)
    read -p "Press ENTER to stop FED Server..."
    echo "-------------------- INFO --------------------"
    echo "               FED Servers stop               "
    echo "----------------------------------------------"
    /sas/sashome/SASFederationServer/4.1/fedserver/bin/dfsadmin stop
    ;;
status)
    echo "-------------------- INFO --------------------"
    echo "             FED Server 1 status              "
    echo "----------------------------------------------"
    /sas/sashome/SASFederationServer/4.1/fedserver/bin/dfsadmin status
    ;;
restart)
    read -p "Press ENTER to restart FED Server..."
    echo "-------------------- INFO --------------------"
    echo "               FED Server stops               "
    echo "----------------------------------------------"
    /sas/sashome/SASFederationServer/4.1/fedserver/bin/dfsadmin stop
    echo "-------------------- INFO --------------------"
    echo "               FED Server starts              "
    echo "----------------------------------------------"
    /sas/sashome/SASFederationServer/4.1/fedserver/bin/dfsadmin start
    ;;
    *)
    echo "ERROR: No [$arg] action found"
    echo "Use -h for help"
    exit 1
    ;;
esac

timer=$(( $SECONDS - time_start ))
min=$((timer / 60))
sec=$((timer % 60))
echo "----------------------------------------------"
echo "Finished!"
echo "Time: ${min}m ${sec}s"
echo "----------------------------------------------"
