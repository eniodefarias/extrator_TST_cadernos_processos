@ECHO OFF

color a

TITLE Instalador do Extrator TST

ECHO Iniciando instalacao do DOCKER
ECHO .
ECHO .
ECHO .


REM START "Instalacao DOCKER" /I /B src\win_Docker_Desktop_Installer.exe

REM ECHO Voce ja tem o DOCKER instalado neste computador?

set /p choice=Voce ja tem o DOCKER instalado neste computador? [S/N]
if '%choice%'=='N' goto label2
if '%choice%'=='Nao' goto label2
if '%choice%'=='Não' goto label2
if '%choice%'=='No' goto label2
if '%choice%'=='n' goto label2
if '%choice%'=='nao' goto label2
if '%choice%'=='não' goto label2
if '%choice%'=='no' goto label2

goto label1


:Label1
color c
ECHO .
ECHO .
ECHO .

ECHO Iniciando Build da Imagem no Docker
ECHO .
ECHO .
ECHO .

START "Build da Imagem DOCKER" /WAIT /I /B "%cd%"  "docker build -t extrator_tst_cadernos_processos ."

ECHO .
ECHO .
ECHO .

ECHO Instalacao concluida
ECHO .
ECHO .
ECHO .
ECHO Digite ENTER para fechar esse terminal
ECHO .
ECHO .
ECHO .
pause
move Instalador.bat TMP\
exit

:Label2
color b
Cls
ECHO .
ECHO .
ECHO .
ECHO ATENCAO, primeiro instale o programa DOCKER no computador antes de prosseguir com o Build da Imagem
ECHO .
ECHO link para download do DOCKER: https://docs.docker.com/desktop/install/windows-install/
ECHO .
start /MAX /D "https://docs.docker.com/desktop/install/windows-install/"

ECHO .

ECHO Apos instalar o DOCKER com o link acima, digite ENTER para finalizar a instalacao do Extrator
ECHO .
ECHO .
ECHO .
pause
set /p choice=Agora voce ja tem o DOCKER instalado neste computador? [S/N]
if '%choice%'=='N' goto label2
if '%choice%'=='Nao' goto label2
if '%choice%'=='Não' goto label2
if '%choice%'=='No' goto label2
if '%choice%'=='n' goto label2
if '%choice%'=='nao' goto label2
if '%choice%'=='não' goto label2
if '%choice%'=='no' goto label2
label1