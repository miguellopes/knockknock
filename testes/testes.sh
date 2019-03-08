#!/bin/bash

PIDFILE='/var/run/knockknock/knock.pid'
PS=$(which ps)
GREP=$(which grep)
WC=$(which wc)
LS=$(which ls)

getpid() {
if [ -f $PIDFILE ]
then

 local pid=$(cat $PIDFILE)
 echo "$pid"
else
   echo "0"
fi
}

check_prof() {
   local chk=$($LS -1 /etc/knockknock.d/profiles/ | $WC -l)
if [ $chk == 0 ]
then
   knockknock-genprofile a 2
fi
}

check_process() {
   local status=$($PS -A | $GREP knockknock | $WC -l)
if [ "$status" == "0" ]
then
   #Nenhum processo encontrado
   echo 1
else
   #Algum processo encontrado
   echo 0
fi

}
C1=$(check_process)
if [ "$C1" == "0" ]
then
   echo "Processo antigo a correr..A tentar matar"
   killall "knockknock-daemon"
fi

pid=$(getpid)
if [ "$pid" == "0" ]
then
   echo "no pid checking profiles"
   check_prof
else
   echo "a apagar pidfile"
   rm -f $PIDFILE
fi
echo "A iniciar daemon"
knockknock-daemon

sleep 1

echo "Verificar pid"


pid=$(getpid)
if [ "$pid" == "0" ]
then
   echo "Erro: pidfile nao encontrado"
fi
echo "A enviar sigterm para  $pid"
kill -s 15 $pid


c2=$(check_process)
while [ "$c2" -eq "0" ]
do
   echo "Processo a correr..A esperar 2s"
   sleep 2
   
   c2=$(check_process)
done
pid=$(getpid)

echo "Resultado teste #1 gestao do pidfile por parte do daemon"
if [ "$pid" == "0" ]
then
   echo "Sucesso"
else
   echo "Falhou"
fi
echo " "
echo "Teste 2 - Gestao do servico com start-stop-daemon"

C1=$(check_process)
if [ "$C1" == "0" ]
then
   echo "Processo antigo a correr..A tentar matar"
   killall "knockknock-daemon"
fi
echo "Iniciar servico"
service knockknock start
sleep 1
echo "Verificar pid"

pid=$(getpid)
if [ "$pid" == "0" ]
then
   echo "Erro: pidfile nao encontrado"
fi
echo "Parar Servico"

service knockknock stop
sleep 1

C1=$(check_process)
if [ "$C1" == "0" ]
then
   echo "Processo antigo a correr..A tentar matar"
   killall "knockknock-daemon"
else
   echo "Processo Terminado. 1/2"
fi


pid=$(getpid)
if [ "$pid" == "0" ]
then
   echo "Pidfile removido com sucesso. 2/2"
fi


exit 1
