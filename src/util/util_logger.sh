#!/bin/bash
#!/usr/bin/awk

echo "oieeee"
#config='/var/robo/ROBOS2/Adapter/config/config.ini'
log_dir='/var/robo/ROBOS2/Adapter/log'
nome=$1
pid_shell=$2
texto=$3
#sed -nr "/^\[$section\]/ { :l /^$param[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $config


echo "$(date "+%Y-%m-%d %H:%M:%S,%3N") $nome $pid_shell: $texto"
