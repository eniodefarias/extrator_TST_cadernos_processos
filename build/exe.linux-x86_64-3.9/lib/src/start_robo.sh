#!/bin/bash
#!/usr/bin/awk

#SHELL=/bin/bash
#PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/home/robo/.pyenv/shims/

#PATH=/home/robo/.pyenv/shims/

#source /home/robo/.pyenv/versions/3.6.7/envs/robos2/bin/activate


#original
#export PATH="~/.pyenv/shims:~/.pyenv/bin:$PATH"


#qtde_grupo_robos=$(groups $(whoami)| sed 's/ /\n/g;s/ //g'| grep "^robos$" | wc -l)
#
#if [ $qtde_grupo_robos -eq 1 ]
#    then
#        echo "qtde_grupo_robos: $qtde_grupo_robos"
#        echo "sg robos bash"
#        echo "usando o grupo robos"
#        sg robos bash
#fi


#export PATH="/home/enio/.pyenv/shims:~/.pyenv/bin:$PATH" #enio

name_hostname=$(hostname)
name_whoami=$(whoami)

if [ "$name_hostname" == "robos" ]
then
    name_whoami="retentiva"
fi

#export PATH="/home/robo/.pyenv/shims:~/.pyenv/bin:$PATH" #robo

export PATH="/home/$name_whoami/.pyenv/shims:~/.pyenv/bin:$PATH" #robo

export PYENV_VERSION=robos2


RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PINK='\033[0;35m'

NC='\033[0m' # No Color
#https://misc.flogisoft.com/bash/tip_colors_and_formatting
#printf "I ${RED}love${NC} Stack Overflow\n"

robo=$*

#pid=$$

dir='/var/robo/ROBOS2'
ini=$(date "+%Y/%m/%d-%H:%M:%S:%3N")

echo -e "\n\n${GREEN}######### INICIALIZAÇÃO ############${NC}"
#echo -e "${PINK}  PID: $pid${NC}"
echo -e "${YELLOW} ROBO: $robo${NC}"
echo -e "${BLUE}  INI: $ini${NC}\n"

cd $dir/Adapter/

pwd
python3 -V
#/home/robo/.pyenv/shims/python3 -V
#/home/robo/.pyenv/shims/python3.6 -V

roboname=$(echo "$robo" | cut -d"." -f1)

sleep 1
#if [ "$roboname" != "retentiva_015_envia_email_html" ]
# then
#    python3 retentiva_015_envia_email_html.py -s "$ini - Iniciado Robô: $roboname" -T "<div style='color:black !important; background-color:white !important; text-align: left !important; font-size: 15px !important; padding: 5px !important;'>$robo</div>"
#fi
python3 $robo
#/home/robo/.pyenv/shims/python3 $robo
#/home/robo/.pyenv/shims/python3.6 $robo

#| tee -a $dir/Adapter/log/$robo-completo.log &
#VPID=$!
#| tee -a $dir/Adapter/log/$robo-completo.log
fim=$(date "+%Y/%m/%d-%H:%M:%S:%3N")



#echo -e "$robo|$VPID|$ini" | tee -a $dir/Adapter/log/processos.log


#echo -e "$robo|$pid|$ini|$fim" | tee -a $dir/Adapter/log/processos.log
echo -e "\n"
#echo -e "$robo|$ini|$fim" | tee -a $dir/Adapter/log/processos.log
echo -e "$robo|$ini|$fim" >> $dir/Adapter/log/processos.log
#echo -e "$robo|$ini|$fim" | tee -a $dir/Adapter/log/processos.log

#if [ "$roboname" != "retentiva_015_envia_email_html" ]
# then
#    python3 retentiva_015_envia_email_html.py -s "$ini - Finalizado Robô: $roboname" -T "<div style='color:black !important; background-color:white !important; text-align: left !important; font-size: 15px !important; padding: 5px !important;'>$robo</div>"
#fi

echo -e "\n${YELLOW} ROBO: $robo${NC}"
echo -e "${BLUE}  INI: $ini${NC}"
echo -e "${RED}  FIM: $fim${NC}"
echo -e "${GREEN}#########  FINALIZAÇÃO  ############${NC}\n\n"
echo -e "\n\n"
#sleep 2
pwd

unset PYENV_VERSION