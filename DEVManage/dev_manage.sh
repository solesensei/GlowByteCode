#!/bin/bash
#
# dev_manage.sh (rm)
# 
# The script managing DEV (SAS Servers, Mule, ActiveMQ, FED Servers)
# 
# Usage: bash dev_manage.sh [mule|sas|mq|fed|dev] [stop|start|status|restart]
# 
# GlowByte, v2.0, 03.2019
#

# Print help
if  [ $# -eq 0 ] || [ $1 == '-h' ] || [ $1 == "-help" ] || [ $1 == "--help" ]; then
    echo
    echo "-------------------- INFO --------------------"
    echo "Usage: bash dev_manage.sh [-h] [SYSTEM [SUB]] [NO] ACTION"
    echo "------                                        "
    echo "-h,--help   - prints this help message        "
    echo "SYSTEM      - mule | sas | mq | fed | dev     "
    echo "              if SYSTEM not specified - dev   "
    echo "SUB         - subsystem for SAS management    "
    echo "            - if SUB not specified - all SAS  " # TODO: add subsystems for sas
    echo "NO          - sas or fed server number        "
    echo "ACTION      - stop | start | status | restart "
    echo "----------------------------------------------"
    echo
    exit 0
fi

sys_n=""
# Parse arguments
if [ $# -lt 2 ]; then
    sys="dev"
    arg=$1
elif [ $# -eq 2 ]; then
    sys=$1
    arg=$2
elif [ $# -eq 3 ]; then
    sys=$1
    sys_n=$2
    arg=$3
else
    echo "To many arguments: $#"
    echo "Use -h for help"
    exit 1
fi

# Checking arguments
if [ $arg == "start" ] || [ $arg == "stop" ] || [ $arg == "restart" ] || [ $arg == "status" ]; then
    if [ $sys == "dev" ]; then
      
        if [ $arg != "status" ]; then
            read -p "Press ENTER to $arg DEV..."
        fi
    
    elif [ $# -ne 3 ] && ([ $sys == "mule" ] || [ $sys == "mq" ]); then

        if [ $arg != "status" ]; then
            read -p "Press ENTER to $arg $sys..."
        fi

    elif [ $sys == "sas" ] || [ $sys == "fed" ]; then
        
        if [ $# -eq 3 ]; then
            
            if [ $sys == "sas" ]; then
                case "$sys_n" in 
                1|2|6|7|11)
                    ;;
                *) 
                    echo "Error: No Sas Server $sys_n found"
                    echo "Use -h for help"
                    exit 1
                esac
            else # fed
                case "$sys_n" in 
                1|2)
                    ;;
                *) 
                    echo "Error: No Fed Server $sys_n found"
                    echo "Use -h for help"
                    exit 1
                esac
            fi
        fi   
        
        if [ $arg != "status" ]; then
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
case "$arg" in
start)
    if [ $sys = "dev" ] || [ $sys = "sas" ]; then
        echo "-------------------- INFO --------------------"
        echo "               SAS.SERVERS start              "
        echo "----------------------------------------------"
        /sas/sasconfig/Lev1/sas.servers start
    fi
    if [ $sys = "dev" ] || [ $sys = "fed" ]; then
        echo "-------------------- INFO --------------------"
        echo "              FED Servers start              "
        echo "----------------------------------------------"
        /sas/sashome/SASFederationServer/4.1/fedserver/bin/dfsadmin start
        /sas/sashome/SASFederationServer2/4.1/fedserver/bin/dfsadmin start
    fi
    if [ $sys = "dev" ] || [ $sys = "mule" ]; then
        echo "-------------------- INFO --------------------"
        echo "                  Mule starts                 "
        echo "----------------------------------------------"
        /sas/mule-standalone/bin/mule start
    fi
    if [ $sys = "dev" ] || [ $sys = "mq" ]; then
        echo "-------------------- INFO --------------------"
        echo "                ActiveMQ starts               "
        echo "----------------------------------------------"
        /sas/apache-activemq-5.15.2/bin/activemq start
    fi
    ;;
stop)
    if [ $sys = "dev" ] || [ $sys = "mq" ]; then
        echo "-------------------- INFO --------------------"
        echo "                ActiveMQ stops                "
        echo "----------------------------------------------"
        /sas/apache-activemq-5.15.2/bin/activemq stop
    fi
    if [ $sys = "dev" ] || [ $sys = "mule" ]; then
        echo "-------------------- INFO --------------------"
        echo "                  Mule stops                  "
        echo "----------------------------------------------"
        /sas/mule-standalone/bin/mule stop
    fi
    if [ $sys = "dev" ] || [ $sys = "fed" ]; then
        echo "-------------------- INFO --------------------"
        echo "               FED Servers stop               "
        echo "----------------------------------------------"
        /sas/sashome/SASFederationServer/4.1/fedserver/bin/dfsadmin stop
        /sas/sashome/SASFederationServer2/4.1/fedserver/bin/dfsadmin stop
    fi
    if [ $sys = "dev" ] || [ $sys = "sas" ]; then
        echo "-------------------- INFO --------------------"
        echo "                SAS.SERVERS stop              "
        echo "----------------------------------------------"
        /sas/sasconfig/Lev1/sas.servers stop
    fi
    ;;
