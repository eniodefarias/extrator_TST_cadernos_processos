#!/bin/bash
#!/usr/bin/awk


filelog_a=$1

datalog=$(date "+%Y%m%d")

filelog=$( echo -n "$filelog_a"| sed 's/\.py$//g;s/\.sh$//g' )

dir='/var/robo/ROBOS2/Adapter/log'

echo "$dir/$filelog""_""$datalog.log"
sleep 3

#tail -F $dir/$filelog.log | perl -pe 's/^.*FATAL.*$/\e[1;37;41m$&\e[0m/g; s/^.*ERROR.*$/\e[1;31;40m$&\e[0m/g; s/^.*WARN.*$/\e[0;33;40m$&\e[0m/g; s/^.*INFO.*$/\e[0;36;40m$&\e[0m/g; s/^.*DEBUG.*$/\e[0;37;40m$&\e[0m/g'


#echo -e "\n SSH\n MYSQL\n SHELL\n FTP\n FATAL\n ERROR\n WARNNING\n INFO\n DEBUG\n" | perl -pe 's/^.*SSH.*$/\e[1;34;40m$&\e[0m/g;s/^.*MYSQL.*$/\e[1;35;40m$&\e[0m/g;s/^.*SHELL.*$/\e[1;32;40m$&\e[0m/g;s/^.*FTP.*$/\e[1;33;40m$&\e[0m/g;s/^.*FATAL.*$/\e[1;37;41m$&\e[0m/g; s/^.*ERROR.*$/\e[1;31;40m$&\e[0m/g; s/^.*WARN.*$/\e[0;33;40m$&\e[0m/g; s/^.*INFO.*$/\e[0;36;40m$&\e[0m/g; s/^.*DEBUG.*$/\e[0;37;40m$&\e[0m/g'

echo -e "\n SSH\n MYSQL\n SHELL\n FTP\n FATAL\n ERROR\n WARNNING\n INFO\n DEBUG\n" | perl -pe 's/^.*SSH.*$/\e[1;34;40m$&\e[0m/g;s/^.*MYSQL.*$/\e[1;35;40m$&\e[0m/g;s/^.*SHELL.*$/\e[1;32;40m$&\e[0m/g;s/^.*FTP.*$/\e[1;33;40m$&\e[0m/g;s/^.*FATAL.*$/\e[1;37;41m$&\e[0m/g; s/^.*ERROR.*$/\e[1;31;40m$&\e[0m/g; s/^.*WARN.*$/\e[0;33;40m$&\e[0m/g; s/^.*INFO.*$/\e[0;36;40m$&\e[0m/g; s/^.*DEBUG.*$/\e[105m$&\e[0m/g'


#tail -F $dir/$filelog.log | perl -pe 's/^.*SSH.*$/\e[1;34;40m$&\e[0m/g;s/^.*MYSQL.*$/\e[1;35;40m$&\e[0m/g;s/^.*SHELL.*$/\e[1;32;40m$&\e[0m/g;s/^.*FTP.*$/\e[1;33;40m$&\e[0m/g;s/^.*FATAL.*$/\e[1;37;41m$&\e[0m/g; s/^.*ERROR.*$/\e[1;31;40m$&\e[0m/g; s/^.*WARN.*$/\e[0;33;40m$&\e[0m/g; s/^.*INFO.*$/\e[0;36;40m$&\e[0m/g; s/^.*DEBUG.*$/\e[0;37;40m$&\e[0m/g'

#tail -F $dir/$filelog.log | perl -pe 's/^.*SSH.*$/\e[1;34;40m$&\e[0m/g;s/^.*MYSQL.*$/\e[1;35;40m$&\e[0m/g;s/^.*SHELL.*$/\e[1;32;40m$&\e[0m/g;s/^.*FTP.*$/\e[1;33;40m$&\e[0m/g;s/^.*FATAL.*$/\e[1;37;41m$&\e[0m/g; s/^.*ERROR.*$/\e[1;31;40m$&\e[0m/g; s/^.*WARN.*$/\e[0;33;40m$&\e[0m/g; s/^.*INFO.*$/\e[0;36;40m$&\e[0m/g; s/^.*DEBUG.*$/\e[105m$&\e[0m/g'
tail -F "$dir/$filelog""_""$datalog.log" | perl -pe 's/^.*SSH.*$/\e[1;34;40m$&\e[0m/g;s/^.*MYSQL.*$/\e[1;35;40m$&\e[0m/g;s/^.*SHELL.*$/\e[1;32;40m$&\e[0m/g;s/^.*FTP.*$/\e[1;33;40m$&\e[0m/g;s/^.*FATAL.*$/\e[1;37;41m$&\e[0m/g; s/^.*ERROR.*$/\e[1;31;40m$&\e[0m/g; s/^.*WARN.*$/\e[0;33;40m$&\e[0m/g; s/^.*INFO.*$/\e[0;36;40m$&\e[0m/g; s/^.*DEBUG.*$/\e[105m$&\e[0m/g;s/\n/\n\n/g'









#                                                                                                                                                              \n para quebra de linha
#tail -F $dir/$filelog.log | perl -pe 's/^.*FATAL.*$/\e[1;37;41m$&\e[0m/g; s/^.*ERROR.*$/\e[1;31;40m$&\e[0m/g; s/^.*WARN.*$/\e[0;33;40m$&\e[0m/g; s/^.*INFO.*$/\n\e[0;36;40m$&\e[0m/g; s/^.*DEBUG.*$/\e[0;37;40m$&\e[0m/g'


