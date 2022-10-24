#!/bin/bash
#!/usr/bin/awk

config='/var/robo/ROBOS2/Adapter/config/config.ini'
section=$1
param=$2
sed -nr "/^\[$section\]/ { :l /^$param[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $config