#!/bin/bash
#!/usr/bin/awk

config='/var/robo/ROBOS2/Adapter/config/config.ini'
log_dir='/var/robo/ROBOS2/Adapter/log'

configsh() {
section=$1
param=$2
sed -nr "/^\[$section\]/ { :l /^$param[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $config
return
}


logger() {
#config='/var/robo/ROBOS2/Adapter/config/config.ini'
#nome=$1
#pid_shell=$2
texto=$*
#sed -nr "/^\[$section\]/ { :l /^$param[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $config
echo -e "$(date "+%Y-%m-%d %H:%M:%S,%3N") bash.$nome"_"$pid_shell: $texto" | tee -a $log_dir/robos.log >> $log_dir/$nome.log
echo -e "$texto"
return
}
xlogger() {
#config='/var/robo/ROBOS2/Adapter/config/config.ini'
#nome=$1
#pid_shell=$2
texto=$*
#sed -nr "/^\[$section\]/ { :l /^$param[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $config
echo -e "$(date "+%Y-%m-%d %H:%M:%S,%3N") bash.$nome"_"$pid_shell: $texto" | tee -a $log_dir/robos.log >> $log_dir/$nome.log
return
}


somente_numeros() {
num=$1
#num_somente=$(echo "$test_cpf"|sort|uniq|head -1 |sed 's/[^0-9]*//g'| sed 's/^0*//' )
num_somente=$(echo "$num"|sort|uniq|head -1 |sed 's/[^0-9]*//g' )
echo -n "$num_somente"
}

somente_numeros_sem_zero() {
numb=$1
num_sem_zero=$(echo "$numb"|sort|uniq|head -1 |sed 's/[^0-9]*//g'| sed 's/^0*//' )
echo -n "$num_sem_zero"
}



teste_cpf() {
test_cpf=$1
cpf_invalido_msg='CPF inválido*'
cpf_valido_msg=''

test_cpf_sem_zero=$(echo "$test_cpf"|sort|uniq|head -1 |sed 's/[^0-9]*//g'| sed 's/^0*//' )
test_cpf_com_zero=$(printf "%011d" $test_cpf_sem_zero)

#aplica o algoritimo:
#fonte: https://dicasdeprogramacao.com.br/algoritmo-para-validar-cpf/

#teste1: verifica se todos os digitos são iguais, se forem todos igual é um cpf inválido

if [ "$test_cpf_com_zero" == "00000000000" -o "$test_cpf_com_zero" == "11111111111" -o "$test_cpf_com_zero" == "22222222222" -o "$test_cpf_com_zero" == "33333333333" -o "$test_cpf_com_zero" == "44444444444" -o "$test_cpf_com_zero" == "55555555555" -o "$test_cpf_com_zero" == "66666666666" -o "$test_cpf_com_zero" == "77777777777" -o "$test_cpf_com_zero" == "88888888888" -o "$test_cpf_com_zero" == "99999999999"  ]
    then
        echo -n "$cpf_invalido_msg"
        else
            #não são todos os digitos iguais, aplica o algoritimo
            n1=$(echo -n "$test_cpf_com_zero"|cut -c1)
            n2=$(echo -n "$test_cpf_com_zero"|cut -c2)
            n3=$(echo -n "$test_cpf_com_zero"|cut -c3)
            n4=$(echo -n "$test_cpf_com_zero"|cut -c4)
            n5=$(echo -n "$test_cpf_com_zero"|cut -c5)
            n6=$(echo -n "$test_cpf_com_zero"|cut -c6)
            n7=$(echo -n "$test_cpf_com_zero"|cut -c7)
            n8=$(echo -n "$test_cpf_com_zero"|cut -c8)
            n9=$(echo -n "$test_cpf_com_zero"|cut -c9)
            n10=$(echo -n "$test_cpf_com_zero"|cut -c10)
            n11=$(echo -n "$test_cpf_com_zero"|cut -c11)

            #Primeiramente multiplica-se os 9 primeiros dígitos pela sequência decrescente de números de 10 à 2 e soma os resultados
            primeira_soma=$(( n1 * 10 + n2 * 9 + n3 * 8 + n4 * 7 + n5 * 6 + n6 * 5 + n7 * 4 + n8 * 3 + n9 * 2 ))
            primeiro_resto=$(( primeira_soma * 10 % 11 ))

            #obs: se primeiro_resto=10 > converte para primeiro_resto=0
            if [ $primeiro_resto -eq 10 ]
                then
                    primeiro_resto=0
            fi


            #verifica se primeiro_resto==n10
            if [ $primeiro_resto -eq $n10 ]
                then
                    #passou no primeiro teste

                    #começa segundo teste
                    #A validação do segundo dígito é semelhante à primeira, porém vamos considerar os 9 primeiros dígitos, mais o primeiro dígito verificador, e vamos multiplicar esses 10 números pela sequencia decrescente de 11 a 2.
                    segunda_soma=$(( n1 * 11 + n2 * 10 + n3 * 9 + n4 * 8 + n5 * 7 + n6 * 6 + n7 * 5 + n8 * 4 + n9 * 3 + n10 * 2 ))
                    segundo_resto=$(( segunda_soma * 10 % 11 ))

                    #obs: se segundo_resto=10 > converte para segundo_resto=0
                    if [ $segundo_resto -eq 10 ]
                        then
                            segundo_resto=0
                    fi


                    if [ $segundo_resto -eq $n11 ]
                        then
                            #passou no segundo teste
                            echo -n "$cpf_valido_msg"

                        else
                            echo -n "$cpf_invalido_msg"
                     fi

                else
                    echo -n "$cpf_invalido_msg"
             fi

    fi



}