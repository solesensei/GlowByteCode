#!/bin/bash
#
# dev_manage.sh (rm)
# 
# The script managing DEV (SAS Servers, Mule, ActiveMQ, FED Servers)
# 
# Usage: bash dev_manage.sh [mule|sas|mq|fed|dev] [stop|start|status|restart]
# 
# GlowByte, v2.1, 06.2019
#


SAS="/opt/sas"
ACTIVEMQ="/opt/sas/apache-activemq-*"
MULE="/opt/sas/mule-standalone"
FED="4.2"

# Print help
if  [ $# -eq 0 ] || [ $1 == '-h' ] || [ $1 == "-help" ] || [ $1 == "--help" ]; then
    echo
    echo "--------------------- INFO - HELP ---------------------"
    echo "Usage: bash dev_manage.sh [-h] [SYSTEM [SUB]] ACTION"
    echo "------                                        "
    echo "-h,--help   - prints this help message        "
    echo "SYSTEM      - mule | sas | mq | fed | dev     "
    echo "              if SYSTEM not specified - dev   "
    echo "SUB         - subsystem for SAS management    "
    echo "            - if SUB not specified - all SAS  "
    echo "ACTION      - stop | start | status | restart "
    echo "-------------------------------------------------------"
    echo "Use: bash dev_manage.sh sas [-h] for info about servers"
    echo "-------------------------------------------------------"
    echo
    exit 0
fi

# Print SAS Servers help
if [ $# -gt 1 ] && [ $1 == "sas" ] && ([ $2 == '-h' ] || [ $2 == "-help" ] || [ $2 == "--help" ]); then
    echo
    echo "--------------------- INFO - SAS SERVERS ---------------------"
    echo "Usage: bash dev_manage.sh sas [-h] [1|2|6|7]  ACTION"
    echo "------                                        "
    echo "-h,--help   - prints this help message        "
    echo "ACTION      - stop | start | status | restart "
    echo "-------------------- AVAILABLE SUBSYSTEMS --------------------"
    echo "1,2   - SAS Server 1,2    (SAS Content Server, Metadata Server, Remote Services)"
    echo "6     - SAS Server 6      (SAS CI Studio)"
    echo "7     - SAS Server 7      (SAS Design Server, SAS Engine Server)"
    echo "-------------------------------------------------------"
    echo
    exit 0
fi

sys_n=""
# Parse arguments
if [ $# -lt 2 ]; then
    sys="dev"
    arg="$1"
elif [ $# -eq 2 ]; then
    sys="$1"
    arg="$2"
elif [ $# -eq 3 ]; then
    sys="$1"
    sys_n="$2"
    arg="$3"
else
    echo "To many arguments: $#"
    echo "Use -h for help"
    exit 1
fi

# Checking arguments
if [ "$arg" == "start" ] || [ "$arg" == "stop" ] || [ "$arg" == "restart" ] || [ "$arg" == "status" ]; then
    if [ $sys == "dev" ]; then
      
        if [ "$arg" != "status" ]; then
            read -p "Press ENTER to $arg DEV..."
        fi
    
    elif [ $# -ne 3 ] && ([ "$sys" == "mule" ] || [ "$sys" == "mq" ] || [ "$sys" == "fed" ]); then

        if [ $arg != "status" ]; then
            read -p "Press ENTER to $arg $sys..."
        fi

    elif [ "$sys" == "sas" ]; then
        
        if [ $# -eq 3 ]; then
            
            case "$sys_n" in 
            1|2)
                sys_n=""
                sysname="ALL SAS SERVERS"
                saspath=${SAS}/sasconfig/Lev1/sas.servers
            ;;
            6)
                sysname="SAS Server 6 (CI Studio)"
                saspath=${SAS}/sasconfig/Lev1/Web/WebAppServer/SASServer6_1/bin/tcruntime-ctl.sh
            ;;
            7)
                sysname="SAS Server 7 (Design & Engine Servers)"
                saspath=${SAS}/sasconfig/Lev1/Web/WebAppServer/SASServer6_1/bin/tcruntime-ctl.sh
            ;;
            12|13)
                echo "WARNING: <anage option for SAS Server $sys_n is in developing"
                echo "Use -h for help"
                exit 1
            ;;
            *) 
                echo "Error: No Sas Server $sys_n found"
                echo "Use -h for help"
                exit 1
            esac

        fi   
        
        if [ "$arg" != "status" ]; then
            read -p "Press ENTER to $arg $sys $sys_n..."
        fi
        
    else
        echo "ERROR: No [$sys] system found"
        echo "Use -h for help"
        exit 1
    fi
else
    echo "ERROR: No [$arg] action found"
    echo "Use -h for help"
    exit 1
fi

time_start=$SECONDS
if [ "$sys" = "dev" ] || [ "$sys" = "sas" ]; then
    if [ -z "$sys_n" ]; then
        echo "-------------------- INFO --------------------"
        echo "               ALL SAS SERVERS ${arg}         "
        echo "----------------------------------------------"
        ${SAS}/sasconfig/Lev1/sas.servers ${arg}
    else
        echo "-------------------- INFO --------------------"
        echo "               ${sysname} ${arg}              "
        echo "----------------------------------------------"
        ${syspath} ${arg}
    fi
fi
if [ "$sys" = "dev" ] || [ "$sys" = "fed" ]; then
    echo "-------------------- INFO --------------------"
    echo "              FED Servers ${arg}              "
    echo "----------------------------------------------"
    ${SAS}/sashome/SASFederationServer/${FED}/fedserver/bin/dfsadmin ${arg}
fi
if [ "$sys" = "dev" ] || [ "$sys" = "mule" ]; then
    echo "-------------------- INFO --------------------"
    echo "                  Mule ${arg}                 "
    echo "----------------------------------------------"
    ${MULE}/bin/mule ${arg}
fi

if [ "$sys" = "dev" ] || [ "$sys" = "mq" ]; then
    echo "-------------------- INFO --------------------"
    echo "                ActiveMQ ${arg}               "
    echo "----------------------------------------------"
    ${ACTIVEMQ}/bin/activemq ${arg}
fi

timer=$(( $SECONDS - time_start ))
min=$((timer / 60))
sec=$((timer % 60))
echo "----------------------------------------------"
echo "Finished!"
echo "Time: ${min}m ${sec}s"
echo "----------------------------------------------"