status)
    if [ $sys = "dev" ] || [ $sys = "sas" ]; then
        echo "-------------------- INFO --------------------"
        echo "              SAS.SERVERS status              "
        echo "----------------------------------------------"
        /sas/sasconfig/Lev1/sas.servers status
    fi
    if [ $sys = "dev" ] || [ $sys = "mule" ]; then
        echo "-------------------- INFO --------------------"
        echo "                  Mule status                 "
        echo "----------------------------------------------"
        /sas/mule-standalone/bin/mule status
    fi
    if [ $sys = "dev" ] || [ $sys = "fed" ]; then
        echo "-------------------- INFO --------------------"
        echo "             FED Server 1 status              "
        echo "----------------------------------------------"
        /sas/sashome/SASFederationServer/4.1/fedserver/bin/dfsadmin status
        echo "-------------------- INFO --------------------"
        echo "             FED Server 2 status              "
        echo "----------------------------------------------"
        /sas/sashome/SASFederationServer2/4.1/fedserver/bin/dfsadmin status
    fi
    if [ $sys = "dev" ] || [ $sys = "mq" ]; then
        echo "-------------------- INFO --------------------"
        echo "                ActiveMQ status               "
        echo "----------------------------------------------"
        /sas/apache-activemq-5.15.2/bin/activemq status
    fi
    ;;
restart)
    if [ $sys = "dev" ] || [ $sys = "mq" ]; then
        echo "-------------------- INFO --------------------"
        echo "                 ActiveMQ stops               "
        echo "----------------------------------------------"
        /sas/apache-activemq-5.15.2/bin/activemq stop
    fi
    if [ $sys = "dev" ] || [ $sys = "mule" ]; then
        echo "-------------------- INFO --------------------"
        echo "                  Mule stops                  "
        echo "----------------------------------------------"
        /sas/mule-standalone/bin/mule stop
    fi
    if [ $sys = "dev" ] || [ $sys = "fed" ]; then
        echo "-------------------- INFO --------------------"
        echo "               FED Servers stop               "
        echo "----------------------------------------------"
        /sas/sashome/SASFederationServer/4.1/fedserver/bin/dfsadmin stop
        /sas/sashome/SASFederationServer2/4.1/fedserver/bin/dfsadmin stop
    fi
    if [ $sys = "dev" ] || [ $sys = "sas" ]; then
        echo "-------------------- INFO --------------------"
        echo "                SAS.SERVERS stop              "
        echo "----------------------------------------------"
        /sas/sasconfig/Lev1/sas.servers stop
        echo "-------------------- INFO --------------------"
        echo "               SAS.SERVERS start              "
        echo "----------------------------------------------"
        /sas/sasconfig/Lev1/sas.servers start
    fi
    if [ $sys = "dev" ] || [ $sys = "fed" ]; then
        echo "-------------------- INFO --------------------"
        echo "               FED Servers start              "
        echo "----------------------------------------------"
        /sas/sashome/SASFederationServer/4.1/fedserver/bin/dfsadmin start
        /sas/sashome/SASFederationServer2/4.1/fedserver/bin/dfsadmin start
    fi
    if [ $sys = "dev" ] || [ $sys = "mule" ]; then
        echo "-------------------- INFO --------------------"
        echo "                  Mule starts                 "
        echo "----------------------------------------------"
        /sas/mule-standalone/bin/mule start
    fi
    if [ $sys = "dev" ] || [ $sys = "mq" ]; then
        echo "-------------------- INFO --------------------"
        echo "                ActiveMQ starts               "
        echo "----------------------------------------------"
        /sas/apache-activemq-5.15.2/bin/activemq start
    fi
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